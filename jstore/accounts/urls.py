from django.urls import path
from .views import views

app_name = 'accounts'


urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logoutuser', views.logout_user, name='logout'),
]
