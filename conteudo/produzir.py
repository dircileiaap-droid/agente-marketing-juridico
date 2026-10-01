"""Produz as peças finais dos posts da fila (lâminas, stories e Reels) e roda os testes.

  python -m conteudo.produzir 2026-10 imagens   -> carrosséis e stories do mês
  python -m conteudo.produzir 2026-10 reels     -> Reels do mês (com os 10 testes)
  python -m conteudo.produzir 2026-10-05        -> só os posts dessa data
"""
import json
import sys
import time

from agente import compliance
from agente.config import PASTA_FILA, PASTA_IMAGENS, RAIZ, carregar_perfil

PASTA_VIDEOS = RAIZ / "posts" / "videos"


def _posts(filtro: str):
    for arq in sorted(PASTA_FILA.glob("*.json")):
        p = json.loads(arq.read_text(encoding="utf-8"))
        if p["data_publicacao"].startswith(filtro):
            yield arq, p


def _salvar(arq, p):
    arq.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")


def imagens(filtro: str):
    from agente.imagem import gerar_imagens
    from agente.stories import gerar_stories
    perfil = carregar_perfil()
    for arq, p in _posts(filtro):
        if p["formato"] in ("carrossel", "card"):
            caminhos = gerar_imagens(p, perfil, PASTA_IMAGENS)
        elif p["formato"] == "stories":
            caminhos = gerar_stories(p, perfil, PASTA_IMAGENS)
        else:
            continue
        p["imagens"] = [c.relative_to(RAIZ).as_posix() for c in caminhos]
        p["alertas_oab"] = compliance.verificar_post(p) if p["formato"] != "stories" else compliance.verificar(
            " ".join(q["titulo"] + " " + q.get("texto", "") for q in p["quadros"]))
        _salvar(arq, p)
        print(f"[ok] {p['id']}: {len(caminhos)} imagens, alertas OAB: {p['alertas_oab'] or 'nenhum'}")


def reels(filtro: str):
    from agente import qa_video
    from agente.musica import analisar
    from agente.video import fechar_roteiro, gerar_video, montar_roteiro
    perfil = carregar_perfil()
    for arq, p in _posts(filtro):
        if p["formato"] != "reel":
            continue
        t0 = time.time()
        p["musica"] = {"arquivo": p["trilha"], **analisar(RAIZ / p["trilha"], 55)}
        mp4, capa, _ = gerar_video(p, PASTA_VIDEOS, perfil)
        cenas, _ = montar_roteiro(p, perfil)
        resultado = qa_video.testar(mp4, p, cenas)
        fechar_roteiro(cenas)
        aprovados = sum(1 for _, _, ok, _ in resultado if ok)
        p["video"] = mp4.relative_to(RAIZ).as_posix()
        p["imagens"] = [capa.relative_to(RAIZ).as_posix()]
        p["testes_video"] = {"resultado": f"{aprovados}/10", "detalhes": [
            {"n": n, "teste": nome, "ok": ok, "obs": obs} for n, nome, ok, obs in resultado]}
        _salvar(arq, p)
        print(f"\n=== {p['id']} ({time.time() - t0:.0f}s) música {p['musica']} ===")
        print(qa_video.relatorio(resultado))


if __name__ == "__main__":
    filtro = sys.argv[1]
    modo = sys.argv[2] if len(sys.argv) > 2 else "tudo"
    if modo in ("imagens", "tudo"):
        imagens(filtro)
    if modo in ("reels", "tudo"):
        reels(filtro)
