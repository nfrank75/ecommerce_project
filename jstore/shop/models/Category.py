from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=False, null=False)
    is_mega = models.BooleanField(blank=False, null=False)
    image = models.ImageField(upload_to="category_images/%Y/%m/%d/", blank=False, null=False)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
            
            
    def __str__(self):
        return self.name

                