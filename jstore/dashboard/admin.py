from django.contrib import admin
from django.db import models

from .models.AddressModel import Address

class AddressAdmin(admin.ModelAdmin):
    list_display = ( 'full_name', 'author', 'street', 'code_postal', 'city', 'country', 'more_details','address_type', 'updated_at', )
    list_display_links = ( 'full_name', 'author', 'city')


admin.site.register(Address  , AddressAdmin)
