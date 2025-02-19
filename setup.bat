@echo off

REM Criar ambiente virtual
python -m venv venv

REM Ativar o ambiente virtual
call venv\Scripts\activate.bat

REM Atualizar pip
python -m pip install --upgrade pip

REM Instalar dependências
pip install -r requirements.txt

REM Criar e aplicar migrações
python manage.py migrate

REM Criar superusuário
python manage.py createsuperuser

pause
