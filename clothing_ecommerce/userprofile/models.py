from django.contrib.auth.models import User
from django.db import models
from store.models import Product
from django.utils import timezone

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    is_vendor_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Promotion(models.Model):
    user = models.ForeignKey(User, related_name='promotions', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='promotions', on_delete=models.CASCADE)
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.product.title} - {self.discount_percentage}% off"

    def is_active(self):
        return self.start_date <= timezone.now().date() <= self.end_date