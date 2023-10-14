import json
import os
class commons:
    def obter_arquivo_ou_secao_json(nome_arquivo: str, secoes: str = None, path:str = ''):
        path = ''.join(__file__).replace("commons.py", path + nome_arquivo + ".json")
        try:
            with open(path, 'r') as arq_json:
                arquivo = json.load(arq_json)

            if secoes is not None:
                secoes_separadas = secoes.split(":")
                if len(secoes_separadas) == 1:
                    return arquivo[secoes]

                for secao in secoes_separadas:
                    arquivo = arquivo[secao]

            return arquivo
        except Exception:
            raise