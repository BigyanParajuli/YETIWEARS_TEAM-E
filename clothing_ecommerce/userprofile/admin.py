from django.contrib import admin

from .models import Userprofile
from django.contrib import admin
from .models import Promotion, Product

admin.site.register(Userprofile)
# products/admin.py

admin.site.register(Promotion)
admin.site.register(Product)