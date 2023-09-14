from flask import request, jsonify
from flask_restx import Resource
from features.login.services import login_service
from features.login.models.RequestLoginModel import request_login_resource, RequestLoginModel
from app import api

ns = api.namespace('login', description='Operações de login')

@ns.route("/")
class LoginResource(Resource):
    @api.expect(request_login_resource)
    def post(self):
        data = request.get_json()
        email, senha = data.get("email"), data.get("senha")
        if data is None or email is None or senha is None:
            return jsonify({"erro": "Campos de email e senha são obrigatórios"}), 400

        login_model = RequestLoginModel(email, senha)
        resultado = login_service.login(login_model)
        if resultado is not None:
            return resultado.__dict__, 200
        else:
            return "", 404

