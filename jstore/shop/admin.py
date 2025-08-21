from django.contrib import admin
from django.utils.html import format_html
from django.db import models


from .models.Slider import Slider
from .models.Collection import Collection
from .models.Category import Category
from .models.Product import Product
from .models.Image import Image
from .models.Setting import Setting
from .models.Social import Social
from .models.Page import Page
from .models.NavCollection import NavCollection
from .models.Carrier import Carrier
from .models.Order import Order
from .models.OrderDetail import OrderDetail


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'button_text', 'button_link', 'display_image', 'update_at' )
    list_display_links = ('title', 'description', 'display_image')

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" width="100" />')

    display_image.short_description = 'image'


class SocialAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'link','updated_at')
    list_display_links = ('name', 'icon', 'link','updated_at')


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_head','is_foot', 'is_checkout')
    list_editable = ('is_head', 'is_foot', 'is_checkout')
    exclude = ('slug',)
    


class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'copyright', 'email', 'display_logo', 'currency', 'taxe_rate', 'logo', 'street', 'city', 'code_postal', 'state','phone','updated_at')
    list_display_links = ('name', 'description', 'copyright', 'email', 'currency', 'taxe_rate', 'logo', 'street', 'city', 'code_postal', 'state','phone','updated_at')

    def display_logo(self, obj):
        return format_html(f'<img src="{ obj.logo.url }" width="100" />')

    display_logo.short_description = 'logo'


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'button_text', 'button_link', 'display_image', 'update_at' )
    list_display_links = ('title', 'description', 'display_image')

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" width="100" />')

    display_image.short_description = 'image'


class NavCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'button_text', 'button_link', 'display_image', 'update_at' )
    list_display_links = ('title', 'description', 'display_image')

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" width="100" />')

    display_image.short_description = 'image'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug', 'display_image', 'update_at', 'is_mega',)
    list_display_links = ('name', 'description', 'slug', 'display_image',)
    list_editable = ('is_mega',)

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" height="50" width="60" />')

    display_image.short_description = 'image'
    exclude = ('slug',)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('name', 'stocks', 'regular_price', 'solde_price',  'rate', 'display_image', "currency", 'is_available', 'is_best_seller', 'is_new_arrival', 'is_featured', 'is_special_offer',  'get_categories', 'slug', 'description', 'more_description', 'additional_infos', 'brand', 'update_at' )
    list_display_links = ('name',  'display_image', 'description', 'slug', 'get_categories', 'update_at')
    list_editable = ('is_available','stocks',  'regular_price', 'solde_price', "currency", 'is_best_seller', 'is_new_arrival', 'is_featured', 'is_special_offer',)
    list_per_page = 5
    list_filter = ('created_at', 'update_at')
    search_fields = ('name',)

    exclude = ('slug',)

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

    def display_image(self, obj):
        first_image = obj.images.first()
        if not first_image:
            return ''
        return format_html(f'<img src="{ first_image.image.url }" height="90" width="80" />')

    display_image.short_description = 'image'
    exclude = ('slug',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'display_image', 'update_at')
    list_display_links = ('product', 'display_image', 'update_at')

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" width="100" />')

    display_image.short_description = 'image'
    exclude = ('slug',)


class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'details', 'price', 'updated_at','display_image',)
    list_display_links = ('name', 'description', 'details', 'updated_at','display_image',)
    list_editable = ('price', )

    def display_image(self, obj):
        return format_html(f'<img src="{ obj.image.url }" width="100" />')

    display_image.short_description = 'image'
    exclude = ('slug',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'billing_address', 'shipping_address', 'quantity', 'taxe', 'order_cost', 'order_cost_ttc', 'is_paid', 'carrier_name', 'carrier_price', 'payment_method', 'status', 'created_at', 'updated_at')
    list_display_links = ('client_name', 'billing_address', 'shipping_address')
    list_filter = ('status',)
    search_fields = ('client_name',)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_description', 'solde_price', 'regular_price', 'quantity', 'taxe', 'sub_total_ht', 'sub_total_ttc', 'created_at', 'updated_at', 'order')
    list_display_links = ('product_name', 'product_description')
    search_fields = ('product_name',)
    list_filter = ('order__client_name',)

admin.site.register(Slider, SliderAdmin)

admin.site.register(Collection  , CollectionAdmin)

admin.site.register(Category  , CategoryAdmin)

admin.site.register(Product  , ProductAdmin)

admin.site.register(Image  , ImageAdmin)

admin.site.register(Setting  , SettingAdmin)

admin.site.register(Social  , SocialAdmin)

admin.site.register(Page  , PageAdmin)

admin.site.register(NavCollection  , NavCollectionAdmin)

admin.site.register(Carrier  , CarrierAdmin)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
