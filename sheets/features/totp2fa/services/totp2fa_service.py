import hashlib
import pyotp
import json
import base64
import boto3
import qrcode
import io
from botocore.exceptions import ClientError
import dbcontext.samaka_db_context as _context

def obterKeyBase2FA():
    secret_name = "dev/login/2FA"
    region_name = "us-east-1"

    session = boto3.session.Session()
    with open('appsetings.json', 'r') as arquivo_json:
        appsettings = json.load(arquivo_json)
        credenciais = appsettings["credenciais-aws"]

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=credenciais["aws_access_key_id"],
        aws_secret_access_key=credenciais["aws_secret_access_key"],
        aws_session_token=credenciais["aws_session_token"]
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    jsonObject = json.loads(secret)
    return jsonObject["SamakaChaveBase2FA"]

def obterHashedKey(emailCliente):
    key = (obterKeyBase2FA() + emailCliente)
    hashed_key = hashlib.sha256(key.encode()).hexdigest()
    b32_hashed_key = base64.b32encode(bytes.fromhex(hashed_key)).decode("utf-8")
    return b32_hashed_key

def gerarUriOtp(idFuncionario):
    nomeCliente, emailCliente = _context.obterNomeEmailByIdFuncionario(idFuncionario)
    nomeCliente = nomeCliente.split()
    nomeCliente = nomeCliente[0]
    key = obterHashedKey(emailCliente)
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=nomeCliente, issuer_name="Samaka")
    #qrcode.make(uri).save("qrCode.png")
    return uri
#
# def obterQrCode(idFuncionario):
#     from PIL import Image
#     uri = gerarUriOtp(idFuncionario)
#     qr = qrcode.QRCode()
#     qr.make(uri)
#     img = qr.make_image()
#     buffer = io.BytesIO()
#     img.save(buffer, "PNG")
#     base64_image = base64.b64encode(buffer.getvalue()).decode()
#
#     return base64_image

def validar_2FA(codigoInserido, idFuncionario):
    emailCliente = _context.obterEmailByIdFuncionario(idFuncionario)
    key = obterHashedKey(emailCliente)
    isValido = pyotp.totp.TOTP(key).verify(codigoInserido)
    return isValido


def atualizarAutenticacao(id_usuario):
    retorno = _context.atualizarAutenticacao(id_usuario)
    return retorno