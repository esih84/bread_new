from django.urls import path
from .views import *

app_name = 'administrator'

urlpatterns = [
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('signup/', Register, name='signup'),
    path('post/', create_post, name="create_post"),
    path('profile/', profile_view, name='profile'),
    path('profile_edit/', profile_save, name='profile_save'),
    path('shoping_cart/', shping_cart, name='shping_cart'),
    path('buy/<int:id>/', Buy, name="buy"),
    path('delete/<int:id>/', delete, name="delete"),
    path('credit_cart/', credit_cart, name="credit_cart"),
]
