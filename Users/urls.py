from django.urls import path
from . import views


urlpatterns = [
    path('login_user',views.login_user, name='login'),
    path('register_user',views.register_user, name='register_user'),
    path('home',views.home, name='home'),
    path('sport',views.sportpage, name='sport'),
    path('userbookings',views.bookings, name='bookings'),
    path('addsport',views.addsport, name='addsport'),
    path('addslot',views.addslot, name="addslot"),
    path('bookslot', views.bookslot, name="bookslot"),
    path('edit', views.edit, name="edit"),
    path('cancel', views.cancel, name="cancel"),
    path('refresh', views.refresh, name="refresh"),
    path('logout_user/', views.logout_user, name="logout"),
]