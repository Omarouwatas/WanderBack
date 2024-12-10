from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('adventure', 'Adventure'),
    ]

    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255) 
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    country = models.CharField(max_length=100)  # Pays
    city = models.CharField(max_length=100, blank=True, null=True)  
    facilities = models.JSONField(default=list) 
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  
    rating = models.FloatField(default=0.0)  
    image = models.ImageField(upload_to='places/', blank=True, null=True)  

    def __str__(self):
        return self.title



class Comment(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")  
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="comments")  
    content = models.TextField()  
    date_posted = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.place.title}"


User = get_user_model() 

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="favorited_by")
    date_added = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'place')  
        ordering = ['-date_added']  

    def __str__(self):
        return f"{self.user.username} -> {self.place.title}"
