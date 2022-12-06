from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError


# Creating a Validator function for Stock
def validate_stock(value):
    if 0 < value < 1000:
        return value
    else:
        raise ValidationError("The Stock value should be between 0 and 1000")


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators=[validate_stock])
    available = models.BooleanField(default=True)
    optional = models.TextField(max_length=300, blank=True, default='')
    interested = models.PositiveIntegerField(default=0)

    def refill(self):
        return self.stock + 100

    def __str__(self):
        return self.name


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]
    company = models.CharField(max_length=50, blank=True, default='')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    ORDER_STATUS = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'OrderShipped'),
        (3, 'Order Delivered')
    ]
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=0)
    order_status = models.IntegerField(choices=ORDER_STATUS, default=1)
    status_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} => {self.client.company}"

    def __total_cost__(self):
        return Product.price * self.num_units
