from django.db import models

class Slot(models.Model):
    TIMING_CHOICES = [
        ('MORNING', 'MORNING'),
        ('NOON', 'NOON'),
        ('EVENING', 'EVENING'),
        ('NIGHT', 'NIGHT'),
    ]
    date = models.DateField()
    timing = models.CharField(max_length=10, choices=TIMING_CHOICES)

class Category(models.Model):
    category_name = models.CharField(max_length=20)

class Venue(models.Model):
    venue_name = models.CharField(max_length=30)
    location = models.TextField()
    phone_number = models.CharField(max_length=10)

class Hall(models.Model):
    hall_name = models.CharField(max_length=30)
    hall_capacity = models.IntegerField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True,related_name="halls")

    # create seats based on hall capacity
    def save(self, *args, **kwargs):
        has_existing_hall = self.pk is None
        super().save(*args, **kwargs)

        if has_existing_hall:
            Seat.objects.bulk_create([
                Seat(seat_number=i + 1, hall=self) for i in range(self.hall_capacity)
            ])
    
    # check if the hall supports a given show category
    def supports_category(self, category):
        return HallSupportsCategory.objects.filter(hall=self, category=category).exists()

    # check if the slot exists for the hall
    def supports_slot(self, slot):
        return HallSupportsSlot.objects.filter(hall=self, slot=slot).exists()

    # fetch all halls that supports given category and slot
    def get_halls_by_category_and_slot(self, category, slot):
        halls_with_category = HallSupportsCategory.objects.filter(category=category).values_list('hall_id', flat=True)
        halls_with_slot = HallSupportsSlot.objects.filter(slot=slot).values_list('hall_id', flat=True)

        return

class HallSupportsCategory(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True,related_name="hall_supports_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name="hall_supports_categories")

class HallSupportsSlot(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, related_name="hall_supports_slots")
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True, related_name="hall_supports_slots")

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, related_name="seats")