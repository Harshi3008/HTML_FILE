from datetime import date
from django.shortcuts import render,redirect
from.models import add_category,product_detail, order, coustomer, suggested, issued_book, Membership
from .forms import MembershipForm
import random



# Create your views here.

def add_category(request):
    if request.method == "POST":
        cname = request.POST['category_name']
        add_category(category_name=cname).save()
        msg = "Category added"
        return render(request, 'admin/add_category.html', {'msg': msg})
    return render(request, 'admin/add_category.html')

def view_category(request):
    data = add_category.objects.all()
    return render(request, 'admin/view_category.html', {'data': data})

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

def suggested_book_post(request):
    if request.method == "POST":
        book_name = request.POST['book_name']
        book_author = request.POST['book_author']
        suggested(book_name=book_name, author_name=book_author).save()
        msg = "THANK YOU FOR SUGGESTING A BOOK"
        return render(request, 'user/suggested_books.html', {'msg': msg})
    return render(request, 'user/suggested_books.html')

def password_update(request):
    if request.method == "POST":
        email = request.POST['email']
        cpassword = request.POST['cpassword']
        npassword = request.POST['npassword']
        try:
            user = coustomer.objects.get(email=email)
            if user.password == cpassword:
                user.password = npassword
                user.save()
                msg = "Your password is successfully updated"
            else:
                msg = "Wrong Password Entered"
        except coustomer.DoesNotExist:
            msg = "User not found"
        return render(request, 'admin/password_update.html', {'msg': msg})
    return render(request, 'admin/password_update.html')

def suggested_book(request):
    data = suggested.objects.all()
    return render(request, 'admin/suggested_books.html', {'data': data})

def logout(request):
    return redirect('index')

def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')

def view_books(request):
    data = product_detail.objects.all()
    return render(request, 'book.html', {'data': data})

def upload_suggested_book(request):
    data = suggested.objects.all()
    return render(request, 'user/upload_suggested_book.html', {'data': data})

def issue_books(request):
    data = product_detail.objects.all()
    return render(request, 'user/issue_book.html', {'data': data})

def memberships(request):
    if request.method == "POST":
        email_id = request.POST['email']
        password = request.POST['password']
        try:
            user = coustomer.objects.get(email=email_id)
            if user.password == password:
                user_type = user.user_type
                if user_type == 'Admin':
                    request.session['email'] = email_id
                    return redirect('admin_dashboard')
                else:
                    request.session['email'] = email_id
                    return redirect('user_dashboard')
            else:
                msg = "Invalid email or password"
                return render(request, 'membership.html', {'msg': msg})
        except coustomer.DoesNotExist:
            msg = "Invalid email or password"
            return render(request, 'membership.html', {'msg': msg})
    return render(request, 'membership.html')

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
        return render(request, 'issue book.html', {'data': data, 'msg': msg})
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            data = product_detail.objects.filter(
                models.Q(product_name__icontains=search_query) |
                models.Q(product_category__icontains=search_query)
            )
        else:
            data = product_detail.objects.all()
        return render(request, 'issue book.html', {'data': data})

def books(request):
    data = product_detail.objects.all()
    return render(request, 'book.html', {'data': data})

def reviews(request):
    return render(request, 'review.html')

def issue_login(request):
    if request.method == 'POST':
        register_number = request.POST.get('register_number')
        try:
            user = coustomer.objects.get(contact=register_number)
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['register_number'] = register_number
            print(f"Sending OTP {otp} to {register_number}")
            return redirect('otp_verify')
        except coustomer.DoesNotExist:
            error = "Register number not found"
            return render(request, 'issue.html', {'error': error})
    else:
        return render(request, 'issue.html')

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

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        if not (name and email and contact and password):
            error = "Please fill all fields."
            return render(request, 'login.html', {'error': error, 'name': name, 'email': email, 'contact': contact})

        user = None
        try:
            user = coustomer.objects.get(email=email)
        except coustomer.DoesNotExist:
            try:
                user = coustomer.objects.get(contact=contact)
            except coustomer.DoesNotExist:
                user = None

        if user:
            if user.password == password:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('user_dashboard')
            else:
                error = "Incorrect password."
                return render(request, 'login.html', {'error': error, 'name': name, 'email': email, 'contact': contact})
        else:
            new_user = coustomer(name=name, email=email, contact=contact, password=password)
            new_user.save()
            request.session['user_id'] = new_user.id
            request.session['user_name'] = new_user.name
            return redirect('user_dashboard')
    else:
        return render(request, 'login.html')


def membership_view(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Membership form submitted successfully."
            form = MembershipForm()  # reset form after successful submission
            return render(request, 'membership.html', {'form': form, 'msg': msg})
        else:
            msg = "Please correct the errors below."
            return render(request, 'membership.html', {'form': form, 'msg': msg})
    else:
        form = MembershipForm()
    return render(request, 'membership.html', {'form': form})
