# Generated by Django 5.1.2 on 2024-11-09 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='show',
            name='category',
            field=models.CharField(choices=[('LIVE_PERFORMANCE', 'LIVE_PERFORMANCE'), ('MOVIE_SCREENING', 'MOVIE_SCREENING'), ('CONFERENCE', 'CONFERENCE')], default='LIVE_PERFORMANCE', max_length=20),
        ),
        migrations.AlterField(
            model_name='show',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('SCHEDULED', 'SCHEDULED'), ('COMPLETED', 'COMPLETED'), ('REJECTED', 'REJECTED'), ('CANCELLED', 'CANCELLED')], default='PENDING', max_length=10),
        ),
    ]
