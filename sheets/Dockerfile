# Use uma imagem base Python
FROM python:3.8-slim-buster

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copie o código da aplicação para o contêiner
COPY . .

# Exponha as portas em que a aplicação Flask está sendo executada (por padrão, porta 5000)
EXPOSE 5000
EXPOSE 8080

# Comando para iniciar a aplicação quando o contêiner for iniciado
CMD ["python3", "-m", "flask", "run", "-h" "0.0.0.0" "-p" "8080"]
