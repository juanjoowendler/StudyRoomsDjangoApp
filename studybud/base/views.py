from django.shortcuts import render, redirect # for rendering templates and redirecting
from django.db.models import Q # for complex queries
from .models import Room, Topic, User, Message
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
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) # sql: SELECT * FROM message WHERE room.topic.name LIKE '%q%'
    )
    
    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages} 
    return render(request, "base/home.html", context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # sql: SELECT * FROM message WHERE room_id=pk ORDER BY created DESC
    participants = room.participants.all()
    
    if request.method == "POST":
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        
        room.participants.add(request.user) # add the user to participants if they post a message
        return redirect("room", pk=room.id) # because it is a POST request, we redirect to avoid resubmission on refresh
    
    
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)

@login_required(login_url="login") # if not logged in when I try to create a new room it redirects me to login page
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False) # commit=False to modify before saving
            room.host = request.user # set the host to the logged-in user
            room.save()
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


@login_required(login_url="login") 
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here")
    
    if request.method == "POST":
        message.delete()
        return redirect("home") 
    
    return render(request, "base/delete.html", {"obj": message})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = user.message_set.all()  # sql: SELECT * FROM message WHERE user_id=pk 
    rooms = user.room_set.all() 
    
    context = {"user": user, "topics": topics, "room_messages": room_messages, "rooms": rooms}
    return render(request, "base/profile.html", context)
    




