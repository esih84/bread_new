from django.urls import path
from .views import *

app_name = 'administrator'

urlpatterns = [
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('signup/', Register, name='signup'),
    path('post/', create_post, name="create_post"),
    # path('profile/', profile_view, name='profile'),
    # path('profile_save/', profile_save, name='profile_save'),
    # path('buy/<int:id>/', Buy, name="buy"),

]
