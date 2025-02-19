# Use uma imagem base oficial do Python 3.10
FROM python:3.10-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do projeto para o contêiner
COPY . .

# Exponha a porta que o Django usará
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]