# Generated by Django 4.2.14 on 2024-07-26 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]