from django.contrib import admin

# Register your models here.
from .models import Entry, Choice

admin.site.register(Entry)
admin.site.register(Choice)
