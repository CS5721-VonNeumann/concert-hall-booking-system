# Generated by Django 5.1.2 on 2024-11-24 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_showproducer_organisation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="showproducer",
            name="organisation",
            field=models.CharField(default="", max_length=30),
        ),
    ]
