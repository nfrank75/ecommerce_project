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


def index(request):

    carrier_id = request.GET.get('carrier_id')
    address_billing_id = request.GET.get('address_billing_id', '')
    new_shipping_address = request.GET.get('new_shipping_address', '')
    if address_billing_id and address_billing_id !="":
        address_billing_id = int(address_billing_id )
    address_shipping_id = request.GET.get('address_shipping_id', address_billing_id)
    if address_shipping_id and address_shipping_id !="":
        address_shipping_id = int(address_shipping_id) 
    ready_to_pay = False
    if new_shipping_address and new_shipping_address !='false':
        ready_to_pay = bool(address_billing_id) and bool(address_shipping_id)
    else:
        ready_to_pay = bool(address_billing_id)
        
    
    if carrier_id and carrier_id != '':
        carrier = Carrier.objects.filter(id=carrier_id).first()
        if carrier:
            request.session['carrier'] = {
                'id': carrier.id,
                'name': carrier.name,
                'price': carrier.price
                }
            
    cart = CartService.get_cart_details(request)
    carriers = Carrier.objects.all()
    address_form =  CheckoutAddressForm()
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


        