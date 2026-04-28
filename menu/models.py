from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    image = models.CharField(max_length=300, blank=True, default='https://via.placeholder.com/300x200?text=Food')
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category__order', 'name']

    def __str__(self):
        return self.name

class Reservation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField(default=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    pickup_time = models.TimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"
