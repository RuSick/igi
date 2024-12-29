from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.core.paginator import Paginator

from ..forms import ProductForm
from ..models import Product, Supplier, Sale, Cart, Category

def is_superuser(user):
    return user.is_superuser

def is_staff(user):
    return user.groups.filter(name='Employee').exists()

def is_public_user(user):
    return user.groups.filter(name='User').exists()
# Только для админа

# Только для сотрудников
@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    sales = Sale.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'shop/staff_dashboard.html', {'sales': sales, 'suppliers': suppliers})

def public_products_view(request):

    # if request.user.is_authenticated:
    #     # Перенаправляем авторизованных пользователей, если это необходимо
    #     return redirect('some_other_view')

    # Получаем список всех товаров и категорий
    products = Product.objects.all()
    categories = Category.objects.all()

    # Получение параметров фильтрации из GET-запроса
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    category_id = request.GET.get('category', None)

    # Применение фильтров
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 10)  # Показывать 10 товаров на странице
    page_number = request.GET.get('page')  # Номер текущей страницы из параметра 'page'
    page_obj = paginator.get_page(page_number)  # Получение данных для текущей страницы

    # Возврат шаблона с контекстом 
    return render(request, 'shop/public_products.html', {
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
        'selected_category': int(category_id) if category_id else None,
        'page_obj': page_obj,
    })

#товары crud
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('public_products')
    else:
        form = ProductForm()
    return render(request, 'shop/product_create.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('public_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_update.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('public_products')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})


