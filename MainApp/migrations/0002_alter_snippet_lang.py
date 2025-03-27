# Generated by Django 5.1.7 on 2025-03-27 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='lang',
            field=models.CharField(choices=[('py', 'Python'), ('js', 'Java'), ('cpp', 'C++'), ('html', 'HTML')], max_length=30),
        ),
    ]
