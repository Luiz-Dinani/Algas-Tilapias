from flask import Flask, request, jsonify
import features.login.services.login_service as _login_service
from features.login.models.RequestLoginModel import RequestLoginModel
from Google_sheets import gerarPlanilha as gp

app = Flask(__name__)
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["email"] is None or data["senha"] is None:
        return jsonify({"erro": "Campos de email e senha são obrigatórios"}), 400

    login_model = RequestLoginModel(data["email"], data["senha"])

    resultado = _login_service.login(login_model)
    if len(resultado) > 0:
        return resultado, 200
    else:
        return '', 404
    # if resultado[0][0]>0:
    #     return "A"
    # else:
    #     resultado = coletaDados(f"select count(*), funcao from funcionario where email = '{email}' and senha = '{senha}';")
    #     if resultado[0][0]>0:
    #         return resultado[0][1]
    #     else:
    #         return 'erro'
        
#
# funcao('atacado_peixe@atacado.com','atacado_peixe')

@app.route("/planilha/<idCliente>")
def obterPlanilha(idCliente):
    resultado = _login_service.coletarDadosPlanilha(idCliente)
    return gp(resultado.empresa[0], 'A', resultado.drop(columns=['empresa', 'idMonitoracaoCiclo']))