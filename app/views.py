from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from .models import Products, Category, Customer, Order, OrderItem, ContactMessage, Wishlist
from .decorators import customer_login_required
import datetime

# ====================== PRELOADER ======================

def preloader(request):
    return render(request, 'preloader.html')


# ====================== HELPER FUNCTION ======================
def get_cart_and_wishlist(request):
    """Reusable function to get cart and wishlist count"""
    cart = request.session.get('cart', {})

    wishlist_count = 0
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(id=request.session['customer_id'])
            wishlist_count = Wishlist.objects.filter(user=customer).count()
        except Customer.DoesNotExist:
            del request.session['customer_id']  # Clean invalid session

    return cart, wishlist_count


# ====================== INDEX ======================
def index(request):
    cart, wishlist_count = get_cart_and_wishlist(request)

    categories = Category.objects.all()
    new_arrivals = Products.objects.all().order_by('-id')[:8]

    # Get list of product IDs that are already in the user's wishlist
    wishlist_product_ids = []
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(id=request.session['customer_id'])
            wishlist_product_ids = list(
                Wishlist.objects.filter(user=customer)
                .values_list('product_id', flat=True)
            )
        except Customer.DoesNotExist:
            del request.session['customer_id']

    category_id = request.GET.get('category')
    if category_id:
        products = Products.objects.filter(category_id=category_id).order_by('-id')
        current_category = get_object_or_404(Category, id=category_id)
    else:
        products = Products.objects.all().order_by('-id')
        current_category = None

    context = {
        'products': products,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'current_category': current_category,
        'cart': cart,
        'wishlist_count': wishlist_count,
        'wishlist_product_ids': wishlist_product_ids,   # This is the key line
    }
    return render(request, 'index.html', context)

    
# ====================== SHOP ======================
def shop(request):
    cart, wishlist_count = get_cart_and_wishlist(request)

    categories = Category.objects.all()
    products = Products.objects.all().order_by('-id')

    if request.GET.get('category'):
        products = products.filter(category_id=request.GET.get('category'))
    if request.GET.get('q'):
        products = products.filter(name__icontains=request.GET.get('q'))

    context = {
        'products': products,
        'categories': categories,
        'cart': cart,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'shop.html', context)


# ====================== ABOUT ======================
def about(request):
    cart, wishlist_count = get_cart_and_wishlist(request)
    return render(request, 'about.html', {
        'cart': cart,
        'wishlist_count': wishlist_count,
    })


# ====================== CONTACT ======================
def contact(request):
    cart, wishlist_count = get_cart_and_wishlist(request)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name, 
                email=email, 
                subject=subject or '', 
                message=message
            )
            # Use a custom tag so we can filter it later
            messages.success(request, 'Your message has been sent successfully!', extra_tags='contact')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill out all required fields.', extra_tags='contact')

    return render(request, 'contact.html', {
        'cart': cart,
        'wishlist_count': wishlist_count,
    })
# ====================== PRODUCT DETAIL ======================
def product(request, product_id=None):
    if not product_id:
        return redirect('shop')

    product_obj = get_object_or_404(Products, id=product_id)
    related_products = Products.objects.filter(category=product_obj.category).exclude(id=product_obj.id)[:4]

    cart, wishlist_count = get_cart_and_wishlist(request)

    # Wishlist check for this product
    wishlist_product_ids = []
    if 'customer_id' in request.session:
        try:
            customer = Customer.objects.get(id=request.session['customer_id'])
            wishlist_product_ids = list(Wishlist.objects.filter(user=customer).values_list('product_id', flat=True))
        except:
            pass

    return render(request, 'product.html', {
        'product': product_obj,
        'related_products': related_products,
        'cart': cart,
        'wishlist_count': wishlist_count,
        'wishlist_product_ids': wishlist_product_ids,
    })


# ====================== WISHLIST ======================
@customer_login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Products, id=product_id)
        customer = Customer.objects.get(id=request.session['customer_id'])

        wishlist_item, created = Wishlist.objects.get_or_create(user=customer, product=product)

        if created:
            return JsonResponse({'status': 'added', 'wishlist_count': Wishlist.objects.filter(user=customer).count()})
        else:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed', 'wishlist_count': Wishlist.objects.filter(user=customer).count()})

    return JsonResponse({'status': 'error'}, status=400)


@customer_login_required
def wishlist_view(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    wishlist_items = Wishlist.objects.filter(user=customer).select_related('product')
    
    return render(request, 'wishlist.html', {
        'products': [item.product for item in wishlist_items],
        'wishlist_count': wishlist_items.count(),
    })


# ====================== SIGNUP ======================
def signup(request):
    if request.method == 'POST':
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        phone           = request.POST.get('phone')
        email           = request.POST.get('email')
        password        = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if Customer.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered!', extra_tags='signup')
            return redirect('signup')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!', extra_tags='signup')
            return redirect('signup')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!', extra_tags='signup')
            return redirect('signup')

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email)
        customer.password = make_password(password)
        customer.save()

        messages.success(request, 'Account created successfully! Please login.', extra_tags='signup')
        return redirect('login')

    return render(request, 'signup.html')


