
def main():
    Faker.seed(0)
    fake = Faker()
    clientes = CLIENTE.objects.all()
    dbservicoes = SERVICO.objects.all()
    start_date = date(2023, 1, 1)
    end_date = date(2023, 12, 31)
  #  for _ in range(50):
  #      pessoa=CLIENTE.objects.create(
  #          NOME=fake.name(),
  #          LOGRADOURO=fake.street_address(),
  #          NUMERO=fake.building_number(),
  #          BAIRRO=fake.country(),
  #          CIDADE=fake.city(),
  #          TELEFONE=fake.numerify(text='########'),
  #          CPF=fake.numerify(text='###########'),
  #          DATA_NASCIMENTO=fake.date_of_birth(),
  #          EMAIL=fake.email(),
  #          DATA_CADASTRO=fake.date_between(start_date=start_date, end_date=end_date)

   #     )
   #     print(f'A pessoal {pessoa.NOME} foi criada')

    for _ in range(100):
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        cliente = random.choice(clientes)
        valor_com_dolar= fake.pricetag()
        valor_sem_dolar = valor_com_dolar.replace("$", "")
        valor_float = float(valor_sem_dolar.replace(',', '').replace('.', '', 1))
        os = ORDEN.objects.create(
            VENDEDOR=USUARIO.objects.get(id=5),
            CLIENTE=cliente,
            PREVISAO_ENTREGA=fake.date_between(start_date=start_date, end_date=end_date),
            DATA_SOLICITACAO=fake.date_between(start_date=start_date, end_date=end_date),
            SERVICO=SERVICO.objects.get(id=2),
            OBSERVACAO=fake.sentence(nb_words=15),
            QUANTIDADE_PARCELA = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']),
            FORMA_PAG=random.choice(['A', 'B', 'C', 'D', 'E', 'F']),
            VALOR=valor_float,
            STATUS=random.choice(['A', 'E', 'C', 'L', 'J']),
            ENTRADA=fake.pricetag(),
        )
        print(f'os {os.id} criada')

    for _ in range(50):
        valor_com_dolar= fake.pricetag()
        valor_sem_dolar = valor_com_dolar.replace("$", "")
        valor_float = valor_sem_dolar.replace('.', '').replace(',', '.')
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)
        caixa = CAIXA.objects.create(
            DATA=fake.date_between(start_date=start_date, end_date=end_date),
            DESCRICAO=fake.sentence(nb_words=15),
            TIPO=random.choice(['E', 'S']),
            VALOR=valor_float,
            FORMA=random.choice(['A', 'B', 'C', 'D', 'E', 'F']),
            FECHADO=random.choice([True,False])
        )
        print(f'Caixa criado {caixa} data {caixa.TIPO}')


if __name__ == '__main__':
    import os
    import random
    from django.core.wsgi import get_wsgi_application
 
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sis.settings')
    application = get_wsgi_application()
    from Core.models import CLIENTE, ORDEN,CAIXA,SERVICO
    from Autenticacao.models import USUARIO
    from faker import Faker
    from datetime import date

    main()
