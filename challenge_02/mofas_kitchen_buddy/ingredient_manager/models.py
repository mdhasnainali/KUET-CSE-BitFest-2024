from django.db import models

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=255)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
