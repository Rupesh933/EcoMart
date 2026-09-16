from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register,      name='register'),
    path('login/',    views.signin,         name='login'),
    path('logout/',   views.signout,        name='logout'),
    path('dashboard/', views.dashboard,    name='dashboard'),
    path('',           views.dashboard,    name='dashboard'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
]
