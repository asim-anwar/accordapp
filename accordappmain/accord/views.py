import datetime
import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import *
from .forms import *


# Create your views here.

# lobbys = [
#     {'id':1, 'name':'Python-grammers'},
#     {'id':2, 'name':'Java-grammers'},
#     {'id':3, 'name':'Cpp-grammers'},
#     {'id':4, 'name':'React-grammers'}
# ]


def loginpage(request):
    page = 'login'
    error = ''
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        # username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            email = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Username or password incorrect'
            messages.error(request, 'Username or password incorrect')

    context = {'page': page, 'error': error}
    return render(request, 'accord/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def signup(request):
    page = 'signup'
    if request.user.is_authenticated:
        return redirect('home')
    error = ''

    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            error = form.errors
            messages.error(request, 'Sign up unsuccessful, please try again later.')

    context = {'page': page, 'form': form, 'error': error}
    return render(request, 'accord/login_register.html', context)


@login_required(login_url='login')
def home(request):
    page = 'home'

    if request.method == 'POST':
        order = Order.objects.get(id=request.POST.get('order_id'))
        # print(product, available)
        order.status = request.POST.get('available')
        order.save()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    orders = Order.objects.all()
    if q != '':
        orders = orders.filter(
            Q(customer_name__icontains=q) |
            Q(product__product_name__icontains=q) |
            Q(customer_contactnumber__contains=q) |
            Q(order_id__contains=q) |
            Q(product__product_id__contains=q) |
            Q(status__icontains=q))

    products = Product.objects.all()
    pages = Pages.objects.all()
    if request.user.id == 1:
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.filter(assigned_to=request.user)

    context = {'page': page, 'orders': orders, 'pages': pages, 'products': products, 'tasks': tasks}
    return render(request, 'accord/home.html', context)


@login_required(login_url='login')
def products(request):
    page = 'products'

    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        available = request.POST.get('available')
        # print(product, available)
        product.available = available
        product.save()
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    orders = Order.objects.all()
    products = Product.objects.all()
    if q != '':
        products = products.filter(
            Q(product_name__icontains=q) |
            Q(price__contains=q) |
            Q(product_type__contains=q) |
            Q(product_id__contains=q) |
            Q(available__contains=q))

    pages = Pages.objects.all()
    if request.user.id == 1:
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.filter(assigned_to=request.user)

    context = {'page': page, 'orders': orders, 'pages': pages, 'products': products, 'tasks': tasks}
    return render(request, 'accord/products.html', context)


@login_required(login_url='login')
def tasks(request):
    page = 'tasks'

    if request.method == 'POST':
        task = Tasks.objects.get(id=request.POST.get('task_id'))
        # available = request.POST.get('available')
        # print(product, available)
        task.status = 2
        task.save()

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if request.user.id == 1:
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.filter(assigned_to=request.user)

    if q != '':
        tasks = tasks.filter(
            Q(completed_by__icontains=q) |
            Q(assigned_to__icontains=q) |
            Q(task_id__contains=q)
        )
    # topics = Topic.objects.all()[0:6]
    # lobby_count = lobbys.count
    # posts = Post.objects.filter(lobby__topic__name__icontains=q)[0:4]
    orders = Order.objects.all()
    products = Product.objects.all()
    pages = Pages.objects.all()

    context = {'page': page, 'orders': orders, 'pages': pages, 'products': products, 'tasks': tasks}
    return render(request, 'accord/tasks.html', context)


def lobby(request, pk):
    page = 'lobby'
    lobby = Lobby.objects.get(id=pk)
    posts = lobby.post_set.all().order_by('-created')
    participants = lobby.participants.all()

    if request.method == 'POST':
        post = Post.objects.create(
            user=request.user,
            lobby=lobby,
            post=request.POST.get('post')
        )
        lobby.participants.add(request.user)
        return redirect('lobby', pk=lobby.id)

    context = {'page': page, 'lobby': lobby, 'posts': posts, 'participants': participants}
    return render(request, 'accord/lobby.html', context)


def user_profile(request, pk):
    page = 'user-profile'
    user = User.objects.get(id=pk)
    lobbys = user.lobby_set.all()
    posts = user.post_set.all()
    topics = Topic.objects.all
    pages = Pages.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    if request.user.id == 1:
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.filter(assigned_to=request.user)

    context = {'page': page, 'user': user, 'lobbys': lobbys, 'posts': posts, 'topics': topics, 'pages': pages,
               'products': products, 'tasks': tasks, 'orders': orders}
    return render(request, 'accord/user_profile.html', context)


def order_list(request):
    page = 'order-list'
    # user = User.objects.get(id=pk)
    orders = Order.objects.all()
    # posts = user.post_set.all()
    # topics = Topic.objects.all

    context = {'page': page, 'orders': orders}
    return render(request, 'accord/feed_component.html', context)


@login_required(login_url='login')
def create_lobby(request):
    page = 'create-lobby'
    form = LobbyForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # form = LobbyForm(request.POST)
        # if form.is_valid():
        #     lobby = form.save(commit=False)
        #     lobby.host = request.user
        #     lobby.save()
        Lobby.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'page': page, 'form': form, 'topics': topics}
    return render(request, 'accord/create_update_lobby.html', context)


