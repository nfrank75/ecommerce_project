from django.shortcuts import render, redirect
from shop.services.wish_service import WishService


def index(request):
    wishlist = WishService.get_wished_products_details(request)
    if not wishlist:
        return redirect('shop:index')
        
    return render(request, 'shop/wishlist.html',  { 'wishlist': wishlist, })

def add_to_wishlist(request, product_id):
    WishService.add_product_to_wish(request, product_id)
    return redirect('shop:wishlist')

def remove_from_wishlist(request, product_id):
    WishService.remove_product_from_wish(request, product_id)
    return redirect('shop:wishlist')
