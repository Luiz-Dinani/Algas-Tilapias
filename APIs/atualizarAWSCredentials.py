import sys
import json

def main():
    print("NÃO PRECISA FAZER COMMIT DO APPSETTINGS, APENAS ENTRE NA EC2 E RODE O SCRIPT gerarDocker.sh")

    atualizar = ""
    while atualizar.upper() not in ("S", "N"):
        atualizar = input("Atualizar Credenciais da AWS? (S/N): ")
    if atualizar.upper() == "N":
        return

    aws_cli = ""

    while True:
        user_input = input("Insira TODO o conteúdo do AWS_CLI: ")

        if user_input.endswith("="):
            aws_cli += user_input
            break
        
        aws_cli += user_input

    aws_cli = aws_cli.replace("[default]", "")
    aws_cli = aws_cli.replace("aws_access_key_id=", " ")
    aws_cli = aws_cli.replace("aws_secret_access_key=", " ")
    aws_cli = aws_cli.replace("aws_session_token=", " ")
    aws_cli = aws_cli.split()
  
    aws_access_key_id, aws_secret_access_key, aws_session_token = aws_cli[0], aws_cli[1], aws_cli[2]
     
    credenciais = {
        "credenciais-aws": {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "aws_session_token": aws_session_token
        }
    }
    
    with open("appsettings.json", "r") as arquivo_json:
        #substitui o conteúdo do appsettings.json pelas novas credenciais
        appSettings = json.load(arquivo_json)
        appSettings["credenciais-aws"] = credenciais
        json.dump(appSettings, arquivo_json, indent=4)
    print("Conteúdo do arquivo appsettings.json foi atualizado com sucesso!")

main()