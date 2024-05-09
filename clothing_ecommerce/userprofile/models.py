from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.utils import timezone

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    # products/models.py

class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    ACTIVE = 'active'
    DELETED = 'deleted'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.name

    def get_discounted_price(self):
        if self.promotion and self.promotion.end_date >= timezone.now() >= self.promotion.start_date:
            discount_amount = self.price * (self.promotion.discount_percentage / 100)
            return self.price - discount_amount
        return self.price