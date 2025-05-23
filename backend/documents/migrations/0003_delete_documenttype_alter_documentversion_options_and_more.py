# Generated by Django 4.2.6 on 2025-05-02 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0003_fielddefinitionvalue_delete_employeefieldvalue'),
        ('documents', '0002_documenttype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentType',
        ),
        migrations.AlterModelOptions(
            name='documentversion',
            options={'ordering': ['-uploaded_at']},
        ),
        migrations.RemoveField(
            model_name='document',
            name='name',
        ),
        migrations.AddField(
            model_name='document',
            name='field_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='fields.fieldgroup'),
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(upload_to='documents/', verbose_name='Скан документа'),
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер версии'),
        ),
    ]
