# Generated by Django 3.0.3 on 2020-06-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0005_auto_20200622_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(default='Unknown', max_length=200),
        ),
        migrations.AlterField(
            model_name='entry',
            name='comment',
            field=models.CharField(default='Unknown', max_length=400),
        ),
        migrations.AlterField(
            model_name='entry',
            name='user_choice',
            field=models.CharField(default='Unknown', max_length=200),
        ),
    ]