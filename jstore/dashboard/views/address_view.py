from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.AddressModel import Address
from ..forms.AddressModelForm import AddressModelForm 


@login_required
def address(request):
    user = request.user
    if request.method == 'POST':
        address_form = AddressModelForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.author = user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('dashboard:address')
    else:
        address_form = AddressModelForm()
        
    addresses = Address.objects.filter(author=user)
    return render(request, 'dashboard/index.html', {
        'page': 'address',
        'address_form': address_form,
        'addresses': addresses
        })



@login_required
def edit_address(request, id):
    user = request.user

    address = get_object_or_404(Address, id=id, author=user)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            address_form = AddressModelForm(request.POST, instance=address)
            if address_form.is_valid():
                address.save()
                messages.success(request, 'Address updated successfully.')
                return redirect('dashboard:address')
        else:
            messages.success(request, 'Server Error !')
            return redirect('dashboard:address')
            
    else:
        address_form = AddressModelForm(instance=address)
    
    return render(request, 'dashboard/index.html', {
        'page': 'address',
        'edit_address_form': address_form,
        })


@login_required
def delete_address(request, id):
    user = request.user
    address = get_object_or_404(Address, id=id, author=user)

    if request.method == 'POST':
        if request.POST.get('_method') == 'DELETE':
            address.delete()
            messages.success(request, 'Address updated successfully.')
    return redirect('dashboard:address')