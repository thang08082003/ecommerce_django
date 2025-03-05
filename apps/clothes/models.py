from django.db import models
from django.utils import timezone

class Clothes(models.Model):
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='clothes/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Clothes'
        verbose_name_plural = 'Clothes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.brand} ({self.size})"