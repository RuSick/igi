from .models import Cart

def base_context(request):
    """
    Контекстный процессор для передачи количества товаров в корзине.
    """
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return {
        'cart_count': cart_count,
    }
