# Generated by Django 5.1.3 on 2024-11-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="showproducer",
            name="organisation",
            field=models.CharField(default="", max_length=100),
        ),
    ]