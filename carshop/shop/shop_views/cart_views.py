from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Cart, Product, Order

@login_required
def cart_view(request):
    """
    Отображение корзины пользователя.
    """
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def add_to_cart(request, product_id):
    """
    Добавление товара в корзину.
    """
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('public_products')

@login_required
def remove_from_cart(request, cart_item_id):
    """
    Удаление товара из корзины.
    """
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')
    
@login_required
def decrease_quantity(request, cart_item_id):
    # Получаем объект CartItem, принадлежащий текущему пользователю
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    
    # Если количество больше 1, уменьшаем его
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # Если количество становится 0, удаляем товар из корзины
        cart_item.delete()
    
    return redirect('cart_view')

def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(
        user=request.user,
        total_price=cart.get_total_price()  # Передаём сумму корзины
    )
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
    cart.items.all().delete()  # Очищаем корзину после оформления заказа
    return render(request, 'shop/order_confirmation.html', {'order': order})
