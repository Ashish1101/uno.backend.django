# Generated by Django 4.0.4 on 2022-06-18 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_pan_kyc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kyc',
            name='user',
        ),
    ]
