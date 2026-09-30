"""Cria novos posts: pauta, redaÃ§Ã£o (Gemini), revisÃ£o em 10 etapas e imagens."""
import json
import re
import unicodedata

from . import fila, llm, revisor
from .config import PASTA_IMAGENS, RAIZ, carregar_perfil, carregar_prompt_sistema
from .imagem import gerar_imagens

ESQUEMA = """Responda SOMENTE com JSON neste formato:
{
  "posts": [
    {
      "formato": "carrossel" ou "card",
      "area": "exatamente o nome da Ã¡rea pedida",
      "titulo": "gancho da capa, atÃ© 8 palavras; destaque UMA palavra com *asteriscos*",
      "subtitulo": "frase curta de apoio na capa, atÃ© 12 palavras",
      "foto_busca": "2 a 4 palavras em inglÃªs para buscar foto (ex.: house keys document)",
      "slides": [ {"titulo": "atÃ© 6 palavras", "texto": "atÃ© 45 palavras"} ],
      "chamada_final": "pergunta que convide a comentar, atÃ© 10 palavras",
      "legenda": "80 a 180 palavras, parÃ¡grafos curtos, termina com chamada permitida",
      "hashtags": ["#exemplo"],
      "fontes": ["cada fundamento citado, ex.: CÃ³digo Civil, art. 1.245"]
    }
  ]
}
Regras do formato:
- "carrossel": de 4 a 6 slides de conteÃºdo (capa e encerramento sÃ£o automÃ¡ticos).
- "card": "slides" deve ser lista vazia; tÃ­tulo e subtÃ­tulo carregam a mensagem.
- De 6 a 10 hashtags especÃ­ficas, sem repetir as fixas.
- "fontes": sÃ³ o que consta nas tabelas da skill. Sem fundamento citado, lista vazia."""


