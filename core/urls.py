from django.urls import path
from.import views

urlpatterns = [
path('', views.homePage, name="home"),
path('logout/', views.logout, name="logout"),
path('login/', views.loginU, name="login"),

path('cart/', views.cart, name="cart"),
path('checkout/', views.checkout, name="checkout"),
path('signup/', views.signup, name="signup"),
path('orderpage/', views.orderpage, name="orderpage"),

]