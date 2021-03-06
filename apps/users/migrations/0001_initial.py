# Generated by Django 4.0.4 on 2022-06-18 13:03

import apps.users.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True, db_index=True)),
                ('first_name', models.CharField(blank=True, max_length=32, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=32, null=True)),
                ('username', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True)),
                ('pan', models.CharField(blank=True, max_length=10, null=True)),
                ('aadhar', models.CharField(blank=True, max_length=16, null=True)),
                ('father_name', models.CharField(blank=True, max_length=128, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=128, null=True)),
                ('spouse_name', models.CharField(blank=True, max_length=128, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('mpin', models.CharField(blank=True, max_length=4, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('is_mobile_verified', models.BooleanField(default=False)),
                ('is_aadhaar_verified', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True, db_index=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('phone_no', models.BigIntegerField(blank=True, null=True)),
                ('otp', models.PositiveIntegerField(default=apps.users.models.random_otp)),
                ('expiry_datetime', models.DateTimeField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user otp',
                'verbose_name_plural': 'users otp',
            },
        ),
    ]
