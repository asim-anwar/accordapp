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
            messages.error(request, 'Username or password incorrect')

    context = {'page': page}
    return render(request, 'accord/login_register.html', context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def signup(request):
    page = 'signup'
    if request.user.is_authenticated:
        return redirect('home')

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
            messages.error(request, 'Sign up unsuccessful, please try again later.')

    context = {'page': page, 'form': form}
    return render(request, 'accord/login_register.html', context)


def home(request):
    page = 'home'
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    lobbys = Lobby.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__contains=q)
    )
    topics = Topic.objects.all()[0:6]
    lobby_count = lobbys.count
    posts = Post.objects.filter(lobby__topic__name__icontains=q)[0:4]
    orders = Order.objects.all()

    context = {'page': page, 'lobbys': lobbys, 'topics': topics, 'lobby_count': lobby_count, 'posts': posts, 'orders':orders}
    return render(request, 'accord/home.html', context)


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

    context = {'page': page, 'user': user, 'lobbys': lobbys, 'posts': posts, 'topics': topics}
    return render(request, 'accord/user_profile.html', context)


def order_list(request, pk):
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
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'page': page, 'form': form, 'topics': topics}
    return render(request, 'accord/create_update_lobby.html', context)


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


def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'accord/topics.html', {'topics': topics})


def activity(request):
    posts = Post.objects.all()
    return render(request, 'accord/activity.html', {'posts': posts})
