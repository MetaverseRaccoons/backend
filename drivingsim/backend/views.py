from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .forms import CreateUserForm
from .models import User, Friend_Request
from .serializers import UserSerializer
from rest_framework import serializers, generics, status
import uuid
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view


class UserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, username=None):
        if username is None:
            user = request.user
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response("User does not exist")
            if not user.is_shareable:
                return HttpResponse("User is private", status=403)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def post(self, request):
        form = CreateUserForm(request.data)
        #form = CreateUserForm(request.POST) # testing
        print(form.errors)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return JsonResponse(
                {
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=201
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.POST['username']
        old_password = request.POST['old_password']
        user = authenticate(username=username, password=old_password)
        if user is not None:
            login(request, user)
            user.set_password(request.POST['new_password'])
            user.save()
            return Response("Password changed successfully", status=status.HTTP_200_OK)
        return Response("failed to change password", status=status.HTTP_400_BAD_REQUEST)

class FriendsView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @api_view(['POST'])
    def send_friend_request(request, userID):
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response("User not logged in", status=status.HTTP_400_BAD_REQUEST)
        from_user = user
        to_user = User.objects.get(id=userID)
        friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
        if created:
            return JsonResponse(
                {
                    'status': "Friend request sent",
                    'httpstatus': status.HTTP_200_OK,
                    'id': friend_request.id,
                })
        else:
            return Response("Friend request was already sent", status=status.HTTP_200_OK)

    @api_view(['POST'])
    def accept_friend_request(request, requestID):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response("User not logged in", status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = Friend_Request.objects.get(id=requestID)
        if friend_request.to_user == user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response("Friend request accepted", status=status.HTTP_200_OK)
        else:
            return Response("Friend request not accepted", status=status.HTTP_404_NOT_FOUND)
        
    @api_view(['POST'])
    def decline_friend_request(request, requestID):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return Response("User not logged in", status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = Friend_Request.objects.get(id=requestID)
        if friend_request.to_user == user or friend_request.from_user == user:
            friend_request.delete()
            return Response("Friend request declined", status=status.HTTP_200_OK)
        else:
            return Response("Friend request not declined", status=status.HTTP_404_NOT_FOUND)