# ====================== LOGIN ======================
def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()

        if customer and check_password(password, customer.password):
            request.session['customer_id'] = customer.id
            request.session.modified = True
            messages.success(request, f'Welcome back, {customer.first_name}!', extra_tags='login')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.', extra_tags='login')
            return redirect('login')

    return render(request, 'login.html')


# ====================== LOGOUT ======================
def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logged out successfully.', extra_tags='logout')
    return redirect('index')

# ====================== MY ACCOUNT ======================
@customer_login_required
def my_account(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    orders   = Order.objects.filter(customer=customer).prefetch_related('items__product')
    return render(request, 'my_account.html', {'customer': customer, 'orders': orders})


# ====================== SEARCH ======================
def search(request):
    query    = request.GET.get('q', '')
    products = Products.objects.filter(name__icontains=query) if query else Products.objects.all()
    return render(request, 'index.html', {'products': products, 'query': query})


# ====================== CART ======================
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity   = int(request.POST.get('quantity', 1))

        # === NEW: Check if user is logged in ===
        if 'customer_id' not in request.session:
            messages.warning(request, 'Please login to add items to your cart.')
            return redirect('login')   # Redirect to login page

        if product_id:
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + quantity
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Added to cart successfully!')
    
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def cart_view(request):
    cart        = request.session.get('cart', {})
    cart_items  = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product  = Products.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product':  product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Products.DoesNotExist:
            pass

    shipping    = 0 if total_price >= 2000 else 99
    grand_total = total_price + shipping

    return render(request, 'cart.html', {
        'cart_items':  cart_items,
        'total_price': total_price,
        'shipping':    shipping,
        'grand_total': grand_total,
    })


def update_cart(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart   = request.session.get('cart', {})
        pid    = str(product_id)

        if action == 'increase':
            cart[pid] = cart.get(pid, 0) + 1
        elif action == 'decrease':
            cart[pid] = cart.get(pid, 1) - 1
            if cart[pid] <= 0:
                del cart[pid]
        elif action == 'remove':
            cart.pop(pid, None)

        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

# ====================== CHECKOUT ======================

@customer_login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop')

    # Build cart items
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Products.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Products.DoesNotExist:
            continue

    shipping = 0 if total_price >= 2000 else 99
    grand_total = total_price + shipping

    customer = get_object_or_404(Customer, id=request.session['customer_id'])

    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')

        if not all([address, city, state, pincode, phone]):
            if not hasattr(request, 'checkout_messages'):
                request.checkout_messages = []
            request.checkout_messages.append(('error', 'Please fill in all delivery details.'))
            # Re-render the form with error
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'shipping': shipping,
                'grand_total': grand_total,
                'customer': customer,
            })

        # Create Order
        order = Order.objects.create(
            customer=customer,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            total_price=grand_total,
            status='pending',
        )

        # Create Order Items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
            )

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        # ==================== WHATSAPP INTEGRATION ====================
        import urllib.parse

        message = f"""* CICADA RISE *   

*Order ID:* `{order.order_number}`
*Customer:* {customer.first_name} {customer.last_name}
*Phone:* {phone}

*Ordered Items:*
"""
        for item in cart_items:
            message += f"• {item['product'].name} × {item['quantity']} = ₹{item['subtotal']}\n"

        message += f"""
*Total Amount:* *₹{grand_total}*

*Delivery Address:*
{address}
{city}, {state} - {pincode}

────────────────────
*Payment Instructions*

Please pay ₹{grand_total} using UPI.

📱 *Scan QR Code to Pay Instantly:*

👉 https://yourdomain.com/static/images/upi-qr.png

Or use UPI ID: `yourupi@okicici`

After payment, reply *PAID* + transaction screenshot.

We will confirm your order shortly.

Thank you for shopping with CICADA RISE ✨"""

        encoded_message = urllib.parse.quote(message)
        whatsapp_number = "8086273188"   # Change to your number

        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

        messages.success(request, f'Order #{order.order_number} placed! Redirecting to WhatsApp...')

        return redirect(whatsapp_url)

    # GET request - Show checkout form
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping': shipping,
        'grand_total': grand_total,
        'customer': customer,
    })


# ====================== ORDER CONFIRMATION ======================
@customer_login_required
def order_confirmation(request, order_number):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    order    = get_object_or_404(Order, order_number=order_number, customer=customer)
    return render(request, 'order_confirmation.html', {'order': order, 'customer': customer})


# ====================== MY ORDERS ======================
@customer_login_required
def my_orders(request):
    customer = get_object_or_404(Customer, id=request.session['customer_id'])
    orders   = Order.objects.filter(customer=customer).prefetch_related('items__product')
    return render(request, 'my_orders.html', {'orders': orders, 'customer': customer})
