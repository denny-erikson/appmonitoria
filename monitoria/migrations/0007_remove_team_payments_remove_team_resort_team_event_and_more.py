# Generated by Django 5.1.2 on 2024-10-29 01:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0006_remove_payment_date_payment_event_payment_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='payments',
        ),
        migrations.RemoveField(
            model_name='team',
            name='resort',
        ),
        migrations.AddField(
            model_name='team',
            name='event',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoria.event'),
        ),
        migrations.AddField(
            model_name='team',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
