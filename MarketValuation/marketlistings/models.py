from django.db import models

# Create your models here.
class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('hos', 'House'),
        ('apt', 'Apartment'),
        ('cdm', 'Condominium'),
        ('cml', 'Commercial'),
    ]
    
    description = models.TextField()
    address = models.CharField(max_length = 255)
    category = models.CharField(max_length = 3, choices = CATEGORY_CHOICES)
    land_size = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    building_size = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    bedrooms = models.IntegerField(null = True, blank = True)
    bathrooms = models.IntegerField(null = True, blank = True)
    latitude = models.DecimalField(max_digits = 12, decimal_places = 5, null = True, blank = True)
    longitude = models.DecimalField(max_digits = 12, decimal_places = 5, null = True, blank = True)
    price = models.DecimalField(max_digits = 12, decimal_places = 2, null = True, blank = True)


    def __str__(self):
        return f"{ self.description } - { self.price } ({ self.category })"
