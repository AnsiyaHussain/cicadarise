from django.contrib import admin
from .models import Category, Products, Customer, Order, OrderItem, ContactMessage, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'image')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    ordering = ('-id',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ('order_number', 'customer', 'total_price', 'status', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('order_number', 'customer__email', 'customer__first_name')
    ordering      = ('-created_at',)
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    inlines       = [OrderItemInline]
    list_editable = ('status',)   # Change order status directly from list view


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display  = ('user', 'product', 'added_at')
    search_fields = ('user__email', 'product__name')
    ordering      = ('-added_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering      = ('-created_at',)
    readonly_fields = ('created_at',)