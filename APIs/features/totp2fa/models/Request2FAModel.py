from app import api
from flask_restx import fields

request_codigo_2FA_resource = api.model("2faModel", {
    "codigo_inserido": fields.String(required=True, description='O codigo 2FA inserido pelo usuário'),
})

class Request2FAModel:
    def __init__(self, codigo_inserido):
        self.codigo_inserido = codigo_inserido