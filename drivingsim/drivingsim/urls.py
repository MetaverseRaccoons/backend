from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from backend import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', views.UserView.as_view(), name='user'),
    path('api/user/passwordchange/', views.PasswordView.as_view(), name='password_change'),
    path('api/user/<str:username>/', views.UserView.as_view(), name='view_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

