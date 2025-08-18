from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
# Create your models here.


class UserQR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_secret = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    qr_image=models.FileField(upload_to='files/')
    

    def _str_(self):
        return f"{self.user.username} - {self.qr_secret}"
    

class customer(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    qr_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class customers(models.Model):
    otp = models.CharField(max_length=6)
    contact=models.CharField(max_length=15, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.timestamp < timezone.now() > self.timestamp + datetime.timedelta(minutes=5)


class add_category(models.Model):
    category_name=models.CharField(max_length=30)


class book_detail(models.Model):
    book_name=models.CharField(max_length=50)
    book_category=models.CharField(max_length=40)
    book_description=models.CharField(max_length=200)
    price=models.CharField(max_length=10)
    image=models.FileField(upload_to='files/')

class issued_book(models.Model):
    name=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    book_name=models.CharField(max_length=50)
    book_category=models.CharField(max_length=40)

    
   
class order(models.Model):
    order_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=60)
    email=models.CharField(max_length=80)
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    book_name=models.CharField(max_length=200)
    book_quantity=models.CharField(max_length=10)
    book_prize=models.CharField(max_length=20)
    status=models.CharField(max_length=30,null=True,default='pending')
    datestart=models.DateTimeField(default=timezone.now)

class suggested(models.Model):
    name=models.CharField(max_length=60)
    email=models.CharField(max_length=80)
    contact=models.CharField(max_length=10)
    book_name=models.CharField(max_length=50)
    author_name=models.CharField(max_length=50)


   