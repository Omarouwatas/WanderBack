from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AddCommentView
router = DefaultRouter()
router.register(r'comments', views.CommentViewSet, basename='comment')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),  
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', views.LoginView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('profile/', views.ProfileView.as_view(), name='profile'),
    #comments
    path('add-comment/', AddCommentView.as_view(), name='add-comment'),
    path('comments/<int:place_id>/', views.get_comments, name='list-comments'),
    #places
    path('add-place/', views.AddPlaceView.as_view(), name='add-place'),
    path('places/city/<str:city_name>/', views.get_places_by_city, name='get_places_by_city'),
    path('place/<int:place_id>/', views.get_place_details, name='get_place_details'),
    path('places/', views.get_all_places, name='get_all_places'),
    #favorite
    path('favorites/toggle/<int:user_id>/<int:place_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/status/<int:user_id>/<int:place_id>/', views.is_favorite, name='is_favorite'),
    path('favorites/ids/<int:user_id>/', views.get_favorite_place_ids, name='get_favorite_place_ids'),



]
