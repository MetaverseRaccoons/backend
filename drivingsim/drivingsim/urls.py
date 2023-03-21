from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from backend import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', views.UserView.as_view(), name='user'),
    path('api/user/passwordchange/', views.PasswordView.as_view(), name='password_change'),
    path('api/user/delete/', views.delete_account, name='delete_account'),
    path('api/user/<str:username>/', views.UserView.as_view(), name='view_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/friend/request/<str:to_username>/send/', views.send_friend_request, name='friend_request'),
    path('api/friend/request/<str:from_username>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('api/friend/request/<str:from_username>/decline/', views.decline_friend_request, name='decline_friend_request'),
    path('api/friend/<str:username>/remove/', views.remove_friend, name='remove_friend'),
    path('api/friend/request/', views.friend_requests, name='friend_requests'),
    path('api/friend/', views.all_friends, name='all_friends'),
    path('api/violation/', views.violation, name='add_or_view_violation'),
    path('api/violation/<str:username>/', views.other_violations, name='other_violations'),
    path('api/leaderboard/km/<int:page_number>/', views.leaderboard_km_driven, name='leaderboard_km_driven'),
    path('api/leaderboard/minutes/<int:page_number>/', views.leaderboard_minutes_driven, name='leaderboard_minutes_driven'),
    path('api/leaderboard/violations/<int:page_number>/', views.leaderboard_violations, name='leaderboard_violations'),
]

