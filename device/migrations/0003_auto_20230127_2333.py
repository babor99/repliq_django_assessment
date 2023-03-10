# Generated by Django 3.2.16 on 2023-01-27 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('device', '0002_auto_20230127_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceassign',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_device_assigns', to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devicelog',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_device_logs', to='authentication.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='devicereturn',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_device_returns', to='authentication.user'),
            preserve_default=False,
        ),
    ]
