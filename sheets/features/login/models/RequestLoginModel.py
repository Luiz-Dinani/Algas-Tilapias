from app import api
from flask_restx import fields

request_login_resource = api.model("reqLoginModel", {
    "email": fields.String(required=True, description='O email do usuário'),
    "senha": fields.String(required=True, description='A senha do usuário')
})

class RequestLoginModel:
    def __init__(self, email: str, senha: str):
        self.email = email
        self.senha = senha