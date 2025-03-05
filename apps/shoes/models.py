from django.db import models

class Shoes(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='shoes/')
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title  
    
    class Meta:
        verbose_name = 'Shoes'
        verbose_name_plural = 'Shoes'