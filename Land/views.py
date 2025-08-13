from datetime import date
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from.models import add_category,product_detail, order, coustomer, suggested, issued_book, coustomers
import random
from dotenv import load_dotenv
import os

load_dotenv()

def send_otp(contact):
        account_sid = os.getenv('ACf7119d5eb12735c120762192e130a40d')
        auth_token =  os.getenv('52cdad05c282c820791f3ceb45ed3999')
        Client = Client(account_sid, auth_token)

        otp = random.randint(100000, 999999)
        message = Client.messages.create(
            body=f'Your OTP is {otp}, please do not share it with anyone.',
            from_='+7607846008',
            to="+91" + contact

        )
        return otp

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
        pname = request.POST['product_name']
        pcategory = request.POST['product_category']
        pdescription = request.POST['product_description']
        price = request.POST['price']
        file = request.FILES['image']
        product_detail(product_name=pname, product_category=pcategory, product_description=pdescription, price=price, image=file).save()
        msg = "Product added"
        return render(request, 'admin/add_product.html', {'msg': msg})
    return render(request, 'admin/add_product.html')

def view_products(request):
    data = product_detail.objects.all()
    return render(request, 'admin/view_product.html', {'data': data})

def view_issued_book(request):
    data = issued_book.objects.all()
    return render(request, 'admin/view_issued_books.html', {'data': data})

def view_customer(request):
    data = coustomer.objects.all()
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
    data = product_detail.objects.all()
    return render(request, 'book.html', {'data': data})


def issue_books(request):
    data = product_detail.objects.all()
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
                book = product_detail.objects.get(id=book_id)
                user = coustomer.objects.get(contact=register_number)
                issued_book.objects.create(
                    book_name=book.product_name,
                    book_category=book.product_category,
                    name=user.name,
                    contact=user.contact
                )
                msg = f"Book '{book.product_name}' issued successfully."
            except product_detail.DoesNotExist:
                msg = "Book not found."
            except coustomer.DoesNotExist:
                msg = "User not found."
        else:
            msg = "Invalid request."
        data = product_detail.objects.all()
        return render(request, 'issue.html', {'data': data, 'msg': msg})
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            data = product_detail.objects.filter(
                coustomer(product_name__icontains=search_query) |
                coustomer(product_category__icontains=search_query)
            )
        else:
            data = product_detail.objects.all()
        return render(request, 'issue.html', {'data': data})

def issue_book(request):
    if request.method=="POST":
        name=request.POST['name']
        email_id=request.POST['email']
        if coustomer.objects.filter(email=email_id,name=name):
            data=coustomer.objects.filter(email=email_id,name=name).get()
            return redirect('book.html')
        else:
            msg="Invalid name or email"
            return render(request,'issue.html',{'msg':msg})
    return render(request,'issue.html')



def books(request):
    data = product_detail.objects.all()
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
     if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        contact=request.POST['contact']

        if coustomer.objects.filter(email=email, contact=contact).exists():
            msg = "You are already a member"
            return render(request, 'membership.html', {'msg': msg})
        
        if coustomer.objects.filter(name=name).exists():
            msg = "You are already a member"
            return render(request, 'membership.html', {'msg': msg})
        if coustomer.objects.filter(contact=contact).exists():
            msg = "You are already a member"
            return render(request, 'membership.html', {'msg': msg})

        user = coustomer.objects.filter(name=name,email=email,contact=contact, is_active=False)
        return render(request, 'verify.html', {'contact': contact})
     
     if request.user.is_authenticated:
        return redirect('membership')
     return render(request,'membership.html')


def otp_verify(request):
    if request.method == 'POST':
        contacts = request.POST.get('contact')
        otp = request.POST.get('otp')
        try:
            otp_obj = coustomers.objects.get(contact=contacts, otp=otp)

            if otp_obj.is_expired():
                messages.error(request,"OTP has expired. Please request a new OTP.")
                return redirect('verify_otp')
            if otp_obj.otp == otp:
                user = coustomers.objects.get(contact=contacts)
                otp_obj.is_active = True
                otp_obj.save()
                otp_obj.delete()  # Delete the OTP after successful verification
                messages.success(request, "OTP verified successfully.")
                request.session['register_number'] = contacts
                return redirect('membership.html')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
                return redirect('verify_otp')   
            
        except coustomers.DoesNotExist:
            messages.error(request, "Invalid contact number or OTP. Please try again.")
            return redirect('membership')
    return render(request, 'verify.html')
            


def logins(request):
    if request.method=="POST":
        name=request.POST['name']
        email_id=request.POST['email']
        if coustomer.objects.filter(email=email_id,name=name):
            data=coustomer.objects.filter(email=email_id,name=name).get()
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


