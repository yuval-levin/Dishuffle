# Generated by Django 2.2.15 on 2020-10-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='unwanted_dishes',
            field=models.ManyToManyField(to='catalog.Dish'),
        ),
    ]
