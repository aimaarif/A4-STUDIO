from django.contrib import admin
from .models import MainCategory, Category, Product, ContactMessage, Subscriber
# Register your models here.

admin.site.register(Subscriber)
admin.site.register(ContactMessage)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Product)
