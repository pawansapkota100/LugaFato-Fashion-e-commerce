from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, default="null",unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100,default="null")
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image= models.ImageField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100,default="null")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    country=models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        products = ", ".join([item.product.name for item in self.orderitem_set.all()])
        return f"Order ID: {self.pk} - Customer: {self.customer.name} - Products: {products}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


class Message(models.Model):
    name= models.CharField(max_length=30)
    email= models.CharField(max_length=50)
    message=models.CharField( max_length=250)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.transaction_id
    
