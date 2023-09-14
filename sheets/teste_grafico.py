from googleapiclient.discovery import build
from google.oauth2 import service_account

# Carregue suas credenciais do Google Cloud em formato JSON
credentials = service_account.Credentials.from_service_account_file('projetosamaka.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])

# ID da planilha
spreadsheet_id = '1VtwtPHPKl2YEwIawfOkn9VQATgqWcl5qquoQIKRno7Q'

# Crie uma solicitação para adicionar um gráfico de colunas
request = {
    "requests": [
        {
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "Data X Biomassa",
                        "titleTextPosition": {
                            "horizontalAlignment": "CENTER"
                        },
                        "basicChart": {
                            "chartType": "LINE",
                            "legendPosition": "BOTTOM_LEGEND",
                            "axis": [
                                {
                                    "position": "BOTTOM_AXIS",
                                    "title": "Data"
                                },
                                {
                                    "position": "LEFT_AXIS",
                                    "title": "Biomassa"
                                }
                            ],
                            "domains": [
                                {
                                    "domain": {
                                        "sourceRange": {
                                            "sources": [
                                                {
                                                    "sheetId": 680959972,
                                                    "startRowIndex": 237,
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
                                                    "sheetId": 680959972,
                                                    "startRowIndex": 237,
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
                        "overlayPosition": {
                            "anchorCell": {
                                "sheetId": 1187499399,
                                "rowIndex": 0,
                                "columnIndex": 0
                                },
                            "widthPixels": 400,
                            "heightPixels": 300
                        }
                    },
                }
            }#,
            # "addChart": {
            #     "chart": {
            #         "spec": {
            #             "title": "Data X Amonia",
            #             "titleTextPosition": {
            #                 "horizontalAlignment": "CENTER"
            #             },
            #             "basicChart": {
            #                 "chartType": "LINE",
            #                 "legendPosition": "BOTTOM_LEGEND",
            #                 "axis": [
            #                     {
            #                         "position": "BOTTOM_AXIS",
            #                         "title": "Data"
            #                     },
            #                     {
            #                         "position": "LEFT_AXIS",
            #                         "title": "Amonia"
            #                     }
            #                 ],
            #                 "domains": [
            #                     {
            #                         "domain": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 4,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 5
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ],
            #                 "series": [
            #                     {
            #                         "series": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 2,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 3
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ]
            #             }
            #         },
            #         "position": {
            #             "overlayPosition": {
            #                 "anchorCell": {
            #                     "sheetId": 1187499399,
            #                     "rowIndex": 0,
            #                     "columnIndex": 4
            #                     },
            #                 "widthPixels": 400,
            #                 "heightPixels": 300
            #             }
            #         },
            #     }
            # }#,
            # "addChart": {
            #     "chart": {
            #         "spec": {
            #             "title": "Data X Biomassa",
            #             "titleTextPosition": {
            #                 "horizontalAlignment": "CENTER"
            #             },
            #             "basicChart": {
            #                 "chartType": "LINE",
            #                 "legendPosition": "BOTTOM_LEGEND",
            #                 "axis": [
            #                     {
            #                         "position": "BOTTOM_AXIS",
            #                         "title": "Data"
            #                     },
            #                     {
            #                         "position": "LEFT_AXIS",
            #                         "title": "Biomassa"
            #                     }
            #                 ],
            #                 "domains": [
            #                     {
            #                         "domain": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 4,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 5
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ],
            #                 "series": [
            #                     {
            #                         "series": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 3,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 4
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ]
            #             }
            #         },
            #         "position": {
            #             "overlayPosition": {
            #                 "anchorCell": {
            #                     "sheetId": 1187499399,
            #                     "rowIndex": 0,
            #                     "columnIndex": 0
            #                     },
            #                 "widthPixels": 400,
            #                 "heightPixels": 300
            #             }
            #         },
            #     }
            # },
            # "addChart": {
            #     "chart": {
            #         "spec": {
            #             "title": "Data X Amonia",
            #             "titleTextPosition": {
            #                 "horizontalAlignment": "CENTER"
            #             },
            #             "basicChart": {
            #                 "chartType": "LINE",
            #                 "legendPosition": "BOTTOM_LEGEND",
            #                 "axis": [
            #                     {
            #                         "position": "BOTTOM_AXIS",
            #                         "title": "Data"
            #                     },
            #                     {
            #                         "position": "LEFT_AXIS",
            #                         "title": "Amonia"
            #                     }
            #                 ],
            #                 "domains": [
            #                     {
            #                         "domain": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 4,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 5
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ],
            #                 "series": [
            #                     {
            #                         "series": {
            #                             "sourceRange": {
            #                                 "sources": [
            #                                     {
            #                                         "sheetId": 680959972,
            #                                         "startRowIndex": 237,
            #                                         "startColumnIndex": 2,
            #                                         "endRowIndex": 252,
            #                                         "endColumnIndex": 3
            #                                     }
            #                                 ]
            #                             }
            #                         }
            #                     }
            #                 ]
            #             }
            #         },
            #         "position": {
            #             "overlayPosition": {
            #                 "anchorCell": {
            #                     "sheetId": 1187499399,
            #                     "rowIndex": 0,
            #                     "columnIndex": 4
            #                     },
            #                 "widthPixels": 400,
            #                 "heightPixels": 300
            #             }
            #         },
            #     }
            # },
        }
    ]
}

# Execute a solicitação para adicionar o gráfico à planilha
service = build('sheets', 'v4', credentials=credentials)
response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request).execute()
