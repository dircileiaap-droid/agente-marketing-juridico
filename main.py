"""Agente de Marketing JurÃ­dico - linha de comando.

  python main.py gerar [--quantidade 3] [--tema "usucapiÃ£o"] [--area "Direito ImobiliÃ¡rio"]
  python main.py gerar-mes [--mes 2026-11]   (programaÃ§Ã£o do mÃªs para aprovaÃ§Ã£o)
  python main.py kpi-coletar                 (mÃ©tricas do Instagram)
  python main.py kpi-relatorio [--dias 30]
  python main.py listar
  python main.py publicar [--simular] [--max 1]
  python main.py demo                 (gera imagens de exemplo, sem usar API)
  python main.py verificar-token
  python main.py renovar-token
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from agente import fila
from agente.config import RAIZ, carregar_perfil


def carregar_env(arquivo: Path = RAIZ / ".env") -> None:
    """LÃª chaves do arquivo .env local (nunca enviado ao GitHub)."""
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8-sig").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#") and "=" in linha:
            nome, valor = linha.split("=", 1)
            valor = valor.strip().strip('"').strip("'")
            if valor:
                os.environ.setdefault(nome.strip(), valor)


carregar_env()


def url_base_imagens() -> str:
    """URL pÃºblica onde o Instagram vai buscar as imagens."""
    if os.environ.get("URL_IMAGENS"):
        return os.environ["URL_IMAGENS"].rstrip("/") + "/"
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        sys.exit("Defina URL_IMAGENS ou rode dentro do GitHub Actions.")
    ref = os.environ.get("GITHUB_REF_NAME", "main")
    return f"https://raw.githubusercontent.com/{repo}/{ref}/"


def cmd_gerar(args):
    from agente.gerador import gerar_lote, resumo_markdown

    from agente.revisor import resumo

    posts = gerar_lote(args.quantidade, args.tema, args.area)
    for p in posts:
        print(f"[novo] {p['data_publicacao']}  {p['area']}  {p['formato']}  {p['titulo']}")
        print(f"       {resumo(p)}")
    if args.resumo_pr:
        base = os.environ.get("URL_IMAGENS_PR", "")
        Path(args.resumo_pr).write_text(resumo_markdown(posts, base), encoding="utf-8")


def cmd_gerar_mes(args):
    from datetime import date
    from agente.gerador import gerar_mes, resumo_markdown
    from agente.revisor import resumo

    if args.mes:
        ano, mes = (int(x) for x in args.mes.split("-"))
    else:
        from agente.config import hoje
        dia = hoje()
        ano, mes = dia.year, dia.month
    posts = gerar_mes(ano, mes)
    print(f"ProgramaÃ§Ã£o de {mes:02d}/{ano}: {len(posts)} posts")
    for p in posts:
        print(f"[novo] {p['data_publicacao']}  {p['area']}  {p['formato']}  {p['titulo']}")
        print(f"       {resumo(p)}")
    if args.resumo_pr:
        base = os.environ.get("URL_IMAGENS_PR", "")
        Path(args.resumo_pr).write_text(resumo_markdown(posts, base), encoding="utf-8")


def cmd_kpi_coletar(_args):
    from agente.kpi import coletar
    foto = coletar()
    print(f"MÃ©tricas coletadas: {foto['seguidores']} seguidores, {len(foto['posts'])} posts.")


def cmd_kpi_relatorio(args):
    from agente.kpi import relatorio
    texto = relatorio(args.dias)
    if args.saida:
        Path(args.saida).parent.mkdir(parents=True, exist_ok=True)
        Path(args.saida).write_text(texto, encoding="utf-8")
    print(texto)


def cmd_listar(_args):
    posts = fila.na_fila()
    if not posts:
        print("Fila vazia.")
    for p in posts:
        print(f"{p['data_publicacao']}  {p['formato']:9}  {p['titulo']}")


def cmd_publicar(args):
    for p in fila.atrasados():
        print(f"[atrasado, NÃƒO publicado] {p['data_publicacao']} {p['titulo']}: "
              "defina nova data no JSON para publicar.")
    pendentes = fila.vencidos()[: args.max]
    if not pendentes:
        print("Nenhum post programado para hoje.")
        return

    base = url_base_imagens()
    ig = None
    if not args.simular:
        from agente.instagram import Instagram
        ig = Instagram()

    for post in pendentes:
        urls = [base + img for img in post["imagens"]]
        legenda = post["legenda"] + "\n\n" + " ".join(post["hashtags"])
        if args.simular:
            print(f"[simulaÃ§Ã£o] {post['titulo']}\n  imagens: {urls}\n")
            continue
        media_id = ig.publicar(urls, legenda)
        post["instagram_id"] = media_id
        post["publicado_em"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        fila.mover_para_publicados(post)
        print(f"[publicado] {post['titulo']} (id {media_id})")


def cmd_demo(_args):
    from agente.imagem import gerar_imagens

    post = {
        "id": "exemplo",
        "formato": "carrossel",
        "area": "Direito ImobiliÃ¡rio",
        "titulo": "VocÃª pagou pelo imÃ³vel. Mas ele Ã© *seu*?",
        "subtitulo": "Entenda a diferenÃ§a entre contrato, escritura e registro.",
        "foto_busca": "house keys contract",
        "slides": [
            {"titulo": "O contrato nÃ£o basta",
             "texto": "Contrato particular e recibo comprovam o negÃ³cio, mas nÃ£o "
                      "transferem a propriedade do imÃ³vel."},
            {"titulo": "A escritura formaliza",
             "texto": "A escritura pÃºblica, lavrada em tabelionato de notas, dÃ¡ forma "
                      "oficial Ã  compra e venda. Ainda assim, sozinha, ela nÃ£o "
                      "transfere a propriedade."},
            {"titulo": "O registro transfere",
             "texto": "A propriedade sÃ³ passa para o seu nome com o registro do tÃ­tulo "
                      "na matrÃ­cula, no CartÃ³rio de Registro de ImÃ³veis "
                      "(CÃ³digo Civil, art. 1.245)."},
            {"titulo": "Por que isso importa",
             "texto": "Sem registro, o imÃ³vel continua no nome do vendedor e pode ser "
                      "atingido por dÃ­vidas dele, alÃ©m de dificultar venda, heranÃ§a e "
                      "financiamento."},
        ],
        "chamada_final": "O seu imÃ³vel jÃ¡ estÃ¡ registrado no seu nome?",
    }
    pasta = RAIZ / "posts" / "exemplo"
    for c in gerar_imagens(post, carregar_perfil(), pasta):
        print(c.relative_to(RAIZ))


def cmd_verificar_token(_args):
    from agente.instagram import Instagram
    print(Instagram().perfil())


def cmd_renovar_token(_args):
    from agente.instagram import Instagram
    if os.environ.get("GITHUB_ACTIONS"):
        sys.exit("Rode este comando no seu computador: o token apareceria no log pÃºblico.")
    dados = Instagram().renovar_token()
    dias = int(dados.get("expires_in", 0)) // 86400
    print(f"Novo token vÃ¡lido por {dias} dias. Atualize o secret IG_ACCESS_TOKEN com:")
    print(dados["access_token"])


def main():
    p = argparse.ArgumentParser(description="Agente de Marketing JurÃ­dico")
    sub = p.add_subparsers(dest="comando", required=True)

    g = sub.add_parser("gerar", help="cria novos posts na fila")
    g.add_argument("--quantidade", type=int)
    g.add_argument("--tema")
    g.add_argument("--area", help='ex.: "Direito PrevidenciÃ¡rio" (padrÃ£o: rodÃ­zio por peso)')
    g.add_argument("--resumo-pr", help="grava resumo em Markdown (usado no Pull Request)")
    g.set_defaults(func=cmd_gerar)

    gm = sub.add_parser("gerar-mes", help="programaÃ§Ã£o do mÃªs inteiro para aprovaÃ§Ã£o")
    gm.add_argument("--mes", help="AAAA-MM (padrÃ£o: mÃªs atual)")
    gm.add_argument("--resumo-pr")
    gm.set_defaults(func=cmd_gerar_mes)

    sub.add_parser("kpi-coletar", help="coleta mÃ©tricas do Instagram").set_defaults(func=cmd_kpi_coletar)
    kr = sub.add_parser("kpi-relatorio", help="relatÃ³rio de KPIs")
    kr.add_argument("--dias", type=int, default=7)
    kr.add_argument("--saida")
    kr.set_defaults(func=cmd_kpi_relatorio)

    sub.add_parser("listar", help="mostra a fila").set_defaults(func=cmd_listar)

    pub = sub.add_parser("publicar", help="publica os posts do dia")
    pub.add_argument("--simular", action="store_true")
    pub.add_argument("--max", type=int, default=1)
    pub.set_defaults(func=cmd_publicar)

    sub.add_parser("demo", help="gera imagens de exemplo").set_defaults(func=cmd_demo)
    sub.add_parser("verificar-token").set_defaults(func=cmd_verificar_token)
    sub.add_parser("renovar-token").set_defaults(func=cmd_renovar_token)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
