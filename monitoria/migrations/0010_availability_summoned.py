# Generated by Django 5.1.2 on 2024-11-03 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0009_remove_availability_cancellation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='summoned',
            field=models.BooleanField(default=False),
        ),
    ]