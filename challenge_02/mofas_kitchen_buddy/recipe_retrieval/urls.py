from django.urls import path
from .views import IngredientView

urlpatterns = [
    path('recipes/', get_recipes, name='get_recipes'),
]
