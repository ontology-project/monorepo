from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Review(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  comment = models.CharField(max_length=1000)
  rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(4)])
  reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  query = models.CharField(max_length=1000)
  curriculum = models.CharField(max_length= 1000)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['reviewer', 'query'], name='unique_reviewer_query')
    ]
  
  def __str__(self):
    return f'Review by {self.reviewer} for {self.query} in curriculum {self.curriculum}'