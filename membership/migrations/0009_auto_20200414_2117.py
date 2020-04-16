# Generated by Django 2.2.12 on 2020-04-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0008_auto_20200414_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipplans',
            name='type',
            field=models.IntegerField(choices=[(30, '1 month'), (90, '3 month'), (180, '6 month'), (360, '1 year')], default=30),
        ),
    ]