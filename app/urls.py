from django.urls import path
from . import views

urlpatterns = [
    # Preloader - This must be the FIRST route for empty path
    path('', views.preloader, name='preloader'),

    # All other pages (moved down)
    path('index/', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('product/<int:product_id>/',   views.product,           name='product_detail'),
    path('contact/',                    views.contact,           name='contact'),
    path('search/',                     views.search,            name='search'),

    # Auth
    path('signup/',                     views.signup,            name='signup'),
    path('login/',                      views.login_view,        name='login'),
    path('logout/',                     views.logout_view,       name='logout'),
    path('my-account/',                 views.my_account,        name='my_account'),

    # Cart
    path('cart/',                       views.cart_view,         name='cart'),
    path('add-to-cart/',                views.add_to_cart,       name='add_to_cart'),
    path('update-cart/<int:product_id>/', views.update_cart,     name='update_cart'),

    # Checkout & Orders
    path('checkout/',                   views.checkout,          name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/',                  views.my_orders,         name='my_orders'),

    # Wishlist
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/',                   views.wishlist_view,     name='wishlist'),
]