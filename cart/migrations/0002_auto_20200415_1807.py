# Generated by Django 2.2.12 on 2020-04-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=10, default=0, max_digits=10),
        ),
    ]
