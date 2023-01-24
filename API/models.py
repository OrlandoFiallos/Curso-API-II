from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    slug = models.SlugField(editable=False)
    title = models.CharField(max_length=255) 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
    def __str__(self):
        return self.title

class WatchesCategory(models.Model):
    slug = models.SlugField(editable=False)
    title = models.CharField(max_length=255) 
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title

class Watches(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
    def __str__(self):
        return self.title