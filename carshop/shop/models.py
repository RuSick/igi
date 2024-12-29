from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    article = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def get_total_price(self):
        # Подсчёт общей суммы всех товаров в корзине
        return sum(item.product.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
# Create your models here.
