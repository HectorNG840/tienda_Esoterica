# Generated by Django 5.1.3 on 2024-12-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiendaEsoterica', '0011_alter_pedido_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]