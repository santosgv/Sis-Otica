# Generated by Django 4.1.3 on 2022-12-28 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Unidades', '0002_delete_comissao_delete_ordem_servico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='DATA_NASCIMENTO',
            field=models.DateField(blank=True, null=True),
        ),
    ]
