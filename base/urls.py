from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name="home"),
    
    path('shop/', views.shop, name="shop"),
    path('carinfo/<str:pk>/', views.carinfo, name="carinfo"),
    
    path('add-car', views.addCar, name = "add-car"),
    path('update-car/<str:pk>', views.updateCar, name = "update-car"), 
    path('delete-car/<str:pk>', views.deleteCar, name = "delete-car"),
    
    
    path('shopparts/', views.shopparts, name="shopparts"),
    path('partinfo/<str:pk>/', views.partinfo, name="partinfo"),
    
    path('add-part', views.addPart, name = "add-part"),
    path('update-part/<str:pk>', views.updatePart, name = "update-part"), 
    path('delete-part/<str:pk>', views.deletePart, name = "delete-part"),
    
    path('delete-comment/<str:pk>', views.deleteComment, name = "delete-comment"),
    path('buyCar/<str:pk>', views.buyCar, name = "buyCar"),
    path('buyPart/<str:pk>', views.buyPart, name = "buyPart"),
    
    path('carOrders', views.carOrders, name="carOrders"),
    path('partOrders', views.partOrders, name="partOrders"),
    
    path('information', views.information, name="information"),
    
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:pk>', views.userProfile, name = "user-profile" ),
]
