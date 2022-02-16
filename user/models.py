from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CHOICES = (
    ('Administrator', 'ADMIN'),
    ('Student', 'STUDENT'),
    ('STAFF', 'STAFF'),
    ('FACULTY', 'FACULTY'),
)


class Profile(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    #birthday = models.DateField()
    bio = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=50, null=True)
    image = models.ImageField(default='avatar.jpg', upload_to='profile_images')
    role = models.CharField(max_length=50, choices=CHOICES, null=True)
    new_password = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.users.username}-Profile'
