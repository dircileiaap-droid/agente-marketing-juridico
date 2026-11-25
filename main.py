"""Agente de Marketing Jurídico - linha de comando.

  python main.py gerar [--quantidade 3] [--tema "usucapião"] [--area "Direito Imobiliário"]
  python main.py gerar-mes [--mes 2026-11]   (programação do mês para aprovação)
  python main.py kpi-coletar                 (métricas do Instagram)
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
    """Lê chaves do arquivo .env local (nunca enviado ao GitHub)."""
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
    """URL pública onde o Instagram vai buscar as imagens."""
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
    print(f"Programação de {mes:02d}/{ano}: {len(posts)} posts")
    for p in posts:
        print(f"[novo] {p['data_publicacao']}  {p['area']}  {p['formato']}  {p['titulo']}")
        print(f"       {resumo(p)}")
    if args.resumo_pr:
        base = os.environ.get("URL_IMAGENS_PR", "")
        Path(args.resumo_pr).write_text(resumo_markdown(posts, base), encoding="utf-8")


def cmd_kpi_coletar(_args):
    from agente.kpi import coletar
    foto = coletar()
    print(f"Métricas coletadas: {foto['seguidores']} seguidores, {len(foto['posts'])} posts.")


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
        print(f"{p['data_publicacao']}  {p['formato']:9}  {p.get('titulo', p['id'])}")


REPOSITORIO = "dircileiaap-droid/agente-marketing-juridico"
FIXAS = {"#abcpaulista", "#advocacia", "#saobernardodocampo"}


def hashtags_finais(post: dict, maximo: int = 5) -> list[str]:
    """As mais específicas do tema + #saobernardodocampo, sem repetir (máximo 5)."""
    temas = [h for h in post.get("hashtags", []) if h not in FIXAS]
    return list(dict.fromkeys(temas[: maximo - 1] + ["#saobernardodocampo"]))[:maximo]


def cmd_esperar(args):
    """Espera o horário do próximo post, se ele estiver perto. O GitHub atrasa as execuções;
    começando antes e esperando, o post sai na hora certa."""
    import time
    if fila.devidos():
        print("Há post no horário: não é preciso esperar.")
        return
    alvo = fila.proximo_alvo()
    agora = fila.agora_brasilia()
    if alvo is None or (alvo - agora).total_seconds() > args.max_min * 60:
        print(f"Nenhum post nos próximos {args.max_min} minutos.")
        return
    print(f"Próximo post: {alvo:%d/%m %H:%M}. Esperando {int((alvo - agora).total_seconds() // 60)} min.",
          flush=True)
    while (falta := (alvo - fila.agora_brasilia()).total_seconds()) > 0:
        time.sleep(min(falta + 1, 300))


def ja_no_ar(ig, legenda: str) -> str | None:
    """ID do post recente com a mesma legenda: evita repetir um post que saiu, mas cujo
    registro no repositório falhou."""
    inicio = " ".join(legenda.split())[:120]
    for m in ig.recentes():
        if inicio and " ".join((m.get("caption") or "").split()).startswith(inicio):
            return m["id"]
    return None


