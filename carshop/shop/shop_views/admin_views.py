from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.db.models import Sum
from ..models import Product, Supplier, Sale

# Проверка: доступ только для администратора
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin_statistics(request):
    """
    Статистика для администратора.
    """
    # Статистика по товарам
    total_products = Product.objects.count()
    total_suppliers = Supplier.objects.count()

    # Статистика по продажам
    total_sales = Sale.objects.count()
    total_revenue = Sale.objects.aggregate(revenue=Sum('quantity') * Sum('unit_price'))['revenue'] or 0

    return render(request, 'shop/admin_statistics.html', {
        'total_products': total_products,
        'total_suppliers': total_suppliers,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
    })
