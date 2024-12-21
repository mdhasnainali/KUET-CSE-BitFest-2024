from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mofas_kitchen_buddy.settings import BASE_DIR
from .serializers import RecipeSerializer, ImageSerializer
from ingredient_manager.models import Ingredient
import requests
from .ocr import extract_text_from_image


# For Reading the text file
def parse_recipes_file(file_path):
    recipes = []
    count = 0
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            recipe = {}
            for line in lines:
                line = line.strip()
                if line.startswith("Recipe:"):
                    if recipe:
                        count += 1
                        recipe["id"] = count
                        recipes.append(recipe)
                    recipe = {"name": line.split(":")[1].strip()}
                elif line.startswith("Taste:"):
                    recipe["taste"] = line.split(":")[1].strip()
                elif line.startswith("Cuisine Type:"):
                    recipe["cuisine_type"] = line.split(":")[1].strip()
                elif line.startswith("Preparation Time:"):
                    recipe["preparation_time"] = line.split(":")[1].strip()
                elif line.startswith("Reviews:"):
                    recipe["reviews"] = int(line.split(":")[1].strip())

            # Append the last recipe
            if recipe:
                count += 1
                recipe["id"] = count
                recipes.append(recipe)
    except FileNotFoundError:
        raise FileNotFoundError("Recipes file not found")
    return recipes


class RecipeListView(APIView):
    """
    API endpoint that allows recipes to be viewed and added.
    """

    def get(self, request):
        try:
            # Path to your recipes text file
            file_path = BASE_DIR.parent / "my_fav_recipes.txt"
            recipes = parse_recipes_file(file_path)
        except FileNotFoundError:
            return Response(
                {"message": "Recipes file not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(recipes, status=status.HTTP_200_OK)

    def post(self, request):
        # Validate the data using the serializer
        if "ocr" in request.query_params:
            serializer = ImageSerializer(data=request.data)
            if serializer.is_valid():
                image = serializer.validated_data["image_url"]
                api_key = "API_KEY"
                response = extract_text_from_image(image, api_key)
                print(response)
                if response == "ERROR":
                    return Response(
                        {"message": "Not enough information to provide a recipe"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Write the response to the file
                try:
                    file_path = BASE_DIR.parent / "my_fav_recipes.txt"
                    with open(file_path, "a") as file:
                        recipe_content = response["choices"][0]["message"]["content"]
                        file.write(f"{recipe_content}\n")

                    return Response(
                        {
                            "message": "Recipe added successfully",
                            "extracted_text": recipe_content,
                        },
                        status=status.HTTP_201_CREATED,
                    )

                except Exception as e:
                    return Response(
                        {"message": f"Error writing to file: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe = serializer.validated_data

            try:
                file_path = BASE_DIR.parent / "my_fav_recipes.txt"
                # Append the new recipe to the file
                with open(file_path, "a") as file:
                    file.write(f"Recipe: {recipe['name']}\n")
                    file.write(f"Taste: {recipe['taste']}\n")
                    file.write(f"Cuisine Type: {recipe['cuisine_type']}\n")
                    file.write(f"Preparation Time: {recipe['preparation_time']}\n")
                    file.write(f"Reviews: {recipe['reviews']}\n\n")
            except Exception as e:
                return Response(
                    {"message": f"Error writing to file: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": "Recipe added successfully"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatBotView(APIView):
    """
    API endpoint that allows chatbot combine the ingredients, recipe and instructions to generate a recipe.
    """

    def get_prompt(self, message):
        ingredients = Ingredient.objects.all()

        if len(ingredients) == 0:
            return Response(
                {"message": "Sorry, you don't have any ingredients yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Prompt for the Gemini API
        prompt = (
            "Suppose you are a chef, and you have the following ingredients: \n```\n"
        )
        for ingredient in ingredients:
            prompt += f"ingredient name: {ingredient.ingredient_name} - quantity: {ingredient.quantity} {ingredient.unit}, price: {ingredient.price}\n"

        prompt += "```\n"
        prompt += f"and you want to make a recipe based on the following message: ```{message}``` \n"
        prompt += "and you know these recipes: ```\n"
        file_path = BASE_DIR.parent / "my_fav_recipes.txt"
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                prompt += f"{line}"

        prompt += "```\n"
        prompt += "Please generate a recipe based on the above information. The response will be in plain text format, simple and easy to understand. Dont use markdown, try to use line breaks for better readability."
        return prompt

    def post(self, request):
        data = request.data
        message = data.get("message")

        if not message:
            return Response(
                {"message": "Please provide a message for the chatbot"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Gemini API endpoint
        gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        api_key = "API_KEY"
        headers = {"Content-Type": "application/json"}

        message = self.get_prompt(message)
        print(message)
        payload = {"contents": [{"parts": [{"text": message}]}]}

        try:
            # Send request to Gemini API
            response = requests.post(
                f"{gemini_api_url}?key={api_key}", json=payload, headers=headers
            )
            response_data = response.json()

            if response.status_code == 200:
                reply = (
                    response_data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )
                return Response({"message": reply}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": response_data.get("error", "Unknown error occurred.")},
                    status=response.status_code,
                )
        except requests.RequestException as e:
            return Response(
                {"error": "Failed to connect to Gemini API", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
