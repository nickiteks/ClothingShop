from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

import json
import datetime
from .models import *
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .utils import cookieCart, cartData, guestOrder


# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'mainapp/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order}
    return render(request, 'mainapp/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order}
    return render(request, 'mainapp/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if action == 'delete':
        orderItem.delete()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        print('User is now logged in...')

        print("COOKIES:", request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']

        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in items:
            product = Product.objects.get(id=item['product'].id)
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAdder.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)


def product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404('продукт не найден')

    data = cartData(request)
    cartItems = data['cartItems']

    context = {'product': product, 'cartItems': cartItems}

    return render(request, "mainapp/product.html", context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            u = User.objects.get(username=user)
            messages.success(request, 'Account was created for ' + user)

            customer, created = Customer.objects.get_or_create(
                email=email,
                user=u,
                name=user
            )
            customer.save()

            return redirect('login')

    context = {'form': form}
    return render(request, "mainapp/register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'incorrect')

    context = {}
    return render(request, "mainapp/login.html", context)
