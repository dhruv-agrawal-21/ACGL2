# Generated by Django 5.1.6 on 2025-02-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acgl', '0002_vendordetails_email_vendordetails_phonenumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=255)),
                ('phonenumber', models.CharField(max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('password_hash', models.CharField(max_length=255)),
            ],
        ),
    ]
