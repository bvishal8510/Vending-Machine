# Generated by Django 3.0.5 on 2020-04-23 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermoney',
            name='u_coin',
        ),
        migrations.RemoveField(
            model_name='usermoney',
            name='u_total_sum',
        ),
        migrations.RemoveField(
            model_name='vendingmachinemoney',
            name='m_coin',
        ),
        migrations.RemoveField(
            model_name='vendingmachinemoney',
            name='m_total_sum',
        ),
    ]
