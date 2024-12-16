from rest_framework import serializers
from .models import Comment
from .models import Favorite
from django.contrib.auth.models import User
from .models import Place
from django import forms

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'title', 'price', 'image']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    place_title = serializers.CharField(source='place.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'content', 'date_posted', 'place_title']

# Favorite Serializer
class FavoriteSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'place', 'date_added']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'place', 'date_added']
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'place', 'date_added']


    def get_place(self, obj):
        return {
            "id": obj.place.id,
            "title": obj.place.title,
            "price": obj.place.price,
            "image": obj.place.image.url if obj.place.image else None,
        }



