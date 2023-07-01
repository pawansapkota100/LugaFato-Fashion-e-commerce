
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static


from database import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('shop/', views.shop, name="shop"),
    path('shop/', views.store, name="store"),
    path('product_details/<int:id>/',views.product, name="product"),

    path('product/<int:id>/', views.catagories,name="catagories"),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),


    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('checkout/', views.checkout, name="checkout"),
    # path('shopping_details/', views.checkout, name="shopping_details"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('error/', views.error_view, name='error'),
    path('shopping_details/', views.shopping_details, name='shopping_details'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)