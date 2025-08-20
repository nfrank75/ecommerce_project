from django.shortcuts import render, redirect   
from shop.services.cart_service import CartService
from shop.models.Carrier import Carrier
from shop.forms.CheckoutAddressForm import CheckoutAddressForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout


def index(request):

    carrier_id = request.GET.get('carrier_id')
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
    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'carriers': carriers,
        'address_form': address_form,
        
        })



def add_address(request):
    user = request.user
    if request.method == 'POST':
        address_form = CheckoutAddressForm(request.POST)
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


        