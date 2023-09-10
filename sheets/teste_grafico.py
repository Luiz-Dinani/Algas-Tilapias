from googleapiclient.discovery import build
from google.oauth2 import service_account

# Carregue suas credenciais do Google Cloud em formato JSON
credentials = service_account.Credentials.from_service_account_file('projetosamaka.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

# ID da planilha
spreadsheet_id = '1V-N1SOEJS4j5MIXoRF1j43vQmySQ2tsXowHNPFLhmUI'

# Crie uma solicitação para adicionar um gráfico de colunas
request = {
    "requests": [
        {
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "Meu Gráfico de Colunas",
                        "titleTextPosition": {
                            "horizontalAlignment": "CENTER"
                        },
                        "basicChart": {
                            "chartType": "LINE",
                            "legendPosition": "BOTTOM_LEGEND",
                            "axis": [
                                {
                                    "position": "BOTTOM_AXIS",
                                    "title": "Categorias"
                                },
                                {
                                    "position": "LEFT_AXIS",
                                    "title": "Valores"
                                }
                            ],
                            "domains": [
                                {
                                    "domain": {
                                        "sourceRange": {
                                            "sources": [
                                                {
                                                    "sheetId": 1364269422,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 4,
                                                    "endRowIndex": 252,
                                                    "endColumnIndex": 5
                                                }
                                            ]
                                        }
                                    }
                                }
                            ],
                            "series": [
                                {
                                    "series": {
                                        "sourceRange": {
                                            "sources": [
                                                {
                                                    "sheetId": 1364269422,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 2,
                                                    "endRowIndex": 252,
                                                    "endColumnIndex": 3
                                                }
                                            ]
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "position": {
                        "newSheet": True
                    }
                }
            },
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "Meu Gráfico de Colunas",
                        "titleTextPosition": {
                            "horizontalAlignment": "CENTER"
                        },
                        "basicChart": {
                            "chartType": "LINE",
                            "legendPosition": "BOTTOM_LEGEND",
                            "axis": [
                                {
                                    "position": "BOTTOM_AXIS",
                                    "title": "Categorias"
                                },
                                {
                                    "position": "LEFT_AXIS",
                                    "title": "Valores"
                                }
                            ],
                            "domains": [
                                {
                                    "domain": {
                                        "sourceRange": {
                                            "sources": [
                                                {
                                                    "sheetId": 1364269422,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 3,
                                                    "endRowIndex": 252,
                                                    "endColumnIndex": 4
                                                }
                                            ]
                                        }
                                    }
                                }
                            ],
                            "series": [
                                {
                                    "series": {
                                        "sourceRange": {
                                            "sources": [
                                                {
                                                    "sheetId": 1364269422,
                                                    "startRowIndex": 1,
                                                    "startColumnIndex": 2,
                                                    "endRowIndex": 252,
                                                    "endColumnIndex": 4
                                                }
                                            ]
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "position": {
                        "newSheet": True
                    }
                }
            }
        }
    ]
}

# Execute a solicitação para adicionar o gráfico à planilha
service = build('sheets', 'v4', credentials=credentials)
response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request).execute()
