import hashlib
from features.login.models.RequestLoginModel import RequestLoginModel
import dbcontext.samaka_db_context as _context
def hash_password(password):
    hash_object = hashlib.sha256()
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()

def login(login_model: RequestLoginModel):
    login_model.senha = hashlib.sha256(login_model.senha)
    return _context.login(login_model)

def coletarDadosPlanilha(idCliente):
    resultado = _context.coletaDados(idCliente)

    return resultado