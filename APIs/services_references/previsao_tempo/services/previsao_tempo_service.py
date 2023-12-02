from services_references.localidade.services import localidade_service
from commons import commons
import requests as req
import xml.etree.ElementTree as ET
from services_references.previsao_tempo.models.previsao_tempo_model import PrevisaoTempoModel

def get_temperatura(nome_cidade: str, uf: str) -> list[PrevisaoTempoModel] | None:
    id_cidade = localidade_service.get_localidade(nome_cidade, uf)
    if (id_cidade is None):
        return None

    api_temperatura = commons.obter_arquivo_ou_secao_json("appsettings", "services_references:api_temperatura")

    chamada = api_temperatura + id_cidade + "/estendida.xml"
    retorno = req.get(chamada)
    xml_root = ET.fromstring(retorno.content)
    previsoes = xml_root.findall('previsao')

    list_previsoes = []
    for previsao in previsoes:
        dia = previsao.find("dia").text
        maxima = int(previsao.find("maxima").text)
        minima = int(previsao.find("minima").text)
        obj_previsao = PrevisaoTempoModel(dia, maxima, minima)
        list_previsoes.append(obj_previsao)

    return list_previsoes