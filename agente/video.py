"""Gera Reels animados (1080x1920, 9:16, MP4 H.264) no estilo do perfil.

Roteiro a partir do mesmo JSON dos posts:
  capa         foto com zoom lento + degradê vinho, título e subtítulo surgindo
  slides       fundo creme, número deslizando, fio crescendo, texto subindo
  encerramento fundo vinho, frase em itálico e convite para salvar e compartilhar

Requer o ffmpeg do pacote imageio-ffmpeg (pip install imageio-ffmpeg).
A trilha de áudio é silenciosa (o Instagram aceita melhor vídeos com áudio).
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .config import carregar_perfil
from .fotos import obter_foto
from .imagem import (_hex, desenhar_titulo, fonte, paragrafo_ajustado, texto_espacado,
                     titulo_ajustado)

W, H = 1080, 1920
FPS = 30
M = 90
UTIL = W - M - 150   # margem direita maior: ícones do Reels ficam à direita
BASE = H - 400       # parte de baixo da tela é coberta pela legenda do Reels
TRANSICAO = 0.4  # segundos de fusão entre cenas


def _suave(p: float) -> float:
    """Curva de animação (ease-out cúbica)."""
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


class Elemento:
    """Um texto ou forma já desenhado, que entra em cena com um efeito."""

    def __init__(self, img: Image.Image, inicio: float, efeito: str = "subir", duracao: float = 0.7):
        caixa = img.getbbox() or (0, 0, 1, 1)
        self.img = img.crop(caixa)
        self.pos = caixa[:2]
        self.inicio, self.efeito, self.duracao = inicio, efeito, duracao

    def aplicar(self, quadro: Image.Image, t: float):
        p = _suave((t - self.inicio) / self.duracao)
        if p <= 0:
            return
        img = self.img
        x, y = self.pos
        if self.efeito == "subir":
            y += int(50 * (1 - p))
        elif self.efeito == "esquerda":
            x -= int(80 * (1 - p))
        elif self.efeito == "crescer":  # fio que cresce da esquerda para a direita
            largura = max(1, int(img.width * p))
            img = img.crop((0, 0, largura, img.height))
            p = 1.0
        if p < 1:
            img = img.copy()
            img.putalpha(img.getchannel("A").point(lambda v: int(v * p)))
        quadro.alpha_composite(img, (x, y))


def _camada():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


class Cena:
    def __init__(self, duracao: float, fundo, elementos: list):
        self.duracao, self.fundo, self.elementos = duracao, fundo, elementos

    def quadro(self, t: float) -> Image.Image:
        img = self.fundo(t).convert("RGBA")
        for e in self.elementos:
            e.aplicar(img, t)
        return img.convert("RGB")


class Roteirista:
    def __init__(self, perfil: dict):
        v = perfil["visual"]
        self.adv = perfil["advogado"]
        self.escura, self.clara = v["cor_escura"], v["cor_clara"]
        self.destaque, self.destaque_clara = v["cor_destaque"], v["cor_destaque_clara"]
        self.areia, self.texto_escuro = v["cor_areia"], v["cor_texto_escuro"]

    # ---- fundos
    def _fundo_foto(self, foto, duracao):
        grande = ImageOps.fit(foto, (int(W * 1.12), int(H * 1.12)), method=Image.LANCZOS)
        veu = Image.new("RGBA", (W, H))
        d = ImageDraw.Draw(veu)
        r, g, b, _ = _hex(self.escura)
        for y in range(H):
            t = y / H
            op = 0.70 - 2.3 * t if t < 0.15 else (0.36 if t < 0.32 else min(0.95, 0.36 + 1.15 * (t - 0.32)))
            d.line((0, y, W, y), fill=(r, g, b, int(255 * op)))

        def fundo(t):
            z = 1 + 0.12 * min(1.0, t / duracao)  # zoom lento
            cw, ch = int(grande.width / z), int(grande.height / z)
            x0, y0 = (grande.width - cw) // 2, (grande.height - ch) // 2
            base = grande.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
            return Image.alpha_composite(base.convert("RGBA"), veu)
        return fundo

    def _fundo_liso(self, cor):
        base = Image.new("RGB", (W, H), cor)
        return lambda t: base

    def _rodape(self, cor_linha, cor_texto, inicio):
        img, d = _camada()
        d.line((M, BASE, M + UTIL, BASE), fill=cor_linha, width=2)
        d.text((M, BASE + 30), f"{self.adv['nome']}  |  {self.adv['oab']}", font=fonte("texto", 30),
               fill=cor_texto)
        return Elemento(img, inicio, "subir", 0.6)

    # ---- cenas
    def capa(self, post, duracao):
        foto = obter_foto(post)
        fundo = self._fundo_foto(foto, duracao) if foto else self._fundo_liso(self.escura)
        els = []
        img, d = _camada()
        texto_espacado(d, (M, 150), self.adv["assinatura"], fonte("texto", 28), self.clara, 0.28)
        els.append(Elemento(img, 0.1, "subir"))

        tam, linhas, alt = titulo_ajustado(post["titulo"], UTIL, 760, 150, 90, 1.08)
        y_tit = 960 - alt // 2
        img, d = _camada()
        d.line((M, y_tit - 80, M + 70, y_tit - 80), fill=self.destaque_clara, width=4)
        texto_espacado(d, (M + 92, y_tit - 96), post["area"].upper(), fonte("negrito", 28), self.clara, 0.22)
        els.append(Elemento(img, 0.35, "esquerda"))

        img, d = _camada()
        y = desenhar_titulo(d, M, y_tit, tam, linhas, self.clara, self.destaque_clara, 1.08)
        els.append(Elemento(img, 0.6, "subir", 0.9))

        if post.get("subtitulo"):
            img, d = _camada()
            f, ls = paragrafo_ajustado(post["subtitulo"], "leve", UTIL, 200, 46, 34, 1.4)
            y += 80
            for linha in ls:
                d.text((M, y), linha, font=f, fill=self.clara)
                y += int(f.size * 1.4)
            els.append(Elemento(img, 1.3, "subir"))

        img, d = _camada()
        d.text((M, BASE + 30), self.adv["instagram"], font=fonte("texto", 32), fill=self.clara)
        els.append(Elemento(img, 1.6, "subir"))
        return Cena(duracao, fundo, els)

    def slide(self, post, n, total, slide, duracao):
        els = []
        img, d = _camada()
        texto_espacado(d, (M, 150), post["area"].upper(), fonte("negrito", 26), self.destaque, 0.24)
        texto_espacado(d, (W - M, 150), f"{n:02d} / {total:02d}", fonte("texto", 26), self.destaque,
                       0.2, ancora_direita=True)
        els.append(Elemento(img, 0.0, "subir", 0.4))

        tam, linhas, alt_t = titulo_ajustado(slide["titulo"], UTIL, 330, 96, 66)
        f, ls = paragrafo_ajustado(slide["texto"], "texto", UTIL, 620, 52, 38, 1.5)
        alt_txt = int(len(ls) * f.size * 1.5)
        y = max(300, 300 + (BASE - 300 - (230 + alt_t + 50 + 60 + alt_txt)) // 2)

        img, d = _camada()
        d.text((M - 8, y - 30), f"{n:02d}", font=fonte("titulo", 230), fill=self.destaque)
        els.append(Elemento(img, 0.15, "esquerda", 0.8))
        y += 230
        img, d = _camada()
        y = desenhar_titulo(d, M, y, tam, linhas, self.texto_escuro, self.destaque)
        els.append(Elemento(img, 0.45, "subir"))
        y += 50
        img, d = _camada()
        d.line((M, y, M + 160, y), fill=self.destaque, width=4)
        els.append(Elemento(img, 0.8, "crescer", 0.6))
        y += 60
        img, d = _camada()
        for linha in ls:
            d.text((M, y), linha, font=f, fill=self.texto_escuro)
            y += int(f.size * 1.5)
        els.append(Elemento(img, 1.0, "subir", 0.8))
        els.append(self._rodape(self.areia, self.texto_escuro, 0.2))
        return Cena(duracao, self._fundo_liso(self.clara), els)

    def encerramento(self, post, duracao):
        els = []
        img, d = _camada()
        texto_espacado(d, (M, 150), self.adv["assinatura"], fonte("texto", 28), self.destaque_clara, 0.28)
        els.append(Elemento(img, 0.0, "subir", 0.4))
        frase = post.get("chamada_final") or "Ficou com alguma dúvida?"
        tam, linhas, alt = titulo_ajustado(f"*{frase}*", UTIL, 560, 116, 72, 1.12)
        y = 380
        img, d = _camada()
        y = desenhar_titulo(d, M, y, tam, linhas, self.clara, self.clara, 1.12)
        els.append(Elemento(img, 0.2, "subir", 0.9))
        y += 80
        img, d = _camada()
        d.line((M, y, M + 160, y), fill=self.destaque_clara, width=4)
        els.append(Elemento(img, 0.9, "crescer", 0.6))
        y += 80
        for i, linha in enumerate(("Salve para consultar depois.",
                                   "Envie para quem precisa saber disso.",
                                   f"Siga {self.adv['instagram']}")):
            img, d = _camada()
            d.text((M, y), linha, font=fonte("leve" if i < 2 else "negrito", 44), fill=self.clara)
            els.append(Elemento(img, 1.2 + 0.25 * i, "subir"))
            y += 84
        els.append(self._rodape(self.destaque, self.clara, 0.3))
        return Cena(duracao, self._fundo_liso(self.escura), els)


def _roteiro(post: dict, perfil: dict) -> list:
    r = Roteirista(perfil)
    slides = post.get("slides", [])
    cenas = [r.capa(post, 3.6)]
    for i, s in enumerate(slides, start=1):
        palavras = len(s["texto"].split()) + len(s["titulo"].split())
        cenas.append(r.slide(post, i, len(slides), s, max(4.0, min(6.0, 2.2 + palavras * 0.13))))
    cenas.append(r.encerramento(post, 4.5))
    return cenas


def gerar_video(post: dict, pasta: Path, perfil: dict | None = None) -> tuple[Path, Path]:
    """Renderiza o Reels. Retorna (caminho do MP4, caminho da capa JPG)."""
    import imageio_ffmpeg

    perfil = perfil or carregar_perfil()
    pasta.mkdir(parents=True, exist_ok=True)
    saida = pasta / f"{post['id']}.mp4"
    capa = pasta / f"{post['id']}_capa.jpg"
    cenas = _roteiro(post, perfil)

    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
           "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "128k",
           "-movflags", "+faststart", str(saida)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    # Nos últimos TRANSICAO segundos de cada cena, ela se funde com o início da
    # próxima; a próxima então continua do ponto em que a fusão terminou.
    pular = 0.0
    for i, cena in enumerate(cenas):
        prox = cenas[i + 1] if i + 1 < len(cenas) else None
        q = int(round(pular * FPS))
        while q / FPS < cena.duracao:
            t = q / FPS
            img = cena.quadro(t)
            inicio_fusao = cena.duracao - TRANSICAO
            if prox and t >= inicio_fusao:
                tp = t - inicio_fusao
                img = Image.blend(img, prox.quadro(tp), tp / TRANSICAO)
            if i == 0 and q == int(2.6 * FPS):
                img.save(capa, "JPEG", quality=92)
            proc.stdin.write(img.tobytes())
            q += 1
        pular = TRANSICAO if prox else 0.0
    proc.stdin.close()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError("Falha ao gerar o vídeo (ffmpeg).")
    return saida, capa
