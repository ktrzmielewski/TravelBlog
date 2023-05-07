from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]