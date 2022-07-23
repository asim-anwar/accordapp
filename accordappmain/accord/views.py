import datetime
import json
import os
import random
import urllib.parse
from email.mime.image import MIMEImage

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

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
        return redirect('menu')

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
            return redirect('menu')
        else:
            error = 'Username or password incorrect'
            messages.error(request, 'Username or password incorrect')

    context = {'page': page, 'error': error}
    return render(request, 'accord/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
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
def mainmenu(request):
    page = 'menu'

    context = {
        'page': page
    }

    return render(request, 'accord/managementmenu.html', context)


@login_required(login_url='login')
def home(request):
    page = 'home'

    if request.method == 'POST':
        order = Order.objects.get(id=request.POST.get('order_id'))
        # print(product, available)
        order.status = request.POST.get('available')
        order.save()
        if order.status in ['IN PRODUCTION', 'ON HAND']:
            mail = EmailVerificationForUpdate(order)
            print(mail)

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    orders = Order.objects.all().order_by('-id')
    if q != '':
        orders = orders.filter(
            Q(customer_name__icontains=q) |
            Q(product__product_name__icontains=q) |
            Q(customer_contactnumber__contains=q) |
            Q(order_id__contains=q) |
            Q(product__product_id__contains=q) |
            Q(status__icontains=q)).order_by('-id')

    products = Product.objects.all()
    order_products = Order_Product.objects.all()
    pages = Pages.objects.all()
    if request.user.id == 1:
        tasks = Tasks.objects.all()
    else:
        tasks = Tasks.objects.filter(assigned_to=request.user)

    context = {'page': page, 'orders': orders, 'pages': pages, 'products': products, 'order_products': order_products,
               'tasks': tasks}
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
    products = Product.objects.all().order_by('-available')
    if q != '':
        products = products.filter(
            Q(product_name__icontains=q) |
            Q(full_sleeve_price__contains=q) |
            Q(half_sleeve_price__contains=q) |
            Q(product_type__contains=q) |
            Q(product_id__contains=q) |
            Q(available__contains=q)).order_by('-available')

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
            Q(completed_by_id__username__icontains=q) |
            Q(assigned_to_id__username__icontains=q) |
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
    mail = ''
    products = Product.objects.filter(available='Yes', product_type="Clothing")
    # topics = Topic.objects.all()

    try:
        if request.method == 'POST':
            product_list = request.POST.get('products_list')
            product_list = json.loads(product_list)

            # Price = Product.objects.get(product_id=request.POST.get('product')).price
            # product_id = Product.objects.get(product_id=request.POST.get('product'))
            # quantity = request.POST.get('quantity')
            form = OrderFormPOST(request.POST)
            order_id_gen = 'OD' + str(random.randint(100000, 999999))
            while Order.objects.filter(order_id=order_id_gen).exists():
                order_id_gen = 'OD' + str(random.randint(100000, 999999))
            if form.is_valid():
                order = form.save(commit=False)
                order.created_by = request.user
                order.created_date = datetime.datetime.now()
                order.order_id = order_id_gen
                # order.total_price =
                # order.product_id = product_id.id
                total = 0
                ordered_products = []

                for selected_product in product_list:
                    form2 = OrderProductForm(selected_product)
                    if form2.is_valid():
                        product_entry = form2.save(commit=False)
                        product_entry.product_id = Product.objects.get(product_id=selected_product['product']).id
                        if selected_product['sleeve'] == 'full':
                            total += Product.objects.get(product_id=selected_product['product']).full_sleeve_price * int(
                                selected_product['quantity'])
                        elif selected_product['sleeve'] == 'half':
                            total += Product.objects.get(product_id=selected_product['product']).half_sleeve_price * int(
                                selected_product['quantity'])
                        order.total_price = total
                        order.save()
                        product_entry.order_id = order.id
                        product_entry.save()
                    else:
                        error = 'Error while taking order form: ' + str(form2.errors)
                orders = Order_Product.objects.filter(order_id=order.id)
                for od in orders:
                    ordered_products.append(od)
                context = {'page': page, 'order': order, 'products': orders, 'total': total,
                           'due': str(total - int(request.POST.get(
                               'paid')))}
                mail = EmailVerification(request.POST, order, ordered_products, context)
                print(mail)
                messages.success(request, 'Order Created Successfully.')
                return redirect('home')
                # if mail.startswith('C'):
                #     mail = 1
                # else:
                #     mail = 2
            else:
                error = 'Error while taking order form: ' + str(form.errors)

    except Exception as e:
        error = 'Error while taking order: ' + str(e)
        messages.error(request, 'Failed to create order.')

    context = {'page': page, 'form': form, 'error': error, 'products': products, 'mail': mail}
    return render(request, 'accord/create_update_order.html', context)


def create_order_customer(request):
    page = 'create-order-customer'
    form = OrderForm()
    error = ''
    mail = ''
    products = Product.objects.filter(available='Yes', product_type='Clothing')
    # topics = Topic.objects.all()

    try:
        if request.method == 'POST':
            product_list = request.POST.get('products_list')
            product_list = json.loads(product_list)

            # Price = Product.objects.get(product_id=request.POST.get('product')).price
            # product_id = Product.objects.get(product_id=request.POST.get('product'))
            # quantity = request.POST.get('quantity')
            form = OrderFormPOST(request.POST)
            order_id_gen = 'OD' + str(random.randint(100000, 999999))
            while Order.objects.filter(order_id=order_id_gen).exists():
                order_id_gen = 'OD' + str(random.randint(100000, 999999))
            if form.is_valid():
                order = form.save(commit=False)
                # order.created_by = request.user
                order.created_date = datetime.datetime.now()
                order.order_id = order_id_gen
                # order.total_price =
                # order.product_id = product_id.id
                total = 0
                ordered_products = []

                for selected_product in product_list:
                    form2 = OrderProductForm(selected_product)
                    if form2.is_valid():
                        product_entry = form2.save(commit=False)
                        product_entry.product_id = Product.objects.get(product_id=selected_product['product']).id
                        if selected_product['sleeve'] == 'full':
                            total += Product.objects.get(product_id=selected_product['product']).full_sleeve_price * int(
                                selected_product['quantity'])
                        elif selected_product['sleeve'] == 'half':
                            total += Product.objects.get(product_id=selected_product['product']).half_sleeve_price * int(
                                selected_product['quantity'])
                        order.total_price = total
                        order.save()
                        product_entry.order_id = order.id
                        product_entry.save()
                    else:
                        error = 'Error while taking order form: ' + str(form2.errors)
                orders = Order_Product.objects.filter(order_id=order.id)
                for od in orders:
                    ordered_products.append(od)
                context = {'page': page, 'order': order, 'products': orders, 'total': total,
                           'due': str(total - int(request.POST.get(
                               'paid')))}
                mail = EmailVerification(request.POST, order, ordered_products, context)
                print(mail)
                messages.success(request, 'Order Created Successfully.')
                return redirect('success')
                # if mail.startswith('C'):
                #     mail = 1
                # else:
                #     mail = 2
            else:
                error = 'Error while taking order! Please provide valid inputs. '

    except Exception as e:
        error = 'Error while taking order!'
        messages.error(request, 'Failed to create order.')

    context = {'page': page, 'form': form, 'error': error, 'products': products, 'mail': mail}
    return render(request, 'accord/create_order_customer.html', context)


def EmailVerification(payload, order, ordered_products, context):
    try:
        product_info = ''
        mail_user_info = 'Thank You for staying with Seikai! Please Confirm your Seikai order details below:'
        # mail_verification = 'Please enter the following verification code in ShareB app to verify your email: ' + code
        mail_order_info_1 = 'Customer Name: ' + payload.get('customer_name') + '\nDelivery Address: ' + payload.get(
            'delivery_address') + '\n ----------------------------------------------'
        mail_order_info_2 = '\nCustom Jersey Name: ' + payload.get(
            'custom_name') + '\nCustom Jersey Number: ' + payload.get(
            'custom_number') + '\nPaid Amount: ' + payload.get(
            'paid') + '\nDue Payment: ' + str(order.total_price - int(payload.get(
            'paid'))) + '\nBkash Number: ' + payload.get('bkash_number')
        for product in ordered_products:
            if product.product.product_id.startswith('JS'):
                product_info += '\nProduct Name: ' + product.product.product_name + '\nSize: ' + str(
                    product.size) + '\nQuantity: ' + str(
                    product.quantity) + '\n ----------------------------------------------'
            # else:
            #     mail_order_info = 'Customer Name: ' + payload.get(
            #         'customer_name') + '\nDelivery Address: ' + payload.get(
            #         'delivery_address') + '\nProduct Name: ' + product.product_name + '\nQuantity: ' + payload.get(
            #         'quantity') + '\nPaid Amount: ' + payload.get(
            #         'paid') + '\nDue Payment: ' + str((product.price * int(payload.get('quantity'))) - int(payload.get(
            #         'paid'))) + '\nBkash Number: ' + payload.get('bkash_number')
        facebook = 'https://www.facebook.com/seikai.bd'
        discord = 'https://discord.gg/wbYsKeXzUr'
        mail_order_info = mail_order_info_1 + product_info + mail_order_info_2
        mail_footer = 'Reply to this email if you face any problem or contact us on:\n discord - ' + discord + '\n facebook - ' + facebook
        email_body = mail_user_info + '\n \n' + mail_order_info + '\n \n' + mail_footer
        email_subject = 'Seikai Order Confirmation. Order-ID: ' + order.order_id

        html_body = render_to_string('accord/email_template.html', context)

        email_verify = EmailMultiAlternatives(
            email_subject,
            email_body,
            os.environ.get('EMAIL_HOST_USER'),
            [payload.get('customer_email')]
        )
        # )email_verify = EmailMessage(
        #     email_subject,
        #     email_body,
        #     os.environ.get('EMAIL_HOST_USER'),
        #     [payload.get('customer_email')]
        # )
        email_verify.attach_alternative(html_body, 'text/html')
        # img_dir = 'static\images'
        # image = 'NavLogo.png'
        # file_path = os.path.join(img_dir, image)
        # with open(file_path, 'r') as f:
        #     img = MIMEImage(f.read())
        #     img.add_header('Content-ID', '<{}>'.format(image))
        #     img.add_header('Content-Disposition', 'inline', filename=image)
        # email_verify.attach(img)
        # email_verify.mixed_subtype = 'related'
        email_verify.send(fail_silently=False)

        return 'Confirmation mail sent to customer email.'
    except Exception as e:
        return 'Failed to send confirmation mail. Error: ' + str(e)


@login_required(login_url='login')
def create_product(request):
    page = 'create-product'
    form = ProductForm()
    error = ''
    # topics = Topic.objects.all()

    if request.method == 'POST':
        # Price = Product.objects.get(id=request.POST.get('product')).price
        # quantity = request.POST.get('quantity')
        form = ProductForm(request.POST, request.FILES)
        ptype = request.POST.get('product_type')
        pshort = 'FG' if ptype == 'Figurines' else 'KCN' if ptype == 'Keychains' else 'KC' if ptype == 'Keycaps' else 'SW' if ptype == 'Swords' else 'HP' if ptype == 'Headphone Pouch' else 'MP' if ptype == 'Mousepads' else 'JS' if ptype == 'Clothing' else 'HL' if ptype == 'Heirloom' else ''
        if form.is_valid():
            product = form.save()
            product.created_by = request.user
            product.created_date = datetime.datetime.now()
            product.product_type = ptype
            # product.preorder = int(request.POST.get('price')) * (30 / 100)
            product.product_id = pshort + str(random.randint(100000, 999999))
            product.available = request.POST.get('available')
            product.save()
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
            task.status = 1
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
    try:
        page = 'update-order'
        order = Order.objects.get(id=pk)
        order_products = Order_Product.objects.filter(order_id=order.id)
        form = OrderFormRetrieve(instance=order)

        if request.method == 'POST':
            product_list = json.loads(request.POST.get('products_list'))
            prev_orders = Order_Product.objects.filter(order_id=order.id)
            form = OrderFormPOST(request.POST, instance=order)
            # order = Order.objects.get(order_id=request.POST.get('order_id'))
            # product = Order.objects.get(order_id=request.POST.get('order_id')).product
            if form.is_valid():
                total = 0
                prev_orders.delete()
                for new_product in product_list:
                    form2 = OrderProductForm(new_product)
                    if form2.is_valid():
                        product_entry = form2.save(commit=False)
                        product_entry.product_id = Product.objects.get(product_id=new_product['product']).id
                        total += Product.objects.get(product_id=new_product['product']).price * int(
                            new_product['quantity'])
                        order.total_price = total
                        product_entry.order_id = order.id
                        product_entry.save()
                    else:
                        error = 'Error while taking order form: ' + str(form2.errors)
                # if request.POST.get('product') != '':
                #     product = Product.objects.get(product_id=request.POST.get('product'))
                #     quantity = request.POST.get('quantity')
                #     price = product.price
                #     order.product_id = Product.objects.get(product_id=request.POST.get('product')).id
                #     order.total_price = int(price) * int(quantity)
                # else:
                #     order.product_id = product
                #     quantity = request.POST.get('quantity')
                #     order.total_price = int(product.price) * int(quantity)
                order.updated_by = request.user
                order.updated_date = datetime.datetime.now()
                order.save()
                ordered_products = Order_Product.objects.filter(order_id=order.id)
                # mail = EmailVerificationForUpdate(request.POST, order, ordered_products)
                form.save()
                messages.success(request, 'Order Updated Successfully.')

                return redirect('home')
            else:
                error = 'Error while taking order form: ' + str(form.errors)
                messages.error(request, 'Failed to update order.')
        products = Product.objects.all()
        order = Order.objects.get(id=pk)

        context = {'page': page, 'form': form, 'products': products, 'order': order, 'order_products': order_products}
        return render(request, 'accord/update-order.html', context)

    except Exception as e:
        error = 'Error while taking order form: ' + str(e)
        messages.error(request, 'Failed to update order.')
        return redirect('home')


def EmailVerificationForUpdate(order):
    try:
        # product_info = ''
        # mail_user_info = 'Thank You for staying with Seikai! Your order has been updated. Please Confirm your Seikai updated order details below:'
        # # mail_verification = 'Please enter the following verification code in ShareB app to verify your email: ' + code
        # mail_order_info_1 = 'Customer Name: ' + payload.get('customer_name') + '\nDelivery Address: ' + payload.get(
        #     'delivery_address') + '\n ----------------------------------------------'
        #
        # mail_order_info_2 = '\nCustom Jersey Name: ' + payload.get(
        #     'custom_name') + '\nCustom Jersey Number: ' + payload.get(
        #     'custom_number') + '\nPaid Amount: ' + payload.get(
        #     'paid') + '\nDue Payment: ' + str(order.total_price - int(payload.get(
        #     'paid'))) + '\nBkash Number: ' + payload.get('bkash_number')
        #
        # for product in ordered_products:
        #     if product.product.product_id.startswith('JS'):
        #         product_info += '\nProduct Name: ' + product.product.product_name + '\nSize: ' + str(
        #             product.size) + '\nQuantity: ' + str(
        #             product.quantity) + '\n ----------------------------------------------'
        #     else:
        #         mail_order_info = 'Customer Name: ' + payload.get(
        #             'customer_name') + '\nDelivery Address: ' + payload.get(
        #             'delivery_address') + '\nProduct Name: ' + product.product_name + '\nQuantity: ' + payload.get(
        #             'quantity') + '\nPaid Amount: ' + payload.get(
        #             'paid') + '\nDue Payment: ' + str((product.price * int(payload.get('quantity'))) - int(payload.get(
        #             'paid'))) + '\nBkash Number: ' + payload.get('bkash_number')
        # facebook = 'https://www.facebook.com/seikai.bd'
        # discord = 'https://discord.gg/wbYsKeXzUr'
        # mail_order_info = mail_order_info_1 + product_info + mail_order_info_2
        # mail_footer = 'Reply to this email if you face any problem or contact us on:\n discord - ' + discord + '\n facebook - ' + facebook
        email_body = 'Order Updated to ' + order.status
        email_subject = 'Seikai Order Update. Order-ID: ' + order.order_id
        # email_verify = EmailMessage(
        #     email_subject,
        #     email_body,
        #     os.environ.get('EMAIL_HOST_USER'),
        #     [payload.get('customer_email')]
        # )
        context = {'order': order}
        html_body = render_to_string('accord/status _mail.html', context)
        email_verify = EmailMultiAlternatives(
            email_subject,
            email_body,
            os.environ.get('EMAIL_HOST_USER'),
            [order.customer_email]
        )
        email_verify.attach_alternative(html_body, 'text/html')
        email_verify.send(fail_silently=False)

        return 'Status update mail sent to customer email.'
    except Exception as e:
        return 'Failed to send status update mail. Error: ' + str(e)


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


def success(request):
    page = 'success'

    context = {
        'page': page
    }

    return render(request, 'accord/success.html', context)


def welcome(request):
    page = 'welcome'

    context = {
        'page': page
    }

    return render(request, 'accord/welcome_seikai.html', context)


@login_required(login_url='login')
def coinShopHome(request):
    page = 'coinshophome'

    context = {
        'page': page
    }

    return render(request, 'accord/coinshophome.html', context)
