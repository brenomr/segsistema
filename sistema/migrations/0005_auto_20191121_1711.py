# Generated by Django 2.2.7 on 2019-11-21 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0004_auto_20191121_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acessointerno',
            name='morador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.Morador'),
        ),
    ]
