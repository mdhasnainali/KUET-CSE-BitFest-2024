from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import BASE_DIR from settings
from mofas_kitchen_buddy.settings import BASE_DIR

# For Reading the text file
def parse_recipes_file(file_path):
    recipes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        recipe = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Recipe:"):
                if recipe:
                    recipes.append(recipe)
                recipe = {'name': line.split(":")[1].strip()}
            elif line.startswith("Taste:"):
                recipe['taste'] = line.split(":")[1].strip()
            elif line.startswith("Cuisine Type:"):
                recipe['cuisine_type'] = line.split(":")[1].strip()
            elif line.startswith("Preparation Time:"):
                recipe['preparation_time'] = line.split(":")[1].strip()
            elif line.startswith("Reviews:"):
                recipe['reviews'] = int(line.split(":")[1].strip())
        if recipe:
            recipes.append(recipe)
    return recipes

class RecipeListView(APIView):
    def get(self, request):
        file_path = BASE_DIR.parent / "recipes.txt"
        recipes = parse_recipes_file(file_path)
        return Response(recipes, status=status.HTTP_200_OK)