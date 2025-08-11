# username: admin
# email: admin@example.com
# password: superadmin

from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
