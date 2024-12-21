from ingredient_manager.models import Ingredient
from ingredient_manager.serializers import IngredientSerializer
from rest_framework.views import APIView, Response


# Crud Operation for Managing Ingredients
class IngredientView(APIView):
    def get(self, request):
        if "id" in request.query_params:
            ingredient = Ingredient.objects.get(pk=request.query_params["id"])
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
        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.delete()
        return Response({"message": "Ingredient deleted successfully"}, status=204)
