from django.urls import path
from .views import home_view,sign_up,sign_in,sign_out,weather

urlpatterns = [
    path('', home_view,name='home'),
    path('signup/', sign_up,name='signup'),
    path('signin/', sign_in,name='signin'),
    path('signout/', sign_out,name='signout'),
    path('weather/', weather,name='weather'),
]