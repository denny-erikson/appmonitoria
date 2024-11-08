# Generated by Django 5.1.2 on 2024-10-29 00:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0005_remove_uniform_size_remove_uniform_uniform_type_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.AddField(
            model_name='payment',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoria.event'),
        ),
        migrations.AddField(
            model_name='payment',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
