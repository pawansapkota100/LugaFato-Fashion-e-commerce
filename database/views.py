import http
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    Catagories=Category.objects.all()
    list= Product.objects.all()
    context={"list":list,"Catagories":Catagories}
   
    return render(request, "index.html",context)


def catagories(request,id):
    Catagories=Product.objects.filter(category_id=id)
    context={ "lists":Catagories}
    return render(request, "store.html",context)

def store(request):
    list= Product.objects.all()
    context={"list":list}
    return render(request, "shop.html",context)

def product(request,id):
    pro=Product.objects.filter(id=id)
    context={"product":pro}
    print("hello world")
    print(product)
    return render(request,"product_description.html",context)


@login_required(login_url="/login")
def checkout(request):
    return render(request,'checkout.html')



def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")



@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("/")




# @login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/")


# @login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

from django.shortcuts import render
from .models import Customer, Order, OrderItem

def shopping_details(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        country = request.POST.get('country')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create a new customer instance
        customer = Customer(
            name=full_name,
            country=country,
            address=address,
            phone=phone,
            email=email
        )
        customer.save()

        # Create a new order instance
        order = Order(
            customer=customer,
            total_amount=0,  # Set the initial total amount to 0
            status='pending'  # Set the initial status to 'pending'
        )
        order.save()

        # Get the cart items from the session
        cart_items = request.session.get('cart', {})

        # Calculate the total amount and create order items
        total_amount = 0
        for product_id, item in cart_items.items():
            product = Product.objects.get(id=product_id)
            quantity = item['quantity']
            price = product.price
            subtotal = quantity * price
            total_amount += subtotal

            # Create an order item
            order_item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
                subtotal=subtotal
            )
            order_item.save()

        # Update the total amount in the order
        order.total_amount = total_amount
        order.save()

        # Additional processing or redirection can be done here

    return render(request, 'checkout.html')






def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            # Set additional fields
            user.first_name = name
            user.save()
            # Redirect to a success page or login page
            return redirect('login')
        else:
            # Passwords don't match, show an error message
            error_message = 'Passwords do not match. Please try again.'
            return redirect('/error')
    
    return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or homepage
            return redirect('/')
        else:
            # Invalid login credentials, show an error message
            return redirect('/error')

    return render(request, 'login.html')

def error_view(request):
    return render(request, 'error.html')