from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    FavoriteViewSet,
    UserDetailView,
    UserListView,
    AddCommentView,
    ListCommentsView,
    RegisterView,
    LoginView,
    ProfileView,
    AddPlacesView,
    AddPlaceView,

)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),  
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('comments/add/', AddCommentView.as_view(), name='add-comment'),
    path('comments/list/<int:place_id>/', ListCommentsView.as_view(), name='list-comments'),
    path('add-places/', AddPlacesView.as_view(), name='add-places'),
    path('add-place/', AddPlaceView.as_view(), name='add-place'),
]
