from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=10, null=True)
    def __str__(self) -> str:
        return self.name
class Product(models.Model):
    CATEGORY = (
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=300, choices=CATEGORY)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tag = models.ManyToManyField(Tag)
    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered'),
        ('Canceled','Canceled'),
        )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL  ,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now=True,null=True)
    status = models.CharField(max_length=50, choices=STATUS)
    note = models.CharField(max_length=50, null=True)
    def __str__(self) -> str:
        return f"{self.product.name}--{self.customer.name}"