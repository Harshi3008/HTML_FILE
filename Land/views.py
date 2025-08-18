from datetime import date
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from.models import add_category,book_detail, order, customer, suggested, issued_book, customers
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import UserQR
from twilio.rest import Client
import json
import qrcode
from django.http import HttpResponse
import io, os
import uuid


# Create your views here.


#admin views
def add_categorys(request):
    if request.method=="POST":
        cname=request.POST['category_name']
        add_category(category_name=cname).save()
        msg="category added"
        return render(request,'admin/add_category.html',{'msg':msg})
    return render(request,'admin/add_category.html')

def view_category(request):
    data=add_category.objects.all()
    return render(request,'admin/view_category.html',{'data':data})



def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def add_products(request):
    if request.method == "POST":
        bname = request.POST['book_name']
        bcategory = request.POST['book_category']
        bdescription = request.POST['book_description']
        price = request.POST['price']
        file = request.FILES['image']
        book_detail(book_name=bname, book_category=bcategory, book_description=bdescription, price=price, image=file).save()
        msg = "Book added"
        return render(request, 'admin/add_product.html', {'msg': msg})
    return render(request, 'admin/add_product.html')

def view_products(request):
    data = book_detail.objects.all()
    return render(request, 'admin/view_product.html', {'data': data})

def view_issued_book(request):
    data = issued_book.objects.all()
    return render(request, 'admin/view_issued_books.html', {'data': data})

def view_customer(request):
    data = customer.objects.all()
    return render(request, 'admin/view_subscription.html', {'data': data})


def suggested_book(request):
    data = suggested.objects.all()
    return render(request, 'admin/suggested_books.html', {'data': data})

def logout(request):
    return redirect('index')





def upload_suggested_books(request):
    if request.method=="POST":
        bname=request.POST['book_name']
        aname=request.POST['author_name']
        suggested(book_name=bname, author_name=aname).save()
        msg="added"
        return render(request,'user/upload_suggested_book.html',{'msg':msg})
    return render(request,'user/upload_suggested_book.html')


def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

def view_books(request):
    data = book_detail.objects.all()
    return render(request, 'book.html', {'data': data})


def issue_books(request):
    data = book_detail.objects.all()
    return render(request, 'user/issue_book.html', {'data': data})


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def event(request):
    return render(request, 'events.html')

def contacts(request):
    return render(request, 'contact.html')

def contribution(request):
    return render(request, 'contributions.html')

def issue_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        register_number = request.session.get('register_number')
        if book_id and register_number:
            try:
                book = book_detail.objects.get(id=book_id)
                user = customer.objects.get(contact=register_number)
                issued_book.objects.create(
                    book_name=book.product_name,
                    book_category=book.product_category,
                    name=user.name,
                    contact=user.contact
                )
                msg = f"Book '{book.product_name}' issued successfully."
            except book_detail.DoesNotExist:
                msg = "Book not found."
            except customer.DoesNotExist:
                msg = "User not found."
        else:
            msg = "Invalid request."
        data = book_detail.objects.all()
        return render(request, 'issue.html', {'data': data, 'msg': msg})
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            data = book_detail.objects.filter(
                customer(product_name__icontains=search_query) |
                customer(product_category__icontains=search_query)
            )
        else:
            data = book_detail.objects.all()
        return render(request, 'issue.html', {'data': data})

def issue_book(request):
    if request.method=="POST":
        name=request.POST['name']
        email_id=request.POST['email']
        if customer.objects.filter(email=email_id,name=name):
            data=customer.objects.filter(email=email_id,name=name).get()
            return redirect('book.html')
        else:
            msg="Invalid name or email"
            return render(request,'issue.html',{'msg':msg})
    return render(request,'issue.html')



def books(request):
    data = book_detail.objects.all()
    return render(request, 'book.html', {'data': data})

def reviews(request):
    return render(request, 'review.html')



def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if entered_otp == session_otp:
            return redirect('issue_book')
        else:
            error = "Invalid OTP"
            return render(request, 'otp.html', {'error': error})
    else:
        return render(request, 'otp.html')





def memberships(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        # Validation (basic)
        if len(contact) != 10 or not contact.isdigit():
            return render(request, "membership.html", {
                "error": "Contact must be a 10-digit number."
            })
        if not email.endswith(".com"):
            return render(request, "membership.html", {
                "error": "Email must be valid and end with .com"
            })

        # Check if customer already exists
        if customer.objects.filter(email=email).exists():
            return render(request, "membership.html", {
                "error": "Email already registered. Please use a different email."
            })

        # Save customer
        new_customer = customer(
            name=name, 
            email=email,
            contact=contact,
            address=address,
            user_type='Customer',
            is_active=True
        )
        new_customer.save()

        # Generate QR code (for login later, using email + contact as data)
        qr_data = f"{new_customer.email}|{new_customer.contact}"
        qr_img = qrcode.make(qr_data)

        # Path to save QR
        qr_path = os.path.join(settings.MEDIA_ROOT, f"qrcodes/{new_customer.id}.png")
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        qr_img.save(qr_path)

        # Save QR path in model
        new_customer.qr_code = f"qrcodes/{new_customer.id}.png"
        new_customer.save()

        return render(request, "membership.html", {
            "success": "Signup successful! Scan this QR for login.",
            "qr_image": new_customer.qr_code
        })
    
    # Default return for GET requests
    return render(request, "membership.html")



# 🔸 Show QR code page
def qr_code_page(request):
    return render(request, "qr.html") 

# 🔸 Generate QR code image dynamically
def generate_qr(request):
    user_qr = UserQR.objects.get(user=request.user)
    qr = qrcode.make(user_qr.qr_secret)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
            


def logins(request):
    if request.method=="POST":
        name=request.POST['name']
        email_id=request.POST['email']
        if customer.objects.filter(email=email_id,name=name):
            data=customer.objects.filter(email=email_id,name=name).get()
            user_type=data.user_type
            if user_type=='Admin':
                request.session['email']=email_id
                return redirect('admin_dashboard')
            else:
                request.session['email']=email_id
                return redirect('user_dashboard')
        else:
            msg="Invalid name or email"
            return render(request,'login.html',{'msg':msg})
    return render(request,'login.html')





def qr_login_new(request):
    return render(request, "qr_login.html")


def qr_login_page(request):
    return render(request, "login.html")

def qr_login_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        qr_data = data.get("qrData")

        try:
            user_qr = UserQR.objects.get(qr_secret=qr_data)
            user = user_qr.user
            login(request, user)  # Django login
            return JsonResponse({"success": True})
        except UserQR.DoesNotExist:
            return JsonResponse({"success": False})

    return JsonResponse({"success": False, "error": "Invalid request"})


def generate_qr(request):
    user_qr = UserQR.objects.get(user=request.user)
    img = qrcode.make(user_qr.qr_secret)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response



