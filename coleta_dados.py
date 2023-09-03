import pandas as pd
dados_abril = pd.read_csv('./Temperatura/6e385352-a20d-42fb-805d-b1e735852678.csv')
dados_marco = pd.read_csv('./Temperatura/43edf9f6-dffb-43da-a562-a0bc1f889a5c.csv')
dados_fever = pd.read_csv('./Temperatura/72b69a12-7e7f-c572-af3e-359e1dad2e52.csv')
dados_janei = pd.read_csv('./Temperatura/f91c3ca6-7c9f-7d1e-f004-4ea88b7d73ab.csv')
dados = pd.DataFrame()
cidades_california = ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose", "Oakland", "Fresno", "Long Beach", "Anaheim", "Santa Monica"]
dados_abril=dados_abril[['DATA 0','TIME 0', 'LOCATION 0']]
dados_marco=dados_marco[['DATA 0','TIME 0', 'LOCATION 0']]
dados_fever=dados_fever[['DATA 0','TIME 0', 'LOCATION 0']]
dados_janei=dados_janei[['DATA 0','TIME 0', 'LOCATION 0']]
dados['Mes']=pd.concat([dados_abril['TIME 0'],dados_marco['TIME 0'],dados_fever['TIME 0'],dados_janei['TIME 0']], axis=0, ignore_index=True)
dados['Temp']=pd.concat([dados_abril['DATA 0'],dados_marco['DATA 0'],dados_fever['DATA 0'],dados_janei['DATA 0']], axis=0, ignore_index=True)
dados['Cidade']=pd.concat([dados_abril['LOCATION 0'],dados_marco['LOCATION 0'],dados_fever['LOCATION 0'],dados_janei['LOCATION 0']], axis=0, ignore_index=True)
dados=dados[dados['Cidade'].isin(cidades_california)]
dados.to_csv("Arquivo_Temperatura.csv", index=False, sep=';')