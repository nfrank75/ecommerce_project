from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models.Customer import Customer

# @admin.register(Customer)
class CustomerAdmin(UserAdmin):
    # Ajout de agree_terms dans les champs affichés dans la liste
    list_display = ('username','email','first_name','last_name','agree_terms','is_staff','is_active',)
    list_filter = ('is_staff','is_active',)

admin.site.register(Customer, CustomerAdmin)
