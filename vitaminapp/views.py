from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
import bcrypt


def index(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 1) 
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {
        'products': Product.objects.all(),
        'page': page,
        'count': paginator.count,
    }
    return render(request, 'home.html', context)

def products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'product.html', context)

def login_register(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login_register')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/')
    return redirect('/')

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                request.session['greeting'] = user.first_name
                return redirect('/')
        messages.error(request, "Email for password are not right")
    return redirect('/login_register')

def checkout (request):
    return render(request, "checkout.html")

def one_product(request, id):
    context = {
        'one_product': Product.objects.get(id=id),
    }
    return render(request, "one_product.html", context)

