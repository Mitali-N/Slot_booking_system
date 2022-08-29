from django.urls import path
from . import views


urlpatterns = [
    path('login_user',views.login_user, name='login'),
    path('register_user',views.register_user, name='register_user'),
    path('home',views.home, name='home'),
    path('sport',views.sportpage, name='sport'),
    path('userbookings',views.bookings, name='bookings'),
    path('logout_user/', views.logout_user, name="logout"),
]