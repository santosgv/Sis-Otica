# Sis-Otica
Repositório para o Projeto SIS ótica !

# Este projeto foi feito com:

* Python 3.10.4
* Django 4.1.3
* Pillow 9.3.0
* python-decouple 3.6

# Como rodar o projeto?


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
