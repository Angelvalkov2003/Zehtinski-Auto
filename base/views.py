from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Car, Brand, Comment, Part, OrdersPart, OrdersCar
from .forms import CarForm, PartForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
def home(request):
    return render(request, 'home.html')

def shop(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    cars = Car.objects.filter(
        Q(brand__name__icontains=q) |
        Q(title__icontains = q) 
    )
    
    
    
    brands = Brand.objects.all()
    car_count = cars.count()
    car_comments = Comment.objects.filter(Q(car__brand__name__icontains = q))
    context = {'cars' : cars, 'brands' : brands, 'car_count' : car_count, 'car_comments': car_comments}
    return render(request, 'shop.html', context)

def carinfo(request, pk):
    car = Car.objects.get(id=pk)
    car_comments = car.comment_set.all()
    
    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            car = car,
            body = request.POST.get('body')
        )
        return redirect('carinfo', pk = car.id)
    context = {'car':car, 'car_comments': car_comments}
    return render(request, 'carinfo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addCar(request):
    form = CarForm()
    brands = Brand.objects.all()
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        brand_name = request.POST.get('brand')
        brand, create = Brand.objects.get_or_create(name=brand_name)
        Car.objects.create(
            host=request.user,
            brand = brand,
            title = request.POST.get('title'),
            horsepower = request.POST.get('horsepower'),
            gear = request.POST.get('gear'),
            fuel = request.POST.get('fuel'),
            price = request.POST.get('price'),
            picture = request.FILES.get('picture'),
            manufactured = request.POST.get('manufactured'),
            description = request.POST.get('description'),
            )
        return redirect('shop')
    context = {'form': form, 'brands':brands}
    return render(request, 'car_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updateCar(request, pk):
    car = Car.objects.get(id=pk)
    form = CarForm(instance=car)
    brands = Brand.objects.all()
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        brand_name = request.POST.get('brand')
        brand, created = Brand.objects.get_or_create(name=brand_name)
        car.title = request.POST.get('title')
        car.brand = brand
        car.horsepower = request.POST.get('horsepower')
        car.gear = request.POST.get('gear')
        car.fuel = request.POST.get('fuel')
        car.price = request.POST.get('price')
        car.picture = request.FILES.get('picture')
        car.manufactured = request.POST.get('manufactured')
        car.description = request.POST.get('description')
        car.save()
        return redirect('shop')
        
    context = {'form': form, 'brands':brands}
    return render(request, 'car_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteCar(request, pk):
    car = Car.objects.get(id=pk)
    if request.method == "POST":
        car.delete()
        return redirect('shop')
    return render(request, 'delete.html', {'obj': car})

def shopparts(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ''

    parts = Part.objects.filter(
        Q(brand__name__icontains=q) |
        Q(title__icontains = q) 
    )
        
    brands = Brand.objects.all()
    part_count = parts.count()
    part_comments = Comment.objects.filter(Q(part__brand__name__icontains = q))
    context = {'parts' : parts, 'brands' : brands, 'part_count' : part_count, 'part_comments': part_comments}
    return render(request, 'shopparts.html', context)

def partinfo(request, pk):
    part = Part.objects.get(id=pk)
    part_comments = part.comment_set.all()
    if request.method == "POST":
        comment = Comment.objects.create(
            user = request.user,
            part = part,
            body = request.POST.get('body')
        )
        return redirect('partinfo', pk = part.id)
    context = {'part':part, 'part_comments': part_comments}
    return render(request, 'partinfo.html', context)

@user_passes_test(lambda u: u.is_superuser)
def addPart(request):
    form = PartForm()
    brands = Brand.objects.all()
    if request.method == "POST":
        brand_name = request.POST.get('brand')
        brand, create = Brand.objects.get_or_create(name=brand_name)
        Part.objects.create(
            host=request.user,
            brand = brand,
            title = request.POST.get('title'),
            price = request.POST.get('price'),
            picture = request.FILES.get('picture'),
            description = request.POST.get('description'),
            )
        return redirect('shopparts')
    context = {'form': form, 'brands':brands}
    return render(request, 'part_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updatePart(request, pk):
    part = Part.objects.get(id=pk)
    form = PartForm(instance=part)
    brands = Brand.objects.all()
    if request.method == "POST":
        brand_name = request.POST.get('brand')
        brand, created = Brand.objects.get_or_create(name=brand_name)
        part.title = request.POST.get('title')
        part.brand = brand
        part.price = request.POST.get('price')
        part.picture = request.FILES.get('picture')
        part.description = request.POST.get('description')
        part.save()
        return redirect('shopparts')      
    context = {'form': form, 'brands':brands}
    return render(request, 'part_form.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deletePart(request, pk):
    part = Part.objects.get(id=pk)
    if request.method == "POST":
        part.delete()
        return redirect('shopparts')
    return render(request, 'delete.html', {'obj': part})


@login_required(login_url='login')
def buyCar(request, pk):
    car = Car.objects.get(id=pk)
    if request.method == "POST":
        OrdersCar.objects.create(
            customer=request.user,
            car=car,
            phoneNumber=request.POST.get('phoneNumber'),
            email=request.POST.get('email'),
        )
        return redirect('shop')
    return render(request, 'buyCar.html', {'obj': car})

@login_required(login_url='login')
def buyPart(request, pk):
    part = Part.objects.get(id=pk)
    if request.method == "POST":
        OrdersPart.objects.create(
            customer=request.user,
            part=part,
            phoneNumber=request.POST.get('phoneNumber'),
            email=request.POST.get('email'),
        )
        return redirect('shop')
    return render(request, 'buyPart.html', {'obj': part})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse("You are not allowed here")
    if request.method == "POST":
        comment.delete()
        return redirect('shop')
    return render(request, 'delete.html', {'obj': comment})

@user_passes_test(lambda u: u.is_superuser)
def carOrders(request):
    ordersCars = OrdersCar.objects.all()
    context = {"ordersCars": ordersCars}
    return render(request, 'carOrders.html', context)

@user_passes_test(lambda u: u.is_superuser)
def partOrders(request):
    ordersParts = OrdersPart.objects.all()
    context = {"ordersParts": ordersParts}
    return render(request, 'partOrders.html', context)


def information(request):
    return render(request, 'information.html')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')
    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            redirect('home')
        else:
            messages.error(request, 'An error accured during registration')
    context = {'form': form}
    return render(request, 'login_register.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user= User.objects.get(id=pk)
    ordersCars = OrdersCar.objects.filter(customer = user)
    ordersParts = OrdersPart.objects.filter(customer = user)
    context = {'user': user, 'ordersCars': ordersCars,  'ordersParts': ordersParts}
    return render(request, 'profile.html', context)
