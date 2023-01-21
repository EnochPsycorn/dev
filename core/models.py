from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    price = models.IntegerField(default=0, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    description = models.TextField(max_length=600, blank=False)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name

    def get_products_by_id(cart_product_id):
        return Product.objects.filter(id__in=cart_product_id)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def does_exits(self):
        return Customer.objects.filter(email=self.email)
        
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def get_order_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id)
