# Generated by Django 5.1.2 on 2024-11-03 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0010_availability_summoned'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='cancellation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='availabilities', to='monitoria.cancellation'),
        ),
    ]