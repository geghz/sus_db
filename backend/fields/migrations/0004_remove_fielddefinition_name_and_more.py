# Generated by Django 4.2.6 on 2025-05-02 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_remove_employee_hired_at_remove_employee_manager_and_more'),
        ('fields', '0003_fielddefinitionvalue_delete_employeefieldvalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fielddefinition',
            name='name',
        ),
        migrations.RemoveField(
            model_name='fielddefinition',
            name='required',
        ),
        migrations.RemoveField(
            model_name='fieldgroup',
            name='code',
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='label',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinition',
            name='options',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinitionvalue',
            name='definition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='values', to='fields.fielddefinition'),
        ),
        migrations.AddField(
            model_name='fielddefinitionvalue',
            name='value_file',
            field=models.FileField(blank=True, null=True, upload_to='fields/'),
        ),
        migrations.AddField(
            model_name='fielddefinitionvalue',
            name='value_list',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinitionvalue',
            name='value_number',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='fielddefinitionvalue',
            name='value_select',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='fielddefinition',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('multiline', 'Multiline'), ('number', 'Number'), ('date', 'Date'), ('file', 'File'), ('select', 'Select'), ('multiselect', 'MultiSelect'), ('boolean', 'Boolean'), ('email', 'Email'), ('url', 'URL'), ('phone', 'Phone'), ('currency', 'Currency')], max_length=20),
        ),
        migrations.AlterField(
            model_name='fielddefinitionvalue',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_fields', to='employees.employee'),
        ),
        migrations.AlterField(
            model_name='fieldgroup',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='fielddefinitionvalue',
            unique_together={('employee', 'definition')},
        ),
        migrations.RemoveField(
            model_name='fielddefinitionvalue',
            name='field_definition',
        ),
    ]
