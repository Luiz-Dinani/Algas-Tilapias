from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

vetor_dados=[]
arquivo = open("Arquivo_Temperatura.csv", 'r', encoding='UTF-8')
dados = arquivo.readlines()
for dado in dados:
    vetor_dados.append(dado.replace('\n','').split(";"))
def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    valores = vetor_dados
    result = sheet.values().update(spreadsheetId='17YOVJR--2xMkAtDlJnpe_ZoiW-ivZuc8yH1PFVdv59Y', range='Página2!A1', valueInputOption="RAW", body={"values":valores}).execute()

if __name__ == '__main__':
    main()