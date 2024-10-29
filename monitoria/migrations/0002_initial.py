# Generated by Django 5.1.2 on 2024-10-28 00:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitoria', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='availability',
            name='cancellation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoria.cancellation'),
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='monitoria.location'),
        ),
        migrations.AddField(
            model_name='product',
            name='events',
            field=models.ManyToManyField(related_name='products', to='monitoria.event'),
        ),
        migrations.AddField(
            model_name='resort',
            name='availability',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoria.availability'),
        ),
        migrations.AddField(
            model_name='team',
            name='payments',
            field=models.ManyToManyField(related_name='teams', to='monitoria.payment'),
        ),
        migrations.AddField(
            model_name='team',
            name='resort',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='monitoria.resort'),
        ),
        migrations.AddField(
            model_name='event',
            name='teams',
            field=models.ManyToManyField(related_name='events', to='monitoria.team'),
        ),
        migrations.AddField(
            model_name='uniform',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]