def _ciclo(pesos: dict, inicio: int, qtd: int) -> list:
    """Distribui itens proporcionalmente aos pesos, de forma intercalada."""
    total = sum(pesos.values())
    sequencia, acumulado = [], {k: 0.0 for k in pesos}
    for _ in range(total):
        for k in pesos:
            acumulado[k] += pesos[k] / total
        escolhido = max(acumulado, key=acumulado.get)
        acumulado[escolhido] -= 1
        sequencia.append(escolhido)
    return [sequencia[(inicio + i) % len(sequencia)] for i in range(qtd)]


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.replace("*", "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:40]


def _prompt_usuario(perfil: dict, pedidos: list, tema: str | None) -> str:
    areas = {a["nome"]: a for a in perfil["areas"]}
    linhas = []
    for i, (formato, area) in enumerate(pedidos, start=1):
        exemplos = ", ".join(areas[area].get("temas_exemplo", []))
        linhas.append(f"Post {i}: formato {formato}; Ã¡rea {area} (ideias: {exemplos})")
    recentes = "\n".join(f"- {t}" for t in fila.titulos_recentes()) or "(nenhum ainda)"
    pauta = (f"Todos os posts devem tratar deste tema: {tema}" if tema else
             "Escolha temas com dÃºvidas reais e frequentes do pÃºblico, variando formatos "
             "de conteÃºdo (mito x verdade, checklist, passo a passo, erro comum, comparativo).")
    return f"""Crie {len(pedidos)} post(s) para o Instagram {perfil['advogado']['instagram']}
({perfil['advogado']['nome']}, {perfil['advogado']['cidade']}).

{chr(10).join(linhas)}

Tom de voz: {perfil['tom_de_voz']}
PÃºblico: {perfil['publico']}

{pauta}

NÃƒO repita estes tÃ­tulos jÃ¡ usados:
{recentes}

{ESQUEMA}"""


def gerar_lote(qtd: int | None = None, tema: str | None = None, area: str | None = None,
               datas: list | None = None) -> list:
    """Gera posts para as datas informadas (ou para as prÃ³ximas datas livres)."""
    perfil = carregar_perfil()
    if datas is None:
        qtd = qtd or perfil["calendario"]["posts_por_lote"]
        datas = fila.proximas_datas(qtd, perfil["calendario"]["dias_semana"])
    qtd = len(datas)
    inicio = len(fila.publicados()) + len(fila.na_fila())
    formatos = _ciclo(perfil.get("formatos", {"carrossel": 1}), inicio, qtd)
    areas = ([area] * qtd if area else
             _ciclo({a["nome"]: a.get("peso", 1) for a in perfil["areas"]}, inicio, qtd))

    pedidos = list(zip(formatos, areas))
    resposta = llm.gerar_json(carregar_prompt_sistema(),
                              _prompt_usuario(perfil, pedidos, tema) + _aprendizados())
    brutos = resposta.get("posts", [])[:qtd]

    criados = []
    for bruto, (formato, area_post), data in zip(brutos, pedidos, datas):
        if formato == "carrossel" and not bruto.get("slides"):
            formato = "card"
        post = {
            "id": f"{data.isoformat()}_{_slug(bruto.get('titulo', 'post'))}",
            "data_publicacao": data.isoformat(),
            "formato": formato,
            "area": area_post,
            "titulo": bruto["titulo"],
            "subtitulo": bruto.get("subtitulo", ""),
            "foto_busca": bruto.get("foto_busca", ""),
            "slides": bruto.get("slides", []) if formato == "carrossel" else [],
            "chamada_final": bruto.get("chamada_final", ""),
            "legenda": bruto["legenda"],
            "hashtags": bruto.get("hashtags", []),
            "fontes": bruto.get("fontes", []),
        }
        post = revisor.revisar(post)
        fixas = [h for h in perfil.get("hashtags_fixas", []) if h not in post["hashtags"]]
        post["hashtags"] = post["hashtags"] + fixas
        imagens = gerar_imagens(post, perfil, PASTA_IMAGENS)
        post["imagens"] = [p.relative_to(RAIZ).as_posix() for p in imagens]
        fila.salvar(post)
        criados.append(post)
    return criados


def _aprendizados() -> str:
    """Resumo do Ãºltimo relatÃ³rio de KPIs, para o agente repetir o que funciona."""
    from .kpi import aprendizados_para_prompt
    texto = aprendizados_para_prompt()
    return f"\n\nAPRENDIZADOS DOS KPIs (use como orientaÃ§Ã£o):\n{texto}" if texto else ""


def gerar_mes(ano: int, mes: int, lote: int = 3, pausa_s: int = 10) -> list:
    """ProgramaÃ§Ã£o do mÃªs inteiro (seg/qua/sex), gerada em lotes pequenos para
    respeitar o limite gratuito do Gemini."""
    import time
    from datetime import timedelta
    from .config import hoje

    perfil = carregar_perfil()
    datas = fila.datas_do_mes(ano, mes, perfil["calendario"]["dias_semana"],
                              a_partir_de=hoje() + timedelta(days=1))
    criados = []
    for i in range(0, len(datas), lote):
        criados += gerar_lote(datas=datas[i:i + lote])
        if i + lote < len(datas):
            time.sleep(pausa_s)
    return criados


def calendario_markdown(posts: list) -> str:
    dias = ["segunda", "terÃ§a", "quarta", "quinta", "sexta", "sÃ¡bado", "domingo"]
    from datetime import date
    linhas = ["| Data | Dia | Ãrea | Formato | TÃ­tulo | RevisÃ£o |", "|---|---|---|---|---|---|"]
    for p in sorted(posts, key=lambda x: x["data_publicacao"]):
        d = date.fromisoformat(p["data_publicacao"])
        ok = "âœ…" if p.get("revisao", {}).get("aprovado_pelo_revisor") else "âš ï¸"
        linhas.append(f"| {d.strftime('%d/%m')} | {dias[d.weekday()]} | {p['area']} | "
                      f"{p['formato']} | {p['titulo'].replace('*', '')} | {ok} |")
    return "\n".join(linhas)


def resumo_markdown(posts: list, url_base: str = "") -> str:
    """Corpo do Pull Request de aprovaÃ§Ã£o."""
    linhas = ["## ProgramaÃ§Ã£o para aprovaÃ§Ã£o da Dra. DircilÃ©ia Pacheco", "",
              calendario_markdown(posts), "",
              "Revise cada post. Para ajustar, edite o arquivo JSON em `posts/fila/`.",
              "**Fazer o merge deste Pull Request = aprovar a publicaÃ§Ã£o.** "
              "Para recusar um post, apague o JSON dele antes do merge.", ""]
    for p in posts:
        linhas += [f"### {p['data_publicacao']} Â· {p['area']} Â· {p['formato']}",
                   f"**{p['titulo'].replace('*', '')}**", "",
                   revisor.resumo(p), ""]
        r = p.get("revisao", {})
        if r.get("alertas_oab"):
            linhas += ["> âš ï¸ **Termos sensÃ­veis (OAB):** " + "; ".join(r["alertas_oab"]), ""]
        for e in r.get("etapas", []):
            if not e["ok"]:
                linhas.append(f"> âŒ {e['etapa']}: {e['obs']}")
        for img in p["imagens"]:
            linhas.append(f'<img src="{url_base}{img}" width="200">')
        linhas += ["", "<details><summary>Legenda e fontes</summary>", "",
                   p["legenda"], "", " ".join(p["hashtags"]), "",
                   "**Fontes citadas:** " + ("; ".join(p.get("fontes", [])) or "nenhuma"),
                   "</details>", ""]
    return "\n".join(linhas)


if __name__ == "__main__":
    print(json.dumps(gerar_lote(), ensure_ascii=False, indent=2))
