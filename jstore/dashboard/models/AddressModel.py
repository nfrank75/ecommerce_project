from django.db import models    
from accounts.models.Customer  import Customer


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
        ]
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    more_details = models.TextField(max_length=255, null=True, blank=True)
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPE_CHOICES)
    author =  models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

            
    def __str__(self):
        return self.name

    

    
    

    

    def __str__(self):
        return self.name