@login_required(login_url='login')
def create_order(request):
    page = 'create-order'
    form = OrderForm()
    error = ''
    products = Product.objects.all()
    # topics = Topic.objects.all()

    try:
        if request.method == 'POST':
            Price = Product.objects.get(product_id=request.POST.get('product')).price
            product_id = Product.objects.get(product_id=request.POST.get('product')).id
            quantity = request.POST.get('quantity')
            form = OrderFormPOST(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.created_by = request.user
                order.created_date = datetime.datetime.now()
                order.order_id = 'OD' + str(random.randint(100000, 999999))
                order.total_price = int(Price) * int(quantity)
                order.product_id = product_id
                order.save()
                return redirect('home')
            else:
                error = form.errors

    except Exception as e:
        error = str(e)

    context = {'page': page, 'form': form, 'error': error, 'products': products}
    return render(request, 'accord/create_update_order.html', context)


@login_required(login_url='login')
def create_product(request):
    page = 'create-product'
    form = ProductForm()
    error = ''
    # topics = Topic.objects.all()

    if request.method == 'POST':
        # Price = Product.objects.get(id=request.POST.get('product')).price
        # quantity = request.POST.get('quantity')
        form = ProductForm(request.POST)
        ptype = request.POST.get('product_type')
        pshort = 'FG' if ptype == 'Figurines' else 'KCN' if ptype == 'Keychains' else 'KC' if ptype == 'Keycaps' else 'SW' if ptype == 'Swords' else 'HP' if ptype == 'Headphone Pouch' else 'MP' if ptype == 'Mousepads' else 'JS' if ptype == 'Clothing' else 'HL' if ptype == 'Heirloom' else ''
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.created_date = datetime.datetime.now()
            product.product_type = ptype
            product.preorder = int(request.POST.get('price')) * (30 / 100)
            product.product_id = pshort + str(random.randint(100000, 999999))
            product.available = request.POST.get('available')
            product.save()
        else:
            error = form.errors

        # Order.objects.create(
        #     customer_name=request.POST.get('customer_name'),
        #     customer_contactnumber=request.POST.get('customer_contactnumber'),
        #     customer_address=request.POST.get('customer_address'),
        #     product_id=request.POST.get('product'),
        #     order_id='OD'+str(random.randint(100000, 999999)),
        #     quantity=request.POST.get('quantity'),
        #     total_price=int(Price)*int(quantity)
        # )
        return redirect('products')

    context = {'page': page, 'form': form, 'error': error}
    return render(request, 'accord/create_update_product.html', context)


@login_required(login_url='login')
def create_task(request):
    page = 'create-task'
    form = TaskForm()
    error = ''
    users = User.objects.all()

    if request.method == 'POST':
        # Price = Product.objects.get(id=request.POST.get('product')).price
        # quantity = request.POST.get('quantity')
        form = TaskForm(request.POST)
        # print(request.POST.get('assigned_to'))

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.created_date = datetime.datetime.now()
            task.assign_date = datetime.datetime.now()
            task.assigned_to = User.objects.get(username=request.POST.get('assigned_to'))
            # task.preorder = int(request.POST.get('price')) * (30 / 100)
            task.task_id = 'TSK' + str(random.randint(10000, 99999))
            task.save()
        else:
            error = form.errors
            print(error)

        # Order.objects.create(
        #     customer_name=request.POST.get('customer_name'),
        #     customer_contactnumber=request.POST.get('customer_contactnumber'),
        #     customer_address=request.POST.get('customer_address'),
        #     product_id=request.POST.get('product'),
        #     order_id='OD'+str(random.randint(100000, 999999)),
        #     quantity=request.POST.get('quantity'),
        #     total_price=int(Price)*int(quantity)
        # )
        return redirect('tasks')

    context = {'page': page, 'form': form, 'error': error, 'users': users}
    return render(request, 'accord/create_update_task.html', context)


@login_required(login_url='login')
def update_lobby(request, pk):
    page = 'update-lobby'
    lobby = Lobby.objects.get(id=pk)
    form = LobbyForm(instance=lobby)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        lobby.name = request.POST.get('name')
        lobby.topic = topic
        lobby.description = request.POST.get('description')
        lobby.save()
        return redirect('home')

    context = {'page': page, 'form': form, 'topics': topics, 'lobby': lobby}
    return render(request, 'accord/create_update_lobby.html', context)


@login_required(login_url='login')
def deleteLobby(request, pk):
    page = 'delete-lobby'
    lobby = Lobby.objects.get(id=pk)

    if request.method == 'POST':
        lobby.delete()
        return redirect('home')

    return render(request, 'accord/delete.html', {'obj': lobby, 'page': page})


@login_required(login_url='login')
def deletePost(request, pk):
    page = 'delete-post'
    post = Post.objects.get(id=pk)
    lobbyId = post.lobby_id

    if request.method == 'POST':
        post.delete()
        return redirect('lobby', pk=lobbyId)

    return render(request, 'accord/delete.html', {'obj': post, 'page': page})


@login_required(login_url='login')
def update_user(request):
    page = 'update-user'
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)

    context = {'page': page, 'form': form}
    return render(request, 'accord/update-user.html', context)


@login_required(login_url='login')
def update_order(request, pk):
    page = 'update-order'
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderFormPOST(request.POST, instance=order)
        if form.is_valid():
            if request.POST.get('product') != '':
                order.product_id = Product.objects.get(product_id=request.POST.get('product')).id
            order.save()
            form.save()

            return redirect('home')
    products = Product.objects.all()
    order = Order.objects.get(id=pk)

    context = {'page': page, 'form': form, 'products': products, 'order': order}
    return render(request, 'accord/update-order.html', context)


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'accord/topics.html', {'topics': topics})


def pages(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    pages = Pages.objects.filter(page_name__icontains=q)
    return render(request, 'accord/pages.html', {'pages': pages})


def activity(request):
    posts = Post.objects.all()
    return render(request, 'accord/activity.html', {'posts': posts})
