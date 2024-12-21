from django.urls import path
from ingredient_manager import IngredientView

urlpatterns = [
    path('', IngredientView.as_view(), name='ingredient-list'),
    path('<int:pk>', IngredientView.as_view(), name='ingredient-detail'),
]