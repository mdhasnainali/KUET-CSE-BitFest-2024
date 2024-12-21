from rest_framework import serializers

class RecipeSerializer(serializers.Serializer):
    name = serializers.CharField()
    taste = serializers.CharField()
    cuisine_type = serializers.CharField()
    preparation_time = serializers.CharField()
    reviews = serializers.IntegerField()

class ImageSerializer(serializers.Serializer):
    image_url = serializers.URLField()