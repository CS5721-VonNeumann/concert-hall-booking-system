# Generated by Django 5.1.2 on 2024-11-24 00:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_rename_membershipcode_customermembership_membership_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customermembership',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]