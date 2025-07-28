from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class coustomer(models.Model):
    name = models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    contact=models.CharField(max_length=10)
    password=models.CharField(max_length=50)
    user_type=models.CharField(max_length=10)

class add_category(models.Model):
    category_name=models.CharField(max_length=30)


class product_detail(models.Model):
    product_name=models.CharField(max_length=50)
    product_category=models.CharField(max_length=40)
    product_description=models.CharField(max_length=200)
    price=models.CharField(max_length=10)
    image=models.FileField(upload_to='files/')

class issued_book(models.Model):
    book_name=models.CharField(max_length=50)
    book_category=models.CharField(max_length=40)
    name=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
   
class order(models.Model):
    order_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=60)
    email=models.CharField(max_length=80)
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    p_name=models.CharField(max_length=200)
    p_quantity=models.CharField(max_length=10)
    p_prize=models.CharField(max_length=20)
    status=models.CharField(max_length=30,null=True,default='pending')
    datestart=models.DateTimeField(default=timezone.now)

class suggested(models.Model):
    book_name=models.CharField(max_length=50)
    author_name=models.CharField(max_length=50)
   