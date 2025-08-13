from django.contrib import admin
from.models import coustomer, add_category, product_detail, order, suggested, issued_book, coustomers
# Register your models here.
class UserRegister(admin.ModelAdmin):
    list_display=["email"]
admin.site.register(coustomer,UserRegister)

class category_register(admin.ModelAdmin):
    list_display=["category_name"]
admin.site.register(add_category,category_register)

class product_register(admin.ModelAdmin):
    list_display=["product_name"]
admin.site.register(product_detail,product_register)

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
