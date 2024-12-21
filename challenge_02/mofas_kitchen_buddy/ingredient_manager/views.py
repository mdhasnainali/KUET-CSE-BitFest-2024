from .models import Ingredient
from .serializers import IngredientSerializer
from rest_framework.views import APIView, Response


# Crud Operation for Managing Ingredients
class IngredientView(APIView):
    def get(self, request):
        if "id" in request.query_params:
            ingredient = Ingredient.objects.filter(id=request.query_params["id"])
            if not ingredient:
                return Response({"message": "Ingredient not found"}, status=404)
            
            ingredient = ingredient.first()
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data)

        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        ingredient = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):        
        ingredient = Ingredient.objects.filter(pk=pk)
        if not ingredient:
            return Response({"message": "Ingredient not found"}, status=404)
        ingredient = ingredient.first()
        ingredient.delete()
        return Response({"message": "Ingredient deleted successfully"}, status=204)
