from django.contrib import admin
from .models import Category, MenuItem, WatchesCategory, Watches

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Watches)
admin.site.register(WatchesCategory)