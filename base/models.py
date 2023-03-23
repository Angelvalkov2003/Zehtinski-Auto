from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Car(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    horsepower = models.IntegerField()
    gear = models.CharField(max_length=50)
    fuel = models.CharField(max_length=50)
    price = models.IntegerField()
    picture = models.ImageField(upload_to = 'files/picturesCars')
    manufactured = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.title
    
class Part(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to = 'files/picturesParts')
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True, null=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]
    
    
class OrdersPart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return str(self.part)
        
class OrdersCar(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=15, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    def __str__(self):
        return str(self.car)