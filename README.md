# Sis-Otica
Repositório para o Projeto SIS ótica !

# Este projeto foi feito com:

* Python 3.10.4
* Django 4.1.3
* Pillow 9.3.0
* python-decouple 3.6

# Como rodar o projeto?

# Criaçao das Tabelas caso nao Suba no migrations

CREATE TABLE Autenticacao_comissao (
    id INTEGER NOT NULL PRIMARY KEY,
    colaborador_id INTEGER, 
    valor_vendas FLOAT,
    data_referencia DATE,
    horas_extras FLOAT,
    FOREIGN KEY (colaborador_id) REFERENCES Autenticacao_USUARIO(ID)
);

CREATE TABLE Autenticacao_desconto (
    id INTEGER NOT NULL PRIMARY KEY,
    colaborador_id INTEGER,
    tipo VARCHAR(100), 
    percentual FLOAT,
    FOREIGN KEY (colaborador_id) REFERENCES Autenticacao_USUARIO(ID)
);

DROP TABLE Autenticacao_desconto ;


DROP TABLE Autenticacao_comissao ;

~~~linux
git clone https://github.com/santosgv/Sis-Otica.git
cd Sis-Otica
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py makemigrations Cliente
python manage.py migrate_schemas
python manage.py createsuperuser #cria o superusuario
python manage.py create_tenant_superuser #cria o superusuario do tennant
python manage.py runserver
