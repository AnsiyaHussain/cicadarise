from django.db import models
from django.contrib.auth.hashers import make_password
import datetime
import uuid


# ==================== CATEGORY ====================
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/categories/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# ==================== CUSTOMER ====================
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def register(self):
        self.password = make_password(self.password)
        self.save()

    class Meta:
        verbose_name_plural = "Customers"


# ==================== PRODUCTS ====================
class Products(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    image4 = models.ImageField(upload_to='uploads/products/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


# ==================== WISHLIST ====================
class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"


# ==================== ORDER ====================
def generate_order_number():
    return 'CR' + uuid.uuid4().hex[:8].upper()   # e.g. CR3F9A12B4


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, unique=True, default=generate_order_number)
    customer     = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    address      = models.CharField(max_length=300)
    city         = models.CharField(max_length=100, default='')
    state        = models.CharField(max_length=100, default='')
    pincode      = models.CharField(max_length=10, default='')
    phone        = models.CharField(max_length=15)
    total_price  = models.IntegerField(default=0)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} — {self.customer.email}"

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-created_at']


# ==================== ORDER ITEM ====================
class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price    = models.IntegerField()   # price at time of purchase

    def get_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        verbose_name_plural = "Order Items"


# ==================== CONTACT MESSAGE ====================
class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200, blank=True)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"