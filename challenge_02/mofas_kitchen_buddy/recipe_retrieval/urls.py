from django.urls import path
from .views import RecipeListView, ChatBotView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('chat/', ChatBotView.as_view(), name='chat'),
]
