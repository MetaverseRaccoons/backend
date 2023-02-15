from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .forms import CreateUserForm
from .models import Friends
from .serializers import UserSerializer, FriendsSerializer
from rest_framework import generics, status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view, permission_classes


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
                return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            if not user.is_shareable and username is not None:
                return JsonResponse({'message': "User is private"}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    def post(self, request):
        form = CreateUserForm(request.data)
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
        username = request.data['username']
        old_password = request.data['old_password']
        user = authenticate(username=username, password=old_password)
        if user is not None:
            login(request, user)
            user.set_password(request.data['new_password'])
            user.save()
            return JsonResponse({'message': "Password changed successfully"}, status=status.HTTP_200_OK)
        return JsonResponse({'message': "Failed to change password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, to_username):
    from_user = request.user
    try:
        to_user = User.objects.get(username=to_username)
    except User.DoesNotExist:
        return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if to_user.get_friend_requests().filter(from_user=from_user).exists():
        return JsonResponse({'message': "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

    if from_user.get_friend_requests().filter(to_user=to_user).exists():
        return JsonResponse({'message': "Friend request already received"}, status=status.HTTP_400_BAD_REQUEST)

    friends = Friends(from_user=from_user, to_user=to_user, accepted=False)
    friends.save()

    return JsonResponse({'message': "Friend request sent"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, from_username):
    to_user = request.user
    try:
        from_user = User.objects.get(username=from_username)
    except User.DoesNotExist:
        return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        friends = Friends.objects.get(from_user=from_user, to_user=to_user)
    except Friends.DoesNotExist:
        return JsonResponse({'message': "Friend request does not exist"}, status=status.HTTP_404_NOT_FOUND)

    friends.accepted = True
    friends.save()

    return JsonResponse({'message': "Friend request accepted"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests(request):
    user = request.user
    friend_requests = user.get_friend_requests()
    serializer = FriendsSerializer(friend_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_friends(request):
    user = request.user
    friends = user.get_friends()
    serializer = FriendsSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

