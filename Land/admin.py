from django.contrib import admin
from.models import coustomer, add_category, book_detail, order, suggested, issued_book, UserQR, coustomers
# Register your models here.
class UserRegister(admin.ModelAdmin):
    list_display=["email"]
admin.site.register(coustomer,UserRegister)

class category_register(admin.ModelAdmin):
    list_display=["category_name"]
admin.site.register(add_category,category_register)

class book_register(admin.ModelAdmin):
    list_display=["book_name"]
admin.site.register(book_detail,book_register)

class issued(admin.ModelAdmin):
    list_display=["name"]
admin.site.register(issued_book,issued)


class order_detail(admin.ModelAdmin):
    list_display=['order_id']
admin.site.register(order,order_detail)

class suggestions(admin.ModelAdmin):
    list_display=['book_name']
admin.site.register(suggested,suggestions)

class otp(admin.ModelAdmin):
    list_display=["contact"]
admin.site.register(coustomers,otp)


class user(admin.ModelAdmin):
    list_display=["user"]
admin.site.register(UserQR, user)
