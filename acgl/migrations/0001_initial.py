# Generated by Django 5.1.6 on 2025-02-18 07:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendorDetails',
            fields=[
                ('vendor_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(blank=True, max_length=100)),
                ('business_since', models.DateField(blank=True, null=True)),
                ('nature_of_services', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('Service', 'Service'), ('Material', 'Material'), ('Both', 'Both')], default='Service', max_length=10)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('pin_code', models.CharField(blank=True, max_length=20)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('bank_name', models.CharField(blank=True, max_length=100)),
                ('branch', models.CharField(blank=True, max_length=100)),
                ('account_number', models.CharField(blank=True, max_length=50)),
                ('ifsc_code', models.CharField(blank=True, max_length=20)),
                ('account_type', models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current')], default='Savings', max_length=10)),
                ('pan_doc', models.FileField(blank=True, null=True, upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])),
                ('aadhar_doc', models.FileField(blank=True, null=True, upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])),
                ('gst_doc', models.FileField(blank=True, null=True, upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])),
                ('bank_doc', models.FileField(blank=True, null=True, upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])])),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
