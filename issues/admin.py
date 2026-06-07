from django.contrib import admin
from .models import Category, Issue, Location

# Register your models here.

admin.site.register(Category)
admin.site.register(Issue)
admin.site.register(Location)
