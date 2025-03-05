from django.db import models
from apps.customer.models import Customer

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def __str__(self):
        return f"Cart for {self.customer.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', null=True, blank=True, on_delete=models.CASCADE)
    shoes = models.ForeignKey('shoes.Shoes', null=True, blank=True, on_delete=models.CASCADE)
    clothes = models.ForeignKey('clothes.Clothes', null=True, blank=True, on_delete=models.CASCADE)
    mobile = models.ForeignKey('mobiles.Mobile', null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_cartitem'

    def get_cost(self):
        if self.book:
            return self.quantity * self.book.price
        elif self.shoes:
            return self.quantity * self.shoes.price
        elif self.clothes:
            return self.quantity * self.clothes.price
        elif self.mobile:
            return self.quantity * self.mobile.price
        return 0
    
    def get_item(self):
        return self.book or self.shoes or self.clothes or self.mobile
    
    def get_title(self):
        item = self.get_item()
        return item.title if item else "Unknown Item"
    
    def get_type(self):
        if self.book:
            return 'book'
        elif self.shoes:
            return 'shoes'
        elif self.clothes:
            return 'clothes'
        elif self.mobile:
            return 'mobile'
        return 'unknown'
    
    def get_image_url(self):
        item = self.get_item()
        if not item:
            return None
        if self.book and hasattr(item, 'cover_image'):
            return item.cover_image.url
        elif hasattr(item, 'image'):
            return item.image.url
        return None

    def __str__(self):
        return f"{self.get_title()} ({self.quantity}x)"