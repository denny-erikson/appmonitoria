# Generated by Django 5.1.2 on 2024-10-29 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoria', '0004_remove_document_documents_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uniform',
            name='size',
        ),
        migrations.RemoveField(
            model_name='uniform',
            name='uniform_type',
        ),
        migrations.AddField(
            model_name='uniform',
            name='festival_shirt_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select festival shirt size', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='uniform',
            name='jacket_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select jacket size', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='uniform',
            name='pants_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select pants size', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='uniform',
            name='party_uniform_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select party uniform size', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='uniform',
            name='shorts_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select shorts size', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='uniform',
            name='t_shirt_size',
            field=models.CharField(blank=True, choices=[('P', 'Pequeno'), ('M', 'Médio'), ('G', 'Grande'), ('GG', 'Extra Grande')], help_text='Select t-shirt size', max_length=2, null=True),
        ),
    ]