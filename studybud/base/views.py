from django.shortcuts import render

# Create your views here.
rooms = [
    {"id": 1, "name": "Study Room 1"},
    {"id": 2, "name": "Study Room 2"},
    {"id": 3, "name": "Study Room 3"},
]

def home(request):
    context = {"rooms": rooms}
    return render(request, "base/home.html", context)

def room(request, pk):
    room = None
    for r in rooms: 
        if r["id"] == int(pk):
            room = r

    context = {"room": room}
    return render(request, "base/room.html", context)