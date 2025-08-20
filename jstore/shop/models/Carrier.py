from django.db import models

class Carrier(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to="carrier_images/%Y/%m/%d/", blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Carrier'
        verbose_name_plural = 'Carriers'
            
    def __str__(self):
        return self.name + " " + str(self.price) + " " + "FCFA"

                