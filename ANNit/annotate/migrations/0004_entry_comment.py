# Generated by Django 3.0.3 on 2020-06-22 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0003_auto_20200621_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='comment',
            field=models.CharField(default='Unknown', max_length=400),
        ),
    ]
