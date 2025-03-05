from django.db import models
from django.utils import timezone

class Mobile(models.Model):
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='mobiles/', null=True, blank=True)
    screen_size = models.CharField(max_length=50, default='6.1 inch')
    storage = models.CharField(max_length=50, default='128GB')
    ram = models.CharField(max_length=50, default='6GB')
    camera = models.CharField(max_length=100, default='12MP')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.title}"