from django.urls import path
from .views import RegisterView, LoginView
from rest_framework import routers
from . import views
from .views import *
# from .views import UserDetailView

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_user/', ProfileViewSet.as_view({'post': 'create'}), name='create_user'),
    path('user/', UserDataAPIView.as_view(), name='userdata'),
    path('user/<int:userId>/',views.getByid_user),
]