import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Alcance mínimo para leer perfil básico (nombre)
SCOPES = ["https://www.googleapis.com/auth/userinfo.profile"]

def main():
    # 1) Inicia el flujo OAuth (abre el navegador y obtiene el token)
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)  # inicia un servidor local temporal

    # 2) Llama al endpoint de userinfo (OAuth2 v2) para obtener el nombre
    service = build("oauth2", "v2", credentials=creds)
    me = service.userinfo().get().execute()  # dict con info del perfil

    # 3) Imprime el nombre del usuario autenticado
    #    'name' puede ser None si el perfil no lo expone; maneja ambos casos:
    nombre = me.get("name") or f"{me.get('given_name','')} {me.get('family_name','')}".strip()
    print(nombre if nombre else "Nombre no disponible")

if __name__ == "__main__":
    main()
