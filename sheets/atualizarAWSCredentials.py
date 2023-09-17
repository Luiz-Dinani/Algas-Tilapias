import sys
import json

def main():
    print("NÃO PRECISA FAZER COMMIT DO APPSETTINGS, APENAS ENTRE NA EC2 E RODE O SCRIPT gerarDocker.sh")

    atualizar = ""
    while atualizar.upper() not in ("S", "N"):
        atualizar = input("Atualizar Credenciais da AWS? (S/N): ")
    if atualizar.upper() == "N":
        return

    aws_access_key_id = input("Insira a aws_access_key_id: ")
    aws_secret_access_key = input("Insira a aws_secret_access_key: ")
    aws_session_token = input("Insira a aws_session_token: ")

    credenciais = {
        "credenciais-aws": {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token
        }
    }
    
    with open("appsettings.json", "w") as arquivo_json:
        #substitui o conteúdo do appsettings.json pelas novas credenciais
        json.dump(credenciais, arquivo_json, indent=4)
    print("Conteúdo do arquivo appsettings.json foi atualizado com sucesso!")

main()