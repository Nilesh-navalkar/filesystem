from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing,name='landing'),
    path('signup', views.signup,name='signup'),
    path('login', views.login,name='login'),
    path('logout', views.log_out,name='logout'),
    path('collections', views.collections,name='collections'),
    path('delete/<fldn>/<fn>', views.delete,name='delete'),
    path('collections/<path:url_params>/', views.navigation,name='collections_nav'),
    
]
