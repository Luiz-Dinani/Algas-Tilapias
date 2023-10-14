import requests as req
import xml.etree.ElementTree as ET
from commons import commons
def get_localidade(nome_cidade: str, uf: str):
    localidade_api = commons.obter_arquivo_ou_secao_json("appsettings", "services_references:api_localidade")
    retorno = req.get(localidade_api, params={"city": nome_cidade}).content
    xml_root = ET.fromstring(retorno)
    localidades = xml_root.findall('cidade')

    for localidade in localidades:
        #local_nome = localidade.find('nome').text
        local_uf = localidade.find('uf').text
        if (local_uf == uf.upper()):
            return localidade.find('id').text
    return None


