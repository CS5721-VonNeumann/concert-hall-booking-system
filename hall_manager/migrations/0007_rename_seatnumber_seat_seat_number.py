# Generated by Django 5.1.2 on 2024-11-12 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hall_manager", "0006_alter_hall_slot_alter_hall_venue"),
    ]

    operations = [
        migrations.RenameField(
            model_name="seat",
            old_name="seatNumber",
            new_name="seat_number",
        ),
    ]