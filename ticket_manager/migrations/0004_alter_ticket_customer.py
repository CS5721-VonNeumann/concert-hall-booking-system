# Generated by Django 5.1.2 on 2024-12-06 12:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_manager', '0003_ticket_created_at_ticket_price_ticket_updated_at'),
        ('users', '0003_alter_showproducer_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='users.customer'),
        ),
    ]
