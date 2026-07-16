import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError


class GerenciaSheets:
    def __init__(self, id_planilha=""):
        self.id_planilha = id_planilha
        self.credenciais = None
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
        self.service = self._connect()

    def _connect(self) -> None:
        pasta = os.path.dirname(__file__)
        arquivo_token = os.path.join(pasta, "token.json")

        if os.path.exists(arquivo_token):
            credenciais = Credentials.from_authorized_user_file(arquivo_token, self.scopes)
            self.credenciais = credenciais
            try:
                return build("sheets", "v4", credentials=credenciais)
            except RefreshError:
                print("Token expirado.")
                return None
        else:
            print("Arquivo de token não encontrado.")
            return None

    def obter_perfil_usuario(self) -> tuple[str, str]:
        if not hasattr(self, 'credenciais') or not self.credenciais:
            return "Desconhecido", "Sem E-mail"
        
        try:
            service_cred = build("oauth2", "v2", credentials=self.credenciais)
            info = service_cred.userinfo().get().execute()
            return info.get("name", "Desconhecido"), info.get("email", "@iat.pr.gov.br")
        except Exception as e:
            print(f"Erro ao obter perfil do usuário: {e}")
            return "Desconhecido", "Sem E-mail"

    def escrever_dados(self, intervalo, dados) -> bool:
        if not self.service:
            print("Erro ao conectar com o Google Sheets.")
            return False

        body = {
            "values": dados
        }

        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.id_planilha,
                range=intervalo,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
        except Exception as e:
            print(f"Erro ao escrever na planilha: {e}")
            return False
        return True

    def ler_dados(self, intervalo) -> list[list[str]]:
        if not self.service:
            print("Erro ao conectar com o Google Sheets.")
            return []

        sheet = self.service.spreadsheets()
        resultado = sheet.values().get(spreadsheetId=self.id_planilha, range=intervalo).execute()
        return resultado.get("values", [])
