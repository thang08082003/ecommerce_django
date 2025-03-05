from django.db import models
from apps.clothes.models import Clothes
from apps.customer.models import Customer
from apps.book.models import Book
from apps.shoes.models import Shoes
from apps.mobiles.models import Mobile

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered')
    ]

    SHIPPING_CHOICES = [
        ('standard', 'Standard (3-5 day)'),
        ('express', 'Express(1-2 day)'),
    ]
    
    PAYMENT_CHOICES = [
        ('cod', 'Cod'),
        ('bank', 'Bank'),
        ('credit', 'Credit'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.username}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_status_display_vietnamese(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    shoes = models.ForeignKey(Shoes, on_delete=models.SET_NULL, null=True, blank=True)
    clothes = models.ForeignKey(Clothes, on_delete=models.SET_NULL, null=True, blank=True)
    mobile = models.ForeignKey(Mobile, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_orderitem'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.get_title()}"

    def get_total(self):
        return self.quantity * self.price

    def get_item(self):
        return self.book or self.shoes or self.clothes or self.mobile

    def get_title(self):
        item = self.get_item()
        return item.title if item else "Deleted"

    def get_type(self):
        if self.book:
            return 'Book'
        elif self.shoes:
            return 'Shoe'
        elif self.clothes:
            return 'Clothe'
        elif self.mobile:
            return 'Mobile'
        return 'Unknown'

    def get_image_url(self):
        item = self.get_item()
        if not item:
            return None
        if self.book and hasattr(item, 'cover_image'):
            return item.cover_image.url
        elif hasattr(item, 'image'):
            return item.image.url
        return None

    def get_specs(self):
        if self.book:
            return f"Author: {self.book.author}"
        elif self.shoes:
            return f"Size: {self.shoes.size}"
        elif self.clothes:
            return f"Size: {self.clothes.size} | Color: {self.clothes.color}"
        elif self.mobile:
            return f"RAM: {self.mobile.ram} | ROM: {self.mobile.storage}"
        return ""