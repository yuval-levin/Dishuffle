# Generated by Django 2.2.15 on 2020-10-02 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_account_unwanted_dishes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='unwanted_dishes',
        ),
        migrations.DeleteModel(
            name='Dish',
        ),
    ]