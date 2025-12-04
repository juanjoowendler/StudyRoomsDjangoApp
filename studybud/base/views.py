from django.shortcuts import render, redirect # for rendering templates and redirecting
from django.db.models import Q # for complex queries
from .models import Room, Topic, User 
from .forms import RoomForm 
from django.contrib import messages # for flash messages
from django.contrib.auth import authenticate, login, logout # for user authentication
from django.contrib.auth.decorators import login_required # to restrict access to logged-in users
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm # for user registration

# Create your views here.
def loginPage(request):
    page = "login"
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username) 
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")
        
    context = {"page": page}
    return render(request, "base/login_register.html", context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerUser(request):
    page = "register"
    form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # False because we want to modify before saving
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")
        
    
    context = {"page": page, "form": form}
    return render(request, "base/login_register.html", context)

def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else '' 
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) # Q is for complex queries: & is for AND condition, | is for OR condition
        | Q(name__icontains=q) 
        | Q(description__icontains=q)
        | Q(host__username__icontains=q)
        ) if q else Room.objects.all()
    
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    context = {"rooms": rooms, "topics": topics, "room_count": room_count} 
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)

@login_required(login_url="login") # if not logged in when I try to create a new room it redirects me to login page
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        
    context = {'form': form}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login") 
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
      
    context = {'form': form}
    return render(request, "base/room_form.html", context)

@login_required(login_url="login") 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    
    if request.method == "POST":
        room.delete()
        return redirect("home")
    
    return render(request, "base/delete.html", {"obj": room})



