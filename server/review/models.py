from django.db import models
from users.models import CustomUser

# Create your models here.
class Review(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  comment = models.CharField(max_length=1000)
  rating = models.IntegerField()
  reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)