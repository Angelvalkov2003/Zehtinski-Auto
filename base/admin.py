from django.contrib import admin
from .models import Car, Brand, Comment, Part, OrdersPart, OrdersCar
# Register your models here.

admin.site.register(Car)
admin.site.register(Brand)
admin.site.register(Comment)
admin.site.register(Part)
admin.site.register(OrdersPart)
admin.site.register(OrdersCar)