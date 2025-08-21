from django.shortcuts import render, redirect   
from shop.services.cart_service import CartService
from shop.models.Carrier import Carrier
from shop.forms.CheckoutAddressForm import CheckoutAddressForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from accounts.models.Customer import Customer
from django.contrib.auth.decorators import login_required
import random
import string
from django.contrib.auth.hashers import make_password
from accounts.forms.CustomLoginForm import CustomLoginForm
from shop.models.Order import Order
from shop.models.OrderDetail import OrderDetail
from dashboard.models.AddressModel import Address
from django.db import transaction
from shop.models.Product import Product

def index(request):
    carrier_id = request.GET.get('carrier_id')
    address_billing_id = request.GET.get('address_billing_id')
    new_shipping_address = request.GET.get('new_shipping_address', 'false') # Use 'false' as default

    # Convert IDs to int if they exist and are not empty
    if address_billing_id:
        address_billing_id = int(address_billing_id)
    else:
        address_billing_id = None # Make sure it's a falsy value

    address_shipping_id = request.GET.get('address_shipping_id')
    if not address_shipping_id:
        # If new_shipping_address is not checked, the shipping address is the same as the billing address
        if new_shipping_address == 'false':
            address_shipping_id = address_billing_id
    else:
        address_shipping_id = int(address_shipping_id)

    # ready_to_pay is True only if both addresses have been selected
    ready_to_pay = bool(address_billing_id) and bool(address_shipping_id) and bool(carrier_id) # also check carrier_id

    # Rest of your code remains the same...
    if carrier_id:
        carrier = Carrier.objects.filter(id=carrier_id).first()
        if carrier:
            request.session['carrier'] = {
                'id': carrier.id,
                'name': carrier.name,
                'price': carrier.price
            }

    cart = CartService.get_cart_details(request)
    carriers = Carrier.objects.all()
    order_id = None
    if ready_to_pay:
        # create order
        if new_shipping_address and new_shipping_address != 'false':
            billing_address = Address.objects.filter(id=address_billing_id).first()
            shipping_address = Address.objects.filter(id=address_shipping_id).first()
        else:
            billing_address = Address.objects.filter(id=address_billing_id).first()
            shipping_address = None
        # address sous forme de string
        billing_address_str = billing_address.get_address_as_string() if billing_address else ""
        shipping_address_str = shipping_address.get_address_as_string() if shipping_address else None
        
        order_id = create_order(request, billing_address_str, shipping_address_str)
    
    address_form = CheckoutAddressForm()
    login_form = CustomLoginForm()

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'carriers': carriers,
        'address_form': address_form,
        'login_form': login_form,
        'ready_to_pay': ready_to_pay,
        'address_billing_id': address_billing_id,
        'address_shipping_id': address_shipping_id,
        'new_shipping_address': new_shipping_address,
        'order_id': order_id,
    })



def add_address(request):
    user = request.user
    if request.method == 'POST':
        address_form = CheckoutAddressForm(request.POST)
        if not user.is_authenticated:
            email = request.POST.get('email')
            existing_user = Customer.objects.filter(email=email).first()
            if existing_user:
                login(request, existing_user)
                user = existing_user
            else:
                new_user = Customer()
                new_user.username = email
                new_user.email = email
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                new_user.password = make_password(password)
                #TODO : Envoi de mail de création de compte, contenant le mot de passe
                new_user.save()
                login(request, new_user) 
                user = new_user
                 
                
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.author = user
            address.save()
            messages.success(request, 'Address added successfully.')
            
    return redirect('shop:checkout')


def login_form(request):
    if request.user.is_authenticated:
        return JsonResponse({"isSucces": True, 'message': 'This user is already connected !'})
        
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return  JsonResponse({'isSuccess': True, 'message': 'This user is connected'})
            # return redirect('shop:checkout')
        else:
            return JsonResponse({"isSucces": False,
                                 'message': 'Invalid credentials. Unable to connect !',
                                 'email': email,
                                 'password': password
                                 })
        
    return JsonResponse({"isSucces": False, 'message': 'Error, Invalid request method'})        


def create_order(request, billing_address, shipping_address=None):
    cart = CartService.get_cart_details(request)

    order = Order()
    user = request.user
    carrier = request.session.get('carrier', Carrier.objects.first())

    order.client_name = user.username
    order.billing_address = billing_address
    order.shipping_address = shipping_address or billing_address
    order.carrier_name = carrier['name']
    order.carrier_price = carrier['price']
    order.quantity = cart['cart_count']
    order.order_cost = cart['sub_total_ht']
    order.taxe = cart['taxe_amount']
    order.order_cost_ttc = cart['sub_total_with_shipping']
    order.payment_method = 'Stripe'
    order.save()

    # order detail
    with transaction.atomic():
        for item in cart['items']:
            order_details = OrderDetail()

            # Retrieve the product object using its ID
            product_id = item.get('product').get('id')
            product = Product.objects.get(id=product_id)
            
            # Now, link the OrderDetail to the Product instance
            order_details.product = product
            
            order_details.product_name = item.get('product').get('name')
            order_details.product_description = item.get('product').get('description')
            order_details.solde_price = item.get('product').get('solde_price')
            order_details.regular_price = item.get('product').get('regular_price')
            order_details.quantity = item.get('quantity')
            order_details.taxe = item.get('taxe_amount')
            order_details.sub_total_ht = item.get('sub_total_ht')
            order_details.sub_total_ttc = item.get('sub_total_ttc')
            order_details.order = order
            order_details.save()

    return order.id
    

        