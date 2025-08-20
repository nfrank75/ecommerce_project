from django.urls import path
from dashboard.views import dashboard_view, address_view, account_view

app_name = 'dashboard'

urlpatterns = [
    # dashboard
    path('', dashboard_view.index , name='index'),
    
    # address 
    path('address', address_view.address , name='address'),
    path('address/<int:id>/edit', address_view.edit_address , name='edit_address'),
    path('address/<int:id>/delete', address_view.delete_address , name='delete_address'),
    
    # account 
    path('account', account_view.index , name='account'),
    path('account/save', account_view.save_account , name='save_account'),
    path('account/reset', account_view.reset_user_password , name='reset_user_password'),
]
 