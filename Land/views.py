from datetime import date
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib import messages
from.models import add_category,Issue, Blog, Event, Team, User, suggested, issued_book, otp, Contact, Book, PreBooking, Donation
# Remove import of django.contrib.auth.models.User
# from django.contrib.auth.models import User
from .models import User, UserQR
import json, qrcode, io, os, uuid, razorpay
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
# Excel
from openpyxl import Workbook
# PDF
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.

#admin views

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def add_products(request):
    excel_msg = ''
    if request.method == "POST":
        if 'upload_excel' in request.POST:
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                excel_msg = "No file selected."
                return render(request, 'admin/add_product.html', {'excel_msg': excel_msg})
            try:
                import openpyxl
                wb = openpyxl.load_workbook(excel_file)
                sheet = wb.active
                imported_count = 0
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    title, category, sub_category, language, price, author, available_copies = row
                    if not title:
                        continue
                    book, created = Book.objects.update_or_create(
                        title=title,
                        defaults={
                            'category': category or '',
                            'sub_category': sub_category or 'General',
                            'language': language or '',
                            'price': str(price) if price is not None else '',
                            'author': author or '',
                            'available_copies': int(available_copies) if available_copies else 1,
                        }
                    )
                    if created:
                        imported_count += 1
                excel_msg = f"Imported or updated {imported_count} books from Excel file."
            except Exception as e:
                excel_msg = f"Error processing Excel file: {str(e)}"
            return render(request, 'admin/add_product.html', {'excel_msg': excel_msg})
        else:
            bname = request.POST['book_name']
            bcategory = request.POST['book_category']
            sbcategory = request.POST['book_sub-category']
            language = request.POST['book_language']
            price = request.POST['price']
            author = request.POST['author']
            available_copies = request.POST['book_available-copies']
            # Check if book with same title already exists
            if Book.objects.filter(title=bname).exists():
                msg = "Book with this title already exists."
                return render(request, 'admin/add_product.html', {'msg': msg})
            # Use the correct model Book instead of book_detail
            Book(
                title=bname,
                category=bcategory,
                sub_category=sbcategory,
                language=language,
                price=price,
                author=author,
                available_copies=available_copies
            ).save()
            msg = "Book added"
            return render(request, 'admin/add_product.html', {'msg': msg})
    return render(request, 'admin/add_product.html')

def view_products(request):
    data = Book.objects.all()
    return render(request, 'admin/view_product.html', {'data': data})

def view_issued_book(request):
    data = issued_book.objects.all()
    return render(request, 'admin/view_issued_books.html', {'data': data})

def view_customer(request):
    data = User.objects.all()
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
    current_user = request.user
    user_id = current_user.id
    print(user_id)  
    return render(request, 'user/user_dashboard.html')

def view_books(request):
    data = Book.objects.all()
    return render(request, 'book.html', {'data': data})


def about(request):
    return render(request, 'about.html')


