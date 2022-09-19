from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MyWatchlist(models.Model):
    watched = models.BooleanField()
    title = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    release_date = models.DateField()
    review = models.TextField()