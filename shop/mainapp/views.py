from django.shortcuts import render


# Create your views here.

def store(request):
    context = {}
    return render(request, 'mainapp/store.html', context)


def cart(request):
    context = {}
    return render(request, 'mainapp/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'mainapp/checkout.html', context)
