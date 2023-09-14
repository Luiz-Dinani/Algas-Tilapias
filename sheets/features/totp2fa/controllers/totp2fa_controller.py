from flask import request, jsonify
from flask_restx import Resource
from features.totp2fa.services import totp2fa_service
from features.totp2fa.models.Request2FAModel import request_codigo_2FA_resource
from app import api

ns = api.namespace('2FA', description='Operações de 2FA')
@ns.route("/<int:id_usuario>")
class Login2faResource(Resource):
    def get(self, id_usuario):
        uri = totp2fa_service.gerarUriOtp(id_usuario)
        if uri is not None:
            return uri, 200
        return "", 404
    @api.expect(request_codigo_2FA_resource)
    def post(self, id_usuario):
        data = request.get_json()
        if data is None or data.get("codigo_inserido") is None:
            return "Código é obrigatório", 400

        codigo_inserido = data.get("codigo_inserido")
        isValido = totp2fa_service.validar_2FA(codigo_inserido, id_usuario)

        if isValido:
            return "", 204
        return "Código Errado", 400

    def patch(self, id_usuario):
        atualizado = totp2fa_service.atualizarAutenticacao(id_usuario)
        if atualizado:
            return "", 204
        return "", 404