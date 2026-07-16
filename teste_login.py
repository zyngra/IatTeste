import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

os.environ["oauthlib_insecure_transport"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


def test_login():
    pasta = os.path.dirname(__file__)
    arquivo_segredo = os.path.join(pasta, "client_secret.json")
    arquivo_token = os.path.join(pasta, "token.json")

    credenciais = None

    if os.path.exists(arquivo_token):
        credenciais = Credentials.from_authorized_user_file(arquivo_token, scopes)
    if not credenciais or not credenciais.valid:
        flow = InstalledAppFlow.from_client_secrets_file(arquivo_segredo, scopes)
        credenciais = flow.run_local_server(host="127.0.0.1", port=8080, prompt="consent")

        with open(arquivo_token, "w") as token_file:
            token_file.write(credenciais.to_json())

    return credenciais


if __name__ == "__main__":
    test_login()
