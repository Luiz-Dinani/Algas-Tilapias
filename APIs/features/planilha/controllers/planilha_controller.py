from flask import jsonify
from flask_restx import Resource
from features.planilha.services import planilha_service
from app import api

ns = api.namespace('planilha', description='Operações de Planilha')

@ns.route("/<int:id_usuario>")
class PlanilhaResource(Resource):
    def get(self, id_usuario):
        resultado = planilha_service.coletarDadosPlanilha(id_usuario)
        if len(resultado) > 0:
            return resultado, 200
        else:
            return '', 404