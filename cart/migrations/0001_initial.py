# Generated by Django 2.2.12 on 2020-04-15 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('content', '0002_auto_20200414_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=10, max_digits=10)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='users.CustomerUser')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=10, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.Cart')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='content.File', unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Product', unique=True)),
            ],
            options={
                'unique_together': {('cart', 'product', 'file')},
            },
        ),
    ]
