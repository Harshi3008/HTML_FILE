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
    path('contributions', views.contribution, name='contributions'),
    path('membership', views.memberships, name='membership'),
    path('book', views.books, name='book'),
    path('review', views.reviews, name='review'),




    path('admin_dashboard',views.admin_dashboards,name='admin_dashboard'),
    path('add_category',views.add_categorys,name='add category'),
    path('view category',views.view_category,name='view category'),
    path('add product',views.add_products,name='add product'),
    path('view product',views.view_products,name='view product'),
    path('view issued_book',views.view_issued_book,name='view issued_book'),
    path('view customer',views.view_customer,name='view customer'),
    path('password update',views.password_update,name='password update'),
    path('logout',views.logout,name='logout'),
    path('suggested book',views.suggested_book,name='suggested book'),

    
    path('user_dashboard',views.user_dashboards,name='user_dashboard'),
    path('issue_book',views.issue_books,name='issue book'),
    path('view book',views.view_books,name='view book'),
    path('upload suggested_book',views.upload_suggested_book,name='upload suggested book'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
