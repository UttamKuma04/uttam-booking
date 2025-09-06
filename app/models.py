from django.db import models
from django.contrib.auth.models import User

class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    travel_id = models.AutoField(primary_key=True)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPES, default='flight')
    source = models.CharField(max_length=100, default="Unknown")
    destination = models.CharField(max_length=100, default="Unknown")
    travel_datetime = models.DateTimeField(null=True, blank=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    available_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.get_travel_type_display()} {self.source} → {self.destination}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ safe for migrations
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, null=True, blank=True)
    number_of_seats = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    booking_date = models.DateTimeField(auto_now_add=True)  # ✅ auto filled
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')

    def save(self, *args, **kwargs):
        if self.travel_option:
            self.total_price = self.travel_option.price * self.number_of_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username if self.user else 'Guest'} ({self.status})"

