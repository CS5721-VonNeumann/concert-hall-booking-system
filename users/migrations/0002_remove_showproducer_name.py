# Generated by Django 5.1.2 on 2024-11-09 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="showproducer",
            name="name",
        ),
    ]