# Generated by Django 3.2.8 on 2021-10-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20211019_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='starttime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]