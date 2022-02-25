from django.contrib.auth.models import AbstractUser
from django.db import models

deafult_receiver = 1

class User(AbstractUser):
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    age = models.PositiveSmallIntegerField()
    status = models.TextField(max_length=150)
    avatar = models.URLField(max_length=250)

    def serialize(self):
        return {
            "username": self.username,
            "avatar": self.avatar,
            "timestamp": self.last_login,
        }

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class Contacts(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')

    def __str__(self):
        return f'{self.user1.username} is in contact with {self.user2.username}'
