from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views


urlpatterns = [

    path("", views.index, name='index'),
    path('about', views.about, name='about'),
    path('events', views.event, name='events'),
    path('contact', views.contacts, name='contact'),
    path('donation', views.donations, name='donation'),
    path('membership', views.memberships, name='membership'),
    path('signup', views.signup, name='signup'),
    path('book', views.books, name='book'),
    path('team', views.team, name='team'),

    path('product', views.view_books, name='product'),
    path('review', views.reviews, name='review'),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('add product',views.add_products,name='add product'),
    path('view product',views.view_products,name='view product'),
    path('view issued_book',views.view_issued_book,name='view issued_book'),
    path('view customer',views.view_customer,name='view customer'),
    path('logout',views.logout,name='logout'),
    path('suggested book',views.suggested_book,name='suggested book'),
    path("event", views.add_event, name="event"),
    path('donated', views.donated, name='donated'),
    path('feedback', views.feedback, name='feedback'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('issue_book',views.issue_books,name='issue book'),
    path("my-issued-books/", views.my_issued_books, name="my_issued_books"),
    path("reissue/<int:issue_id>/", views.reissue_book, name="reissue_book"),
    path('view book',views.view_books,name='view book'),
    path('upload suggested_book',views.upload_suggested_books,name='upload suggested book'),
    path('issue', views.issue_books, name='issue'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
    path('login', views.logins, name='login'),
    path("write_blog", views.write_blog, name="write_blog"),
    path("blog_list", views.blog_list, name="blog_list"),
    path("my-qr", views.qr_code_page, name="qr"),
    path("generate-qr", views.generate_qr, name="generate_qr"),
    path("issues", views.my_issues, name="issues"),
    path("terms-and-conditions", views.terms_and_conditions, name="terms_and_conditions"),
    path("qr-login/", views.qr_login_page, name="qr_login_page"),
    path("qr-login-new/", views.qr_login_new, name="qr_login_new"),
    path("login-qr/", views.qr_login_verify, name="qr_login_verify"),
    path('login-qr', views.qr_login_verify, name='login-qr'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
