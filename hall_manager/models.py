from django.db import models
from config.constants import ShowCategory

class Slot(models.Model):
    TIMING_CHOICES = [
        ('MORNING', 'MORNING'),
        ('NOON', 'NOON'),
        ('EVENING', 'EVENING'),
        ('NIGHT', 'NIGHT'),
    ]
    date = models.DateField()
    timing = models.CharField(max_length=10, choices=TIMING_CHOICES)

class Venue(models.Model):
    venue_name = models.CharField(max_length=30)
    location = models.TextField()
    phone_number = models.CharField(max_length=10)

class Hall(models.Model):
    hall_name = models.CharField(max_length=30)
    hall_capacity = models.IntegerField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True,related_name="halls")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True, related_name='halls')

    # create seats based on hall capacity
    def save(self, *args, **kwargs):
        has_existing_hall = self.pk is None
        super().save(*args, **kwargs)

        if has_existing_hall:
            Seat.objects.bulk_create([
                Seat(seat_number=i + 1, hall=self) for i in range(self.hall_capacity)
            ])

class HallSupportsCategory(models.Model):
    CATEGORY_CHOICES = [(category.name, category.name) for category in ShowCategory]
    show_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default= ShowCategory.LIVE_PERFORMANCE.name)

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True,related_name="hallSupportsCategories")

class HallSupportsSlot(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="hallSupportsSlots")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="hallSupportsSlots")

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")