def event(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events.html', {'events': events})


@csrf_protect
def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and phone and message:
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            msg = "Thank you for your feedback!"
            return render(request, 'contact.html', {'msg': msg})
        else:
            error = "Please fill in all fields."
            return render(request, 'contact.html', {'error': error})
    else:
        return render(request, 'contact.html')

@login_required
def feedback(request):
    contacts = Contact.objects.all().order_by('-submitted_at')
    return render(request, 'admin/feedback.html', {'contacts': contacts})


def donations(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        age = request.POST.get("age")
        mobile_number = request.POST.get("mobile_number")
        email = request.POST.get("email")
        address = request.POST.get("address")
        purpose = request.POST.get("purpose")
        book_name = request.POST.get("book_name")
        number_of_books = request.POST.get("number_of_books")
        agree = request.POST.get("agree")

        if not agree:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'donation.html', {'error': 'You must agree to the terms and conditions.'})

        Donation.objects.create(
            full_name=full_name,
            age=age,
            mobile_number=mobile_number,
            email=email,
            address=address,
            purpose=purpose,
            book_name=book_name,
            number_of_books=number_of_books
        )
        msg = "Thank you for your donation!"
        return render(request, 'donation.html', {'msg': msg})
    else:
        return render(request, 'donation.html')

@require_http_methods(["GET"])

def donated(request):
    donations = Donation.objects.all().order_by('-submitted_at')
    return render(request, 'admin/donated.html', {'donations': donations})

@login_required
def issue_books(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'manual_issue':
            # Handle manual issue form
            book_id = request.POST.get('book_id')
            issue_date_str = request.POST.get('issue_date')
            return_date_str = request.POST.get('return_date')
            datestart_str = request.POST.get('datestart')
            is_returned = request.POST.get('is_returned') == 'on'
            reissued = request.POST.get('reissued') == 'on'

            if book_id and issue_date_str and datestart_str:
                try:
                    book = Book.objects.get(id=book_id)
                    custom_user = User.objects.get(email=request.user.email)

                    from datetime import datetime
                    issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
                    datestart = datetime.strptime(datestart_str, '%Y-%m-%dT%H:%M')
                    return_date = None
                    if return_date_str:
                        return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

                    Issue.objects.create(
                        user=custom_user,
                        book=book,
                        issue_date=issue_date,
                        return_date=return_date,
                        is_returned=is_returned,
                        reissued=reissued,
                        datestart=datestart
                    )

                    if not is_returned:
                        book.available_copies -= 1
                        book.save()

                    messages.success(request, f"Issue for '{book.title}' created successfully.")
                except Book.DoesNotExist:
                    messages.error(request, "Book not found.")
                except User.DoesNotExist:
                    messages.error(request, "User not found.")
                except ValueError:
                    messages.error(request, "Invalid date format.")
            else:
                messages.error(request, "All required fields must be filled.")
        else:
            # Handle original issue form
            book_id = request.POST.get('book_id')
            if book_id:
                try:
                    book = Book.objects.get(id=book_id)
                    # Get the custom User instance corresponding to the logged-in user
                    try:
                        custom_user = User.objects.get(email=request.user.email)
                    except User.DoesNotExist:
                        messages.error(request, "User not found in custom user model.")
                        return redirect('issue book')
                    # Check if book is already issued and not returned
                    if Issue.objects.filter(book=book, is_returned=False).exists():
                        messages.error(request, "Book is already issued to someone else.")
                        return redirect('issue book')
                    # Check if pre-booked by another user
                    if PreBooking.objects.filter(book=book).exclude(user=custom_user).exists():
                        messages.error(request, "Book is pre-booked by another user. Cannot issue.")
                        return redirect('issue book')
                    Issue.objects.create(
                        user=custom_user,
                        book=book
                    )
                    book.available_copies -= 1
                    book.save()
                    messages.success(request, f"Book '{book.title}' issued successfully for 15 days.")
                except Book.DoesNotExist:
                    messages.error(request, "Book not found.")
            else:
                messages.error(request, "Invalid request.")
        return redirect('user_dashboard')
    else:
        search_query = request.GET.get('search', '')
        if search_query:
            data = Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query)
            )
        else:
            data = Book.objects.all()
        # Get the custom User instance
        try:
            custom_user = User.objects.get(email=request.user.email)
            issues = Issue.objects.filter(user=custom_user).order_by('-issue_date')
        except User.DoesNotExist:
            issues = []
        template = 'user/issue book.html' if request.resolver_match.url_name == 'issue book' else 'user/issue.html'
        return render(request, template, {'data': data, 'issues': issues})

@login_required
def reissue_book(request, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id, user=request.user)
        if issue.can_reissue():
            # Reissue: extend due date by 15 days
            issue.issue_date = timezone.now().date()
            issue.reissued = True
            issue.save()
            messages.success(request, f"Book '{issue.book.title}' reissued successfully for another 15 days.")
        else:
            messages.error(request, "Reissue not allowed. Check conditions.")
    except Issue.DoesNotExist:
        messages.error(request, "Issue not found.")
    return redirect('user_dashboard')

from django.core.paginator import Paginator
from collections import defaultdict

def books(request):
    category_filter = request.GET.get('category', None)
    search_query = request.GET.get('q', '')

    books_qs = Book.objects.all()

    if category_filter and category_filter.lower() != 'all':
        books_qs = books_qs.filter(category__iexact=category_filter)

    if search_query:
        books_qs = books_qs.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    paginator = Paginator(books_qs, 12)  # 12 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Book.objects.values_list('category', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'categories': all_categories,
        'selected_category': category_filter or 'All',
        'search_query': search_query,
    }
    return render(request, 'books.html', context)

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






# 🔸 Show QR code page
def qr_code_page(request):
    return render(request, "qr.html") 

