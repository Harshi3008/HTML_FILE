import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from datetime import timedelta, date
# Create your models here.


class UserQR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_secret = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True) 
    

    def _str_(self):
        return f"{self.user.username} - {self.qr_secret}"
    

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=True,)
    adhaar_no= models.CharField(max_length=12, unique=True, blank=False, null=False)
    contact = models.CharField(max_length=10, unique=True,)
    address = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10)
    is_active = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True) 

    def __str__(self):
        return self.name
    
class otp(models.Model):
    otp = models.CharField(max_length=6)
    contact=models.CharField(max_length=15, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.timestamp < timezone.now() > self.timestamp + datetime.timedelta(minutes=5)


class add_category(models.Model):
    category_name=models.CharField(max_length=30)


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    category=models.CharField(max_length=40)
    sub_category=models.CharField(max_length=40, default='General')
    language=models.CharField(max_length=200)
    price=models.CharField(max_length=10)
    image=models.FileField(upload_to='files/')
    author = models.CharField(max_length=100)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.author}"

class Issued_book(models.Model):
    name=models.CharField(max_length=20)
    contact=models.CharField(max_length=10)
    title=models.CharField(max_length=50)
    category=models.CharField(max_length=40)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto set return_date to 15 days later if not given
        if not self.return_date:
            self.return_date = date.today() + timedelta(days=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.name} issued by {self.user.username}"


class suggested(models.Model):
    name=models.CharField(max_length=60)
    email=models.CharField(max_length=80)
    contact=models.CharField(max_length=10)
    book_name=models.CharField(max_length=50)
    author_name=models.CharField(max_length=50)



class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)

    def _str_(self):
        return self.title



class Team(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='team/', blank=True, null=True)

    def _str_(self):
        return self.name
    

class Donation(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    purpose = models.TextField()
    book_name = models.CharField(max_length=200)
    number_of_books = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.full_name}"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact from {self.name} - {self.email}"






class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    reissued = models.BooleanField(default=False)
    datestart=models.DateTimeField(default=timezone.now)

    def due_date(self):
        return self.issue_date + timedelta(days=15)

    def penalty(self):
        if not self.is_returned and date.today() > self.due_date():
            days_late = (date.today() - self.due_date()).days
            return days_late * 5   # Example: 10 Rs/day penalty
        return 0

    def can_reissue(self):
        today = date.today()
        days_since_issue = (today - self.issue_date).days
        prebooked = PreBooking.objects.filter(book=self.book).exclude(user=self.user).exists()
        return 5 <= days_since_issue < 15 and not prebooked and not self.reissued


class PreBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} pre-booked {self.book.title}"
