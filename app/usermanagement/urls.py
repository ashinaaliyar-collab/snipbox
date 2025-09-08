from django.urls import path

from usermanagement import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='LoginView'),
    path('create/', views.UserProfileCreateView.as_view(), name='UserProfileCreateView'),
    path('refresh/', views.RefreshTokenView.as_view(), name='RefreshTokenView'),
    path('logout/', views.LogoutView.as_view(), name='LogoutView'),
]