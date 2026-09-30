"""Publicação pela API oficial do Instagram (gratuita).

Usa a "Instagram API with Instagram Login" (conta Profissional: Criador ou
Empresa; não exige Página do Facebook).

Variáveis de ambiente:
  IG_USER_ID       ID numérico da conta do Instagram
  IG_ACCESS_TOKEN  token de longa duração (válido por 60 dias; renove com
                   `python main.py renovar-token`)
  IG_GRAPH_URL     opcional. Padrão: https://graph.instagram.com/v23.0
                   (para contas ligadas a Página do Facebook use
                   https://graph.facebook.com/v23.0)

Importante: a API só aceita imagens JPEG em URL pública. Por isso as imagens
ficam no próprio repositório (público) e são servidas pelo raw.githubusercontent.com.
"""
import os
import time

import requests

URL_PADRAO = "https://graph.instagram.com/v23.0"


class ErroInstagram(RuntimeError):
    pass


class Instagram:
    def __init__(self):
        self.user_id = os.environ.get("IG_USER_ID")
        self.token = os.environ.get("IG_ACCESS_TOKEN")
        # "or": no GitHub a variável pode existir mas vir vazia
        self.base = (os.environ.get("IG_GRAPH_URL") or URL_PADRAO).rstrip("/")
        if not (self.user_id and self.token):
            raise ErroInstagram("Defina IG_USER_ID e IG_ACCESS_TOKEN.")

    def _req(self, metodo: str, caminho: str, **params) -> dict:
        params["access_token"] = self.token
        resp = requests.request(metodo, f"{self.base}/{caminho}", params=params, timeout=60)
        dados = resp.json()
        if not resp.ok or "error" in dados:
            raise ErroInstagram(f"{caminho}: {dados.get('error', dados)}")
        return dados

    def _aguardar(self, container_id: str, limite_s: int = 300):
        """Espera o Instagram terminar de processar a mídia."""
        inicio = time.time()
        while time.time() - inicio < limite_s:
            status = self._req("GET", container_id, fields="status_code").get("status_code")
            if status == "FINISHED":
                return
            if status in ("ERROR", "EXPIRED"):
                raise ErroInstagram(f"Falha ao processar mídia {container_id}: {status}")
            time.sleep(5)
        raise ErroInstagram(f"Tempo esgotado processando {container_id}")

    def publicar(self, urls_imagens: list[str], legenda: str) -> str:
        """Publica imagem única ou carrossel (2 a 10 imagens). Retorna o ID do post."""
        if len(urls_imagens) == 1:
            container = self._req("POST", f"{self.user_id}/media",
                                  image_url=urls_imagens[0], caption=legenda)["id"]
        else:
            filhos = []
            for url in urls_imagens[:10]:
                filho = self._req("POST", f"{self.user_id}/media",
                                  image_url=url, is_carousel_item="true")["id"]
                filhos.append(filho)
            for filho in filhos:
                self._aguardar(filho)
            container = self._req("POST", f"{self.user_id}/media", media_type="CAROUSEL",
                                  children=",".join(filhos), caption=legenda)["id"]

        self._aguardar(container)
        return self._req("POST", f"{self.user_id}/media_publish", creation_id=container)["id"]

    def perfil(self) -> dict:
        return self._req("GET", "me", fields="user_id,username,followers_count,media_count")

    def renovar_token(self) -> dict:
        """Gera um novo token de 60 dias (o atual precisa ter mais de 24h e estar válido)."""
        resp = requests.get("https://graph.instagram.com/refresh_access_token",
                            params={"grant_type": "ig_refresh_token",
                                    "access_token": self.token}, timeout=60)
        dados = resp.json()
        if not resp.ok or "error" in dados:
            raise ErroInstagram(f"Falha ao renovar token: {dados}")
        return dados
