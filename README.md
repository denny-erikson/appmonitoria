# MVP App Monitoria

Este é um projeto Django para monitoria de usuários, configurado para rodar em um ambiente Docker.

## Pré-requisitos

- Docker
- Docker Compose

## Configuração do Ambiente de Desenvolvimento

### Passo 1: Construir os Contêineres

Construa os contêineres Docker:

```bash
docker-compose up --build
```


### Passo 2: Aplicar Migrações

Aplique as migrações do banco de dados:

```bash
 docker-compose exec web python manage.py migrate
```


### Passo 3: Criar Superusuário

Crie um superusuário para acessar o admin do Django:

```bash
docker-compose exec web python manage.py createsuperuser
```


### Passo 4: Popular o Banco de Dados com Usuários Falsos

Popule o banco de dados com usuários falsos:

```bash
docker-compose exec web python populate.py
```


### Passo 5: Acessar a Aplicação

Acesse a aplicação no navegador:

[http://localhost:8000/admin](vscode-file://vscode-app/c:/Users/Usu%C3%A1rio/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

## Scripts de Configuração

### Script para Linux/Mac: [run_django.sh](vscode-file://vscode-app/c:/Users/Usu%C3%A1rio/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

Este script configura o ambiente virtual, instala as dependências, aplica as migrações e cria um superusuário.

```bash
#!/bin/bash
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate  # Para Linux/Mac

# Instalar dependências
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

# Rodar a aplicação Django
python manage.py runserver
```


### Script para Windows: [setup.bat](vscode-file://vscode-app/c:/Users/Usu%C3%A1rio/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

Este script configura o ambiente virtual, instala as dependências, aplica as migrações, cria um superusuário e popula o banco de dados.

```bash
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

REM Rodar o script de popular o banco
python populate.py

pause
```


## Notas Adicionais

* Certifique-se de que o Docker e o Docker Compose estão instalados e funcionando corretamente no seu sistema.
* Para parar os contêineres, use `docker-compose down`.

## Contato

Para mais informações, entre em contato com o desenvolvedores do projeto

- Amin Moraes
- Cauê Morais
- Denny Erikson
