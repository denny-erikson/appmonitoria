#!/bin/bash

# Ativar o ambiente virtual
source venv/bin/activate  # Para Linux/Mac
# .\venv\Scripts\activate  # Descomente esta linha se estiver usando Windows

# Instalar dependências
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

# Rodar a aplicação Django
python manage.py runserver
