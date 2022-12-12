from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .forms import CreateUserForm
from .models import User
from .serializers import UserSerializer
from rest_framework import serializers, generics, status
import uuid
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout



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
        form = CreateUserForm(request.POST)
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
    permission_classes = [AllowAny]

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
    