def cmd_publicar(args):
    for p in fila.atrasados():
        print(f"[atrasado, NÃO publicado] {p['data_publicacao']} {p['id']}: "
              "defina nova data no JSON para publicar.")
    # Cada post tem data e horário (feed 21h, Stories 14h, ou "horario": "10h"/"18h").
    # Só sai quando esse horário JÁ PASSOU: se o GitHub atrasar, o post sai um pouco
    # depois, nunca antes (em nov/2026 execuções atrasadas de madrugada publicavam o
    # post do dia às 0h30). O mais antigo sai primeiro.
    pendentes = fila.devidos()[: args.max]
    if not pendentes:
        print(f"Nenhum post no horário agora ({fila.agora_brasilia():%d/%m %H:%M}).")
        return

    from agente import facebook
    alcance = carregar_perfil().get("alcance", {})
    local = alcance.get("localizacao_id")
    base = url_base_imagens()
    ig = fb = None
    if not args.simular:
        from agente.instagram import Instagram
        ig = Instagram()
        fb = facebook.Facebook() if facebook.configurado() else None

    for post in pendentes:
        urls = [base + img for img in post["imagens"]]
        tags = hashtags_finais(post, alcance.get("max_hashtags", 5))
        legenda = (post.get("legenda", "") + "\n\n" + " ".join(tags)).strip()
        video = base + post["video"] if post.get("formato") == "reel" else None
        if args.simular:
            destino = "Instagram + Facebook" if facebook.configurado() else "Instagram"
            print(f"[simulação] {post['id']} -> {destino}\n  vídeo: {video}\n  imagens: {urls}\n"
                  f"  local: {local}  hashtags: {tags}\n  story de aviso: {post.get('story_aviso')}\n")
            continue
        if post.get("formato") == "stories":
            # telas na ordem do roteiro; o que já saiu fica anotado para não repetir
            ids = post.setdefault("stories_publicadas", [])
            for u in urls[len(ids):]:
                ids.append(ig.publicar_story(u))
                fila.salvar(post)
            media_id = ",".join(ids)
        elif media_id := ja_no_ar(ig, legenda):
            print(f"[já estava no ar] {post['id']}")
            post["story_aviso"] = None
        elif video:
            media_id = ig.publicar_reel(video, legenda, urls[0] if urls else None, local)
        else:
            media_id = ig.publicar(urls, legenda, local)
        post["instagram_id"] = media_id
        post["publicado_em"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        # Story "NOVO POST NO FEED": uma falha aqui não afeta o post já publicado
        if post.get("story_aviso") and alcance.get("story_aviso", True):
            try:
                post["story_aviso_id"] = ig.publicar_story(base + post["story_aviso"])
            except Exception as erro:  # noqa: BLE001
                post["story_aviso_erro"] = str(erro)[:300]
                print(f"[story de aviso] falhou: {erro}")
        # Facebook: uma falha aqui não desfaz nem bloqueia a publicação no Instagram
        if fb:
            try:
                post["facebook_id"] = fb.publicar(post, urls, video, legenda)
            except Exception as erro:  # noqa: BLE001
                post["facebook_erro"] = str(erro)[:500]
                print(f"[facebook] falhou: {erro}")
        fila.mover_para_publicados(post)
        print(f"[publicado] {post['id']} (instagram {media_id}, facebook {post.get('facebook_id', '-')})")


def cmd_demo(_args):
    from agente.imagem import gerar_imagens

    post = {
        "id": "exemplo",
        "formato": "carrossel",
        "area": "Direito Imobiliário",
        "titulo": "Você pagou pelo imóvel. Mas ele é *seu*?",
        "subtitulo": "Entenda a diferença entre contrato, escritura e registro.",
        "foto_busca": "house keys contract",
        "slides": [
            {"titulo": "O contrato não basta",
             "texto": "Contrato particular e recibo comprovam o negócio, mas não "
                      "transferem a propriedade do imóvel."},
            {"titulo": "A escritura formaliza",
             "texto": "A escritura pública, lavrada em tabelionato de notas, dá forma "
                      "oficial à compra e venda. Ainda assim, sozinha, ela não "
                      "transfere a propriedade."},
            {"titulo": "O registro transfere",
             "texto": "A propriedade só passa para o seu nome com o registro do título "
                      "na matrícula, no Cartório de Registro de Imóveis "
                      "(Código Civil, art. 1.245)."},
            {"titulo": "Por que isso importa",
             "texto": "Sem registro, o imóvel continua no nome do vendedor e pode ser "
                      "atingido por dívidas dele, além de dificultar venda, herança e "
                      "financiamento."},
        ],
        "chamada_final": "O seu imóvel já está registrado no seu nome?",
    }
    pasta = RAIZ / "posts" / "exemplo"
    for c in gerar_imagens(post, carregar_perfil(), pasta):
        print(c.relative_to(RAIZ))


def cmd_verificar_token(_args):
    from agente.instagram import Instagram
    print(Instagram().perfil())


def cmd_renovar_token(_args):
    """Renova a chave da Meta por mais 60 dias e a guarda no .env e no GitHub, sem mostrá-la."""
    import shutil
    import subprocess

    from agente.instagram import Instagram
    if os.environ.get("GITHUB_ACTIONS"):
        sys.exit("Rode este comando no seu computador.")
    gh = shutil.which("gh") or r"C:\Program Files\GitHub CLI\gh.exe"
    if not Path(gh).exists():
        sys.exit("GitHub CLI não encontrado: nada foi alterado.")

    dados = Instagram().renovar_token()
    nova = dados["access_token"]
    os.environ["IG_ACCESS_TOKEN"] = nova
    usuario = Instagram().perfil().get("username")  # confirma que a nova chave funciona
    dias = int(dados.get("expires_in", 0)) // 86400
    print(f"[1/3] Chave renovada por {dias} dias e testada (@{usuario}).")

    arquivo = RAIZ / ".env"
    linhas = arquivo.read_text(encoding="utf-8-sig").splitlines()
    linhas = [f"IG_ACCESS_TOKEN={nova}" if x.strip().startswith("IG_ACCESS_TOKEN") else x for x in linhas]
    arquivo.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("[2/3] Chave guardada no arquivo .env deste computador.")

    # a chave vai pela entrada padrão: não aparece na tela nem na lista de processos
    r = subprocess.run([gh, "secret", "set", "IG_ACCESS_TOKEN", "--repo", REPOSITORIO],
                       input=nova, text=True, capture_output=True)
    if r.returncode:
        sys.exit(f"[3/3] FALHOU ao enviar ao GitHub: {r.stderr.strip()[:200]}")
    print("[3/3] Chave enviada ao GitHub. Pronto!")


def main():
    p = argparse.ArgumentParser(description="Agente de Marketing Jurídico")
    sub = p.add_subparsers(dest="comando", required=True)

    g = sub.add_parser("gerar", help="cria novos posts na fila")
    g.add_argument("--quantidade", type=int)
    g.add_argument("--tema")
    g.add_argument("--area", help='ex.: "Direito Previdenciário" (padrão: rodízio por peso)')
    g.add_argument("--resumo-pr", help="grava resumo em Markdown (usado no Pull Request)")
    g.set_defaults(func=cmd_gerar)

    gm = sub.add_parser("gerar-mes", help="programação do mês inteiro para aprovação")
    gm.add_argument("--mes", help="AAAA-MM (padrão: mês atual)")
    gm.add_argument("--resumo-pr")
    gm.set_defaults(func=cmd_gerar_mes)

    sub.add_parser("kpi-coletar", help="coleta métricas do Instagram").set_defaults(func=cmd_kpi_coletar)
    kr = sub.add_parser("kpi-relatorio", help="relatório de KPIs")
    kr.add_argument("--dias", type=int, default=7)
    kr.add_argument("--saida")
    kr.set_defaults(func=cmd_kpi_relatorio)

    sub.add_parser("listar", help="mostra a fila").set_defaults(func=cmd_listar)

    pub = sub.add_parser("publicar", help="publica os posts do dia")
    pub.add_argument("--simular", action="store_true")
    pub.add_argument("--max", type=int, default=1)
    pub.set_defaults(func=cmd_publicar)

    sub.add_parser("demo", help="gera imagens de exemplo").set_defaults(func=cmd_demo)
    esp = sub.add_parser("esperar", help="espera o horário do próximo post (GitHub)")
    esp.add_argument("--max-min", type=int, default=320)
    esp.set_defaults(func=cmd_esperar)

    sub.add_parser("verificar-token").set_defaults(func=cmd_verificar_token)
    sub.add_parser("renovar-token").set_defaults(func=cmd_renovar_token)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
