# Generated by Django 2.2.15 on 2020-09-24 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200924_1415'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='USERNAME_FIELD',
        ),
    ]
