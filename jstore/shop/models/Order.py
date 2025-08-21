from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    client_name = models.CharField(max_length=255)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    taxe = models.IntegerField(blank=True, null=True)
    order_cost = models.IntegerField()
    order_cost_ttc = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    carrier_name = models.CharField(max_length=255)
    carrier_price = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    stripe_payment = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.client_name