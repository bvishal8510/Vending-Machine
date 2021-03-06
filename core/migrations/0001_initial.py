# Generated by Django 3.0.5 on 2020-04-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_coin', models.PositiveIntegerField(default=0)),
                ('u_penny', models.PositiveIntegerField(default=0)),
                ('u_nickel', models.PositiveIntegerField(default=0)),
                ('u_quater', models.PositiveIntegerField(default=0)),
                ('u_total_sum', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VendingItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coke_price', models.PositiveIntegerField(default=25)),
                ('pepsi_price', models.PositiveIntegerField(default=35)),
                ('soda_price', models.PositiveIntegerField(default=45)),
                ('coke_quantity', models.PositiveIntegerField(default=0)),
                ('pepsi_quantity', models.PositiveIntegerField(default=0)),
                ('soda_quantity', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VendingMachineMoney',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_coin', models.PositiveIntegerField(default=0)),
                ('m_penny', models.PositiveIntegerField(default=0)),
                ('m_nickel', models.PositiveIntegerField(default=0)),
                ('m_quater', models.PositiveIntegerField(default=0)),
                ('m_total_sum', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
