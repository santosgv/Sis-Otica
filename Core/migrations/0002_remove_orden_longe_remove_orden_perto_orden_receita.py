# Generated by Django 4.1.3 on 2023-01-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='LONGE',
        ),
        migrations.RemoveField(
            model_name='orden',
            name='PERTO',
        ),
        migrations.AddField(
            model_name='orden',
            name='RECEITA',
            field=models.TextField(default=1, max_length=2000),
            preserve_default=False,
        ),
    ]
