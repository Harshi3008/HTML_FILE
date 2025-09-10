from django.contrib import admin
from.models import User,Blog, Event,Book, Issue, Team, add_category, suggested, issued_book, UserQR, otp, Donation
# Register your models here.
class UserRegister(admin.ModelAdmin):
    list_display=["email"]
admin.site.register(User,UserRegister)

class category_register(admin.ModelAdmin):
    list_display=["category_name"]
admin.site.register(add_category,category_register)

class book_register(admin.ModelAdmin):
    list_display=["title"]
admin.site.register(Book,book_register)

class issued(admin.ModelAdmin):
    list_display=["name"]
admin.site.register(issued_book,issued)


class suggestions(admin.ModelAdmin):
    list_display=['book_name']
admin.site.register(suggested,suggestions)

class otps(admin.ModelAdmin):
    list_display=["contact"]
admin.site.register(otp,otps)

class title(admin.ModelAdmin):
    list_display=["title"]
admin.site.register(Blog, title)

class qr(admin.ModelAdmin):
    list_display=["user"]
admin.site.register(UserQR, qr)

class events(admin.ModelAdmin):
    list_display=["title"]
admin.site.register(Event, events)

class name(admin.ModelAdmin):
    list_display=["name"]
admin.site.register(Team, name)

class donate(admin.ModelAdmin):
    list_display=["email"]
admin.site.register(Donation,donate)


class issued(admin.ModelAdmin):
    list_display=["user"]
admin.site.register(Issue, issued)

