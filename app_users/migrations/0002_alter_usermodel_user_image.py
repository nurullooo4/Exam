# Generated by Django 5.1.3 on 2024-11-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_image',
            field=models.ImageField(blank=True, default='user-images/user-default.png', null=True, upload_to='user-images/'),
        ),
    ]
