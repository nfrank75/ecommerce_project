from django.db import models
from django.utils.text import slugify

from ..models.Category import Category



class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=120, blank=False, null=False)
    more_description = models.TextField()
    additional_infos = models.TextField()
    stocks = models.IntegerField(blank=False, null=False)
    solde_price = models.IntegerField(blank=False, null=False)
    regular_price = models.IntegerField(blank=False, null=False)
    rate = models.IntegerField(blank=False, null=False)
    brand = models.CharField(max_length=120, blank=False, null=False)
    is_available = models.BooleanField(blank=False, null=False)
    is_best_seller = models.BooleanField(blank=False, null=False)
    is_new_arrival = models.BooleanField(blank=False, null=False)
    is_featured = models.BooleanField(blank=False, null=False)
    is_special_offer = models.BooleanField(blank=False, null=False)
    categories = models.ManyToManyField(Category)
    currency = models.CharField(max_length=120, blank=False, null=False)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def rate(self):
        if self.regular_price and self.solde_price:
            rate = ((self.regular_price - self.solde_price)/self.regular_price)*100

            self.rate = rate

            return int(self.rate)
        

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name