from datetime import date
from django.shortcuts import render,redirect
from.models import add_category,product_detail, order, coustomer, suggested, issued_book
import random

# Create your views here.

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

def admin_dashboards(request):
    return render(request, 'admin/admin_dashboard.html') 

def add_products(request):
    if request.method=="POST":
        pname=request.POST['product_name']
        pcategory=request.POST['product_category']
        pdescription=request.POST['product_description']
        price=request.POST['price']
        file=request.FILES['image']
        product_detail(product_name=pname,product_category=pcategory,product_description=pdescription,price=price,image=file).save()
        msg="product added"
        return render(request,'admin/add_product.html',{'msg':msg})
    return render(request,'admin/add_product.html')

def view_products(request):
    data = product_detail.objects.all()
    print(len(data), data)
    return render(request,'admin/view_product.html',{'data':data})

def view_issued_book(request):
    data=issued_book.objects.all()
    return render(request, 'admin/view_issued_books.html',{'data':data}) 

def view_customer(request):
    data=coustomer.objects.all()
    return render(request, 'admin/view_subscription.html',{'data':data}) 



def suggested_book(request):
    if request.method=="POST":
        book_name=request.POST['book_name']
        book_author=request.POST['book_author']
        suggested(book_name=book_name,book_author=book_author).save()
        msg= "THANK YOU FOR SUGGESTING A BOOK"
        return render(request,'user/suggested_books.html',{'msg':msg})
    return render(request,'user/suggested_books.html')

def password_update(request):
    if request.method=="POST":
       email=request.POST['email']
       cpassword= request.POST['cpassword']
       npassword=request.POST['npassword']
       if coustomer.objects.filter(email=email,password=cpassword):
           coustomer.objects.filter(email=email,password=cpassword).update(password=npassword)
           msg="your password is succesfully updated"
           return render(request,'admin/password_update.html',{'msg':msg})
       else:
           msg="Wrong Password Entered"
           return render(request,'admin/password_update.html',{'msg':msg})
    return render(request, 'admin/password_update.html') 

def suggested_book(request):
    data=suggested.objects.all()
    return render(request,'admin/suggested_books.html',{'data':data})

def logout(request):
    return redirect('index')

# user

def user_dashboards(request):
    return render(request,'user/user_dashboard.html')

def view_books(request):
    data=product_detail.objects.all()
    return render(request,'book.html',{'data':data})

def upload_suggested_book(request):
    data=suggested.objects.all()
    return render(request,'user/upload_suggested_book.html',{'data':data})


def issue_books(request):
    data=product_detail.objects.all()
    return render(request,'user/issue_book.html',{'data':data})



#templates

def memberships(request):
    if request.method=="POST":
        email_id=request.POST['email']
        password=request.POST['password']
        if product_detail.objects.filter(email=email_id,password=password):
            data=product_detail.objects.filter(email=email_id,password=password).get()
            user_type=data.user_type
            if user_type=='Admin':
                request.session['email']=email_id
                return redirect('admin_dashboard')
            else:
                request.session['email']=email_id
                return redirect('user_dashboard')
        else:
            msg="Invalid email or password"
            return render(request,'membership.html',{'msg':msg})
    return render(request,'membership.html')


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def event(request):
    return render(request,'events.html')

def contacts(request):
    return render(request,'contact.html')


def contribution(request):
    return render(request,'contributions.html')


def issue_books(request):
    return render(request,'issue book.html')


def books(request):
    return render(request,'book.html')


def reviews(request):
    return render(request,'review.html')