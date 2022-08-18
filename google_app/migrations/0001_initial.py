# Generated by Django 3.2.5 on 2022-08-18 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='number')),
                ('order_number', models.IntegerField(db_index=True, unique=True, verbose_name='Order number')),
                ('price_dollars', models.IntegerField(verbose_name='Price in Dollars')),
                ('price_rubles', models.IntegerField(verbose_name='Price in Rubles')),
                ('delivery_time', models.CharField(max_length=10, verbose_name='End time to delivery order')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]