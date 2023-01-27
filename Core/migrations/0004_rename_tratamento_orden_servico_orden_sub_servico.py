# Generated by Django 4.1.3 on 2023-01-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_servico_alter_orden_forma_pag_sub_servico'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orden',
            old_name='TRATAMENTO',
            new_name='SERVICO',
        ),
        migrations.AddField(
            model_name='orden',
            name='SUB_SERVICO',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]