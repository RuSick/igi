from django.urls import path
from .shop_views import views, admin_views, accounts_view, cart_views

urlpatterns = [
    path('admin/statistics/', admin_views.admin_statistics, name='admin_statistics'),
    path('products/', views.public_products_view, name='public_products'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  # Read: Просмотр товара
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),  # Delete: Удалить товар
    path('products/create/', views.product_create, name='product_create'),  # Добавление товара
    path('products/<int:pk>/update/', views.product_update, name='product_update'),  # Редактирование товара
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path("signup/", accounts_view.signup_view, name="signup"),  # Маршрут для регистрации
    path('cart/', cart_views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', cart_views.remove_from_cart, name='remove_from_cart'), 
    path('cart/increase/<int:cart_item_id>/', cart_views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:cart_item_id>/', cart_views.decrease_quantity, name='decrease_quantity'),
    path('cart/checkout/', cart_views.checkout, name='checkout'),

]
