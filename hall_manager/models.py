from django.db import models

class Hall(models.Model):
    hall_name = models.CharField(max_length=30)
    hall_capacity = models.IntegerField()

    def save(self, *args, **kwargs):
        # Check if this is a new instance (no primary key assigned yet)
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save the Hall instance first

        if is_new:
            # Create seats based on hall_capacity
            Seat.objects.bulk_create([
                Seat(seatNumber=i + 1, hall=self) for i in range(self.hall_capacity)
            ])

class Seat(models.Model):
    seatNumber = models.PositiveIntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")