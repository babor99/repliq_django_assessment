# Generated by Django 3.2.16 on 2023-01-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='some', max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
