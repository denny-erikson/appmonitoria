# Generated by Django 5.1.2 on 2024-11-06 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0014_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('PENDING', 'Pending'), ('CANCELED', 'Canceled')], default='PENDING', max_length=10),
        ),
    ]