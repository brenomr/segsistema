# Generated by Django 2.2.7 on 2019-11-21 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0003_auto_20191114_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acessoexterno',
            name='veiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.Veiculo'),
        ),
        migrations.AlterField(
            model_name='acessoexterno',
            name='visitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.Visitante'),
        ),
    ]