# 🔸 Generate QR code image dynamically
def generate_qr(request):
    user_qr = UserQR.objects.get(user=request.user)
    qr = qrcode.make(user_qr.qr_secret)
    buffer = User.name()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
            


def logins(request):
    if request.method=="POST":
        name=request.POST['name']
        email_id=request.POST['email']
        if User.objects.filter(email=email_id,name=name):
            data=User.objects.filter(email=email_id,name=name).get()
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







def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, "blog_list.html", {"blogs": blogs})


# @staff_member_required   # ✅ Only staff/admin users can access
def write_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        if title and content:
            Blog.objects.create(
                title=title,
                content=content,
                image=image
            )
            messages.success(request, "✅ Blog submitted successfully!")
            return redirect("blog_list")
        else:
            messages.error(request, "❌ Title and content are required.")

    return render(request, "admin/write_blog.html")

def add_event(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        image = request.FILES.get("image")

        if title and description and date:
            Event.objects.create(
                title=title,
                description=description,
                date=date,
                image=image
            )
            messages.success(request, "✅ Event added successfully!")
            return redirect("events")
        else:
            messages.error(request, "❌ Title, description, and date are required.")

    return render(request, "admin/event.html")


def index(request):
    blogs = Blog.objects.all().order_by('-created_at')
    events = Event.objects.all()
    team = Team.objects.all()

    context = {
        'blogs': blogs,
        'events': events,
        'team': team,
    }
    return render(request, 'index.html', context)





def payment_page(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Example: create an order
    order_amount = 50000  # amount in paise (₹500)
    order_currency = 'INR'
    order_receipt = 'order_rcptid_11'

    order = client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1'
    })

    context = {
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
        'amount': order_amount,
        'currency': order_currency
    }
    return render(request, 'payment.html', context)




@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            })
            return JsonResponse({"status": "Payment Successful"})
        except:
            return JsonResponse({"status": "Payment Failed"})




@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies > 0:
        Issue.objects.create(user=request.user, book=book)
        book.available_copies -= 1
        book.save()
    return redirect("issue")


@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, user=request.user)
    if not issue.is_returned:
        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()
        # Increase available copies
        issue.book.available_copies += 1
        issue.book.save()
        messages.success(request, f"Book '{issue.book.title}' returned successfully.")
    else:
        messages.error(request, "Book is already returned.")
    return redirect('my_issues')

@login_required
def my_issues(request):
    issues = Issue.objects.filter(user=request.user).order_by('-issue_date')
    return render(request, "my_issue.html", {"issue": issues})

def memberships(request):
    return render(request, 'membership.html')

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

from django.db import IntegrityError

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        aadhaar = request.POST.get('aadhaar')
        address = request.POST.get('address')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'membership.html', {'error': 'You must agree to the terms and conditions.'})

        if name and email and phone and aadhaar and address:
            # Check if contact already exists
            if User.objects.filter(contact=phone).exists():
                messages.error(request, "This Phone number is already registered.")
                return render(request, 'membership.html', {'error': 'This phone number is already registered.'})
            if User.objects.filter(email=email).exists():
                messages.error(request, "This Email is already registered.")
                return render(request, 'membership.html', {'error': 'This email is already registered.'})
            if User.objects.filter(adhaar_no=aadhaar).exists():
                messages.error(request, "This Aadhaar number is already registered.")
                return render(request, 'membership.html', {'error': 'This aadhaar is already registered.'})

            try:
                # Create User instance
                user = User(
                    name=name,
                    email=email,
                    contact=phone,
                    adhaar_no=aadhaar,
                    address=address,
                    user_type='User',  # Assuming default user type
                    is_active=True
                )
                user.save()

                # Generate QR code
                qr_data = f"{user.name}-{user.id}-{uuid.uuid4()}"
                qr = qrcode.make(qr_data)
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                buffer.seek(0)

                # Save QR code image
                filename = f"{user.name}_{user.id}.png"
                user.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

                messages.success(request, "Signup successful! Your QR code has been generated.")
                return redirect('index')  # Redirect to login page
            except IntegrityError:
                messages.error(request, "A user with this phone number already exists.")
                return render(request, 'membership.html', {'error': 'A user with this phone number already exists.'})
        else:
            messages.error(request, "All fields are required.")
            return render(request, 'membership.html', {'error': 'All fields are required.'})
    else:
        return render(request, 'membership.html')
