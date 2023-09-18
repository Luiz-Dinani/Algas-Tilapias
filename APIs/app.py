from flask import Flask
from flask_restx import Api, Resource
from configureApp import configure_app

app = Flask(__name__)
configure_app(app)
api = Api(app, version='1.0', title='API de Autenticação e Planilha', description='API para autenticação de usuários e operações em planilhas', doc='/doc/')

from features.login.controllers.login_controller import LoginResource
from features.planilha.controllers.planilha_controller import PlanilhaResource
from features.totp2fa.controllers.totp2fa_controller import Login2faResource

@api.route("/")
class Boot(Resource):
    def get(self):
        return {"message": "Bem-vindo à API de autenticação e planilha"}

api.add_resource(LoginResource, '/login')
api.add_resource(Login2faResource, '/2fa')

api.add_resource(PlanilhaResource, '/planilha')

if __name__ == '__main__':
    app.run(debug=True)
