import json
import string
import random

from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, RegisterForm, PasswordResetForm
# Create your views here.
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from json import dumps


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    message = ""
    last_login = "You are logged out"
    format_data = '"%Y-%m-%d %H:%M:%S.%f"'
    if request.session.get('last_login', False):
        last_login = datetime.strptime(request.session.get('last_login'), format_data)
        time = datetime.now() - last_login
        if time.total_seconds() > 3600:
            message = "Your last login was more than one hour ago"
            logout(request)
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': last_login, 'user': request.user})


def about(request):
    # return render(request, 'myapp/about.html', )
    if 'about_visits' in request.COOKIES:
        count_visited = int(request.COOKIES['about_visits'])
        response = render(request, 'myapp/about.html', {'no_of_times_visited': count_visited + 1})
        response.set_cookie('about_visits', count_visited + 1, max_age=300)
    else:
        response = render(request, 'myapp/about.html', {'no_of_times_visited': 1})
        response.set_cookie('about_visits', 1)
    return response


def detail(request, cat_no):
    category = None
    product = None
    try:
        category = Category.objects.get(id=cat_no)
        product = Product.objects.filter(category=category.id)
    except Exception as e:
        pass

    return render(
        request,
        'myapp/detail.html',
        {'category': category, 'products': product}
    )


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


@login_required(login_url='/myapp/login')
def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if order.num_units <= order.product.stock:

                order.save()
                update_stock = Product.objects.get(id=order.product.id)
                update_stock.stock = update_stock.stock - order.num_units
                update_stock.save()
                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = None
    try:
        product = Product.objects.filter(id=prod_id)
    except Exception as e:
        pass

    if request.method == 'POST':
        form = InterestForm(request.POST)
        print(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']
            if interested == '1':
                prod = Product.objects.get(id=prod_id)
                prod.interested = prod.interested + 1
                prod.save()
                print("Updated successfully")
            return render(request, 'myapp/interest_confirmation.html')
    else:
        form = InterestForm()

    return render(
        request,
        'myapp/productdetail.html',
        {'form': form, 'product': product}
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                cur_datetime = datetime.now()
                print(cur_datetime)
                request.session['last_login'] = json.dumps(cur_datetime, default=str)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:orders'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()

            # pwd = form.cleaned_data.get('password1')
            # user = authenticate(username=user.username, password=pwd)
            # login(request, user)

            return HttpResponseRedirect(reverse('myapp:login'))
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        client = Client.objects.filter(email=email)
        if client:
            for user in client:
                new_password = generate_password()
                user.set_password(new_password)
                user.save()

                subject = "Password has been Reset..."
                email_template_name = 'myapp/password_reset_email.txt'
                c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': " Ecommerce Website",
                    "user": 'user',
                    'protocol': 'http',
                    'new_password': new_password
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'sharma9q@uwindsor.ca', [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid Header Found.')
                return redirect('myapp:password_reset_complete', 1)
            else:
                return redirect('myapp:password_reset_complete', 0)
    else:
        if request.user.is_authenticated:
            return redirect('myorders')
        password_reset_form = PasswordResetForm()
        return render(request, 'myapp/password_reset.html', {'form': password_reset_form})


# New Password generation
def generate_password():
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    password_length = 8
    random.shuffle(characters)

    password = []
    for i in range(password_length):
        password.append(random.choice(characters))

    random.shuffle(password)
    return "".join(password)


def password_reset_done(request, done):
    return render(request, 'myapp/password_reset_complete.html', {'done': done})


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:login'))


@login_required(login_url='/myapp/login')
def myorders(request):
    try:
        user = request.user
        client = Client.objects.get(username=user.username)
        orders = Order.objects.filter(client=client)
        message = f'Orders placed by {client} :-'
        if orders.count() == 0:
            message = 'Client has not placed any orders'
        return render(request, 'myapp/myorders.html', {'orders': orders, 'message': message})
    except Client.DoesNotExist:
        message = 'You are not a registered client'
        return render(request, 'myapp/myorders.html', {'message': message})
