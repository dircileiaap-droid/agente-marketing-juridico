"""Monta a pasta de aprovação no Windows (Imagens > Programação AAAA-MM) com uma
subpasta por publicação e uma página "Programação.html" com o calendário completo.

  python -m conteudo.apresentar 2026-10
"""
import html
import json
import shutil
import sys
from datetime import date
from pathlib import Path

from agente.config import PASTA_FILA, RAIZ

DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
MESES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]
FORMATO = {"carrossel": "Carrossel", "reel": "Reels animado", "stories": "Stories", "card": "Card"}


def _pasta_imagens() -> Path:
    import ctypes.wintypes
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, 39, None, 0, buf)  # CSIDL_MYPICTURES
    return Path(buf.value)


def montar(mes: str) -> Path:
    ano, m = (int(x) for x in mes.split("-"))
    destino = _pasta_imagens() / f"Programação {MESES[m].capitalize()} {ano}"
    destino.mkdir(parents=True, exist_ok=True)
    posts = [json.loads(a.read_text(encoding="utf-8")) for a in sorted(PASTA_FILA.glob(f"{mes}-*.json"))]
    blocos, linhas_tabela = [], []
    for p in posts:
        d = date.fromisoformat(p["data_publicacao"])
        hora = "14h" if p["formato"] == "stories" else "21h"
        titulo = (p.get("titulo") or p["quadros"][0]["titulo"]).replace("*", "")
        nome = f"{d.strftime('%d-%m')} {DIAS[d.weekday()]} - {FORMATO[p['formato']]}"
        pasta = destino / nome
        pasta.mkdir(exist_ok=True)
        midias = []
        if p["formato"] == "reel":
            shutil.copy2(RAIZ / p["video"], pasta / "Reels.mp4")
            midias.append(("video", "Reels.mp4"))
        for i, img in enumerate(p.get("imagens", []), start=1):
            if p["formato"] == "reel":
                break
            nome_img = f"{'Tela' if p['formato'] == 'stories' else 'Lamina'} {i:02d}.jpg"
            shutil.copy2(RAIZ / img, pasta / nome_img)
            midias.append(("img", nome_img))
        legenda = (p.get("legenda", "") + "\n\n" + " ".join(p.get("hashtags", []))).strip()
        if legenda:
            (pasta / "Legenda.txt").write_text(legenda, encoding="utf-8-sig")

        testes = p.get("testes_video", {}).get("resultado")
        selo = f"Testes do vídeo: {testes}" if testes else "Revisão em 10 etapas ✔"
        linhas_tabela.append(
            f"<tr><td>{d.strftime('%d/%m')}</td><td>{DIAS[d.weekday()]}</td><td>{hora}</td>"
            f"<td>{FORMATO[p['formato']]}</td><td>{html.escape(p['area'])}</td><td>{html.escape(titulo)}</td></tr>")
        galeria = "".join(
            f'<video src="{html.escape(nome)}/{f}" controls preload="metadata"></video>' if t == "video"
            else f'<img src="{html.escape(nome)}/{html.escape(f)}" loading="lazy">' for t, f in midias)
        fontes = "".join(f"<li>{html.escape(f)}</li>" for f in p.get("fontes", []))
        blocos.append(
            f'<section><h2>{d.strftime("%d/%m")} · {DIAS[d.weekday()]} · {hora} · {FORMATO[p["formato"]]}</h2>'
            f'<p class="area">{html.escape(p["area"])} · <b>{html.escape(titulo)}</b> · <span class="ok">{selo}</span></p>'
            f'<div class="galeria {p["formato"]}">{galeria}</div>'
            + (f'<details><summary>Legenda</summary><pre>{html.escape(legenda)}</pre></details>' if legenda else "")
            + f'<details><summary>Fontes conferidas</summary><ul>{fontes}</ul></details></section>')

    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Programação {MESES[m]} {ano}</title>
<style>
:root{{--vinho:#3E231D;--terracota:#A8553F;--creme:#F3EADB;--areia:#E4D5BF}}
body{{margin:0;background:var(--creme);color:#2E1B16;font:16px/1.5 Georgia,serif}}
header{{background:var(--vinho);color:var(--creme);padding:28px 24px}}
header h1{{margin:0;font-weight:500}} header p{{margin:6px 0 0;opacity:.85}}
main{{max-width:1100px;margin:auto;padding:16px}}
table{{width:100%;border-collapse:collapse;background:#fff;margin:16px 0 32px}}
td,th{{padding:8px 10px;border-bottom:1px solid var(--areia);text-align:left;font-size:14px}}
th{{background:var(--areia)}}
section{{background:#fff;border-radius:10px;padding:16px;margin:18px 0;box-shadow:0 1px 3px #0001}}
h2{{margin:0 0 4px;color:var(--terracota);font-weight:500}}
.area{{margin:0 0 10px}} .ok{{color:#2f6b3a}}
.galeria{{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}}
.galeria img{{height:300px;border-radius:6px}} .galeria video{{height:420px;border-radius:6px;background:#000}}
.stories img{{height:360px}}
pre{{white-space:pre-wrap;font:14px/1.5 system-ui,sans-serif;background:var(--creme);padding:10px;border-radius:6px}}
summary{{cursor:pointer;color:var(--terracota);margin-top:8px}}
</style></head><body>
<header><h1>Programação de {MESES[m]} de {ano}</h1>
<p>Dirciléia Pacheco · @dircileiaaparecida_adv · Feed: segunda, quarta e sexta, às 21h · Stories: sábado, às 14h</p></header>
<main><table><tr><th>Data</th><th>Dia</th><th>Hora</th><th>Formato</th><th>Área</th><th>Tema</th></tr>
{''.join(linhas_tabela)}</table>{''.join(blocos)}</main></body></html>"""
    (destino / "Programação.html").write_text(pagina, encoding="utf-8")
    return destino


if __name__ == "__main__":
    print(montar(sys.argv[1]))
