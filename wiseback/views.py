from django.shortcuts import render
from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from .models import Comment,Place
from .serializers import CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .serializers import PlaceSerializer,PlaceForm
from django.http import JsonResponse
from .models import Place
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Favorite
from django.core.exceptions import ObjectDoesNotExist

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Favorite, Place
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import User, Favorite
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def toggle_favorite(request, user_id, place_id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            place = Place.objects.get(id=place_id)
            favorite, created = Favorite.objects.get_or_create(user=user, place=place)

            if created:
                return JsonResponse({'message': 'Added to favorites'}, status=201)
            else:
                favorite.delete()
                return JsonResponse({'message': 'Removed from favorites'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Place.DoesNotExist:
            return JsonResponse({'error': 'Place not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_favorite_place_ids(request, user_id):
    permission_classes = [AllowAny]
    try:
        user = User.objects.get(id=user_id)
    
        favorites = Favorite.objects.filter(user=user)
        
        if not favorites.exists():
            return JsonResponse({"message": "No favorites found for this user."}, status=200)
        favorite_place_ids = [favorite.place.id for favorite in favorites]
        print("aaslema")
        return JsonResponse(favorite_place_ids, safe=False, status=200)
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


def is_favorite(request, user_id, place_id):
    user = get_object_or_404(User, id=user_id)
    place = get_object_or_404(Place, id=place_id)
    is_favorite = Favorite.objects.filter(user=user, place=place).exists()
    return JsonResponse({'is_favorite': is_favorite}, status=200)


@csrf_exempt
def get_place_details(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
        place_data = {
            "id": place.id,
            "title": place.title,
            "price": float(place.price),
            "country": place.country,
            "city": place.city,
            "description": place.description,
            "facilities": place.facilities,
            "image": request.build_absolute_uri(place.image.url) if place.image else None,
            "ratings": float(place.rating),
            "category": place.category,
        }
        return JsonResponse(place_data, safe=False)
    except Place.DoesNotExist:
        return JsonResponse({"error": "Place not found"}, status=404)
    

def get_places_by_city(request, city_name):
    places = Place.objects.filter(city__iexact=city_name)  
    places_data = [
        {
            "id": place.id,
            "title": place.title,
            "price": float(place.price),
            "country": place.country,
            "city": place.city,
            "description": place.description,
            "facilities": place.facilities,
            "image": request.build_absolute_uri(place.image.url) if place.image else None,
            "ratings": float(place.rating),
            "category": place.category,
        }
        for place in places
    ]
    return JsonResponse(places_data, safe=False)


def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('place_list') 
    else:
        form = PlaceForm()
    return render(request, 'add_place.html', {'form': form})


def get_all_places(request):
    places = Place.objects.all() 
    places_list = [
        {
            "id": place.id,
            "title": place.title,
            "price": float(place.price),
            "country": place.country,
            "city": place.city,
            "description": place.description,
            "facilities": place.facilities,
            "image": request.build_absolute_uri(place.image.url) if place.image else None,
            "ratings": float(place.rating),
            "category": place.category,
        }
        for place in places
    ]
    return JsonResponse(places_list, safe=False)


class AddPlaceView(APIView):
    parser_classes = (MultiPartParser, FormParser)  
    def post(self, request, format=None):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name

        })

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email_or_username = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")
        try:
            if "@" in email_or_username:
                user = User.objects.get(email__iexact=email_or_username)
            else:
                user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User not found."})


        user = authenticate(username=user.username, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Invalid credentials."})


        data = super().validate({"username": user.username, "password": password})
        data["email"] = user.email
        data["username"] = user.username
        data["id"] = user.id
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "You have access to this view!"})


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print(request.data)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not first_name or not last_name or not username or not email or not password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password) 
        )

        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


def get_comments(request, place_id):
        permission_classes = [AllowAny]
        try:
            place = Place.objects.get(id=place_id)
            comments = Comment.objects.filter(place=place).order_by('-date_posted')
            print("aaslema")
            if not comments.exists():
                return JsonResponse({"message": "No comments found for this place."}, status=200)

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return JsonResponse({"error": "Place not found"}, status=404)


class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:

            place_id = request.data.get('place_id')
            content = request.data.get('content', '').strip()

            if not place_id:
                return Response({"error": "Place ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            if not content:
                return Response({"error": "Content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            place = Place.objects.get(id=place_id)

            comment = Comment.objects.create(user=request.user, place=place, content=content)
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Place.DoesNotExist:
            return Response({"error": "Place not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"Something went wrong: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
