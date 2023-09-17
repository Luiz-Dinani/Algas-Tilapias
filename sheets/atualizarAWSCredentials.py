import json
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

nome_arquivo = "appsettings.json"

with open(nome_arquivo, "w") as arquivo_json:
    #substitui o conteúdo do appsettings.json pelas novas credenciais
    json.dump(credenciais, arquivo_json, indent=4)

print("Conteúdo do arquivo appsettings.json foi atualizado com sucesso!")