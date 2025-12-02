from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # oneToMany relationship 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # oneToMany relationship
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null=True: means db can store empty value, blank=True: means form can be empty
    #participants =
    updated = models.DateTimeField(auto_now=True) # every time we update the model, this field gets updated
    created = models.DateTimeField(auto_now_add=True) # only set when created
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE) # oneToMany relationship
     room = models.ForeignKey(Room, on_delete=models.CASCADE) # oneToMany relationship
     body = models.TextField()
     
     def __str__(self):
         return self.body[0:50]