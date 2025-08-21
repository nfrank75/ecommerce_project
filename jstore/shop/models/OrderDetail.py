from django.db import models
from shop.models.Order import Order
from shop.models.Product import Product

class OrderDetail(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(blank=True, null=True)
    solde_price = models.IntegerField()
    regular_price = models.IntegerField()
    quantity = models.PositiveIntegerField()
    taxe = models.IntegerField(blank=True, null=True)
    sub_total_ht = models.IntegerField()
    sub_total_ttc = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return self.product_name