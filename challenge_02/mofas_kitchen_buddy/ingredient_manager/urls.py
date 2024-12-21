from django.urls import path
from .views import IngredientView

urlpatterns = [
    path('', IngredientView.as_view(), name='ingredient-list'),
    path('<int:pk>', IngredientView.as_view(), name='ingredient-detail'),
]