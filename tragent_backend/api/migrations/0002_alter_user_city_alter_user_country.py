# Generated by Django 4.1.7 on 2024-03-20 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=64),
        ),
    ]
