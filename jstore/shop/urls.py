from django.urls import path
from shop.views import shop_views, cart_views, compare_views, wishlist_views, checkout_view

app_name = "shop"

urlpatterns = [

    # shop
    path('', shop_views.index, name='index'),
    path('page/<str:slug>/', shop_views.display_page, name='page'),
    path('product/<str:slug>/', shop_views.display_product, name='single_product'),
    path('shop/', shop_views.shop, name='shop_list'),

    # cart
    path('cart/', cart_views.index, name='cart'),
    path('cart/add/<int:product_id>', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/<int:quantity>', cart_views.remove_from_cart, name='remove_from_cart'),
    
    # compare
    path('compare/', compare_views.index, name='compare'),
    path('compare/add/<int:product_id>', compare_views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:product_id>', compare_views.remove_from_compare, name='remove_from_cart'),
    
    # wishlist
    path('wishlist/', wishlist_views.index, name='wishlist'),
    path('wishlist/add/<int:product_id>', wishlist_views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>', wishlist_views.remove_from_wishlist, name='remove_from_wishlist'),

    # wishlist
    path('checkout/', checkout_view.index, name='checkout'),
    path('checkout/add_address', checkout_view.add_address, name='add_address'),
    path('checkout/', checkout_view.login_form, name='login_form'),
]
