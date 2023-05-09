from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .forms import CreateUserForm, AddViolationForm, AddLevelSessionForm, AddCertificateForm
from .models import Friends, Violation, Level, LevelSession, Certificate
from .serializers import UserSerializer, FriendsSerializer, ViolationSerializer, CertificateSerializer
from rest_framework import generics, status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login

from rest_framework.decorators import api_view, permission_classes

import mmh3


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
        return JsonResponse({**serializer.data, "certsGot": [f"{n}" for n in range(3) if (mmh3.hash(serializer.data.get('username'), signed=False)//(10**n) % 10) >= 5]}, status=status.HTTP_200_OK)

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
                status=status.HTTP_201_CREATED
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, from_username):
    to_user = request.user
    try:
        from_user = User.objects.get(username=from_username)
    except User.DoesNotExist:
        return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        friends = Friends.objects.get(from_user=from_user, to_user=to_user)
    except Friends.DoesNotExist:
        return JsonResponse({'message': "Friend request does not exist"}, status=status.HTTP_404_NOT_FOUND)

    friends.delete()

    return JsonResponse({'message': "Friend request declined"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_friend(request, username):
    user = request.user
    try:
        friend = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    try:
        friends = Friends.objects.get((Q(from_user=user) & Q(to_user=friend)) | (Q(to_user=user) | Q(from_user=friend)))
    except Friends.DoesNotExist:
        return JsonResponse({'message': "Friend does not exist"}, status=status.HTTP_404_NOT_FOUND)

    friends.delete()

    return JsonResponse({'message': "Friend removed"}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return JsonResponse({'message': "Account deleted"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def violation(request):
    user = request.user
    if request.method == 'POST':
        form = AddViolationForm(request.data)
        if form.is_valid():
            violation = form.save(commit=False)
            violation.user = user
            violation.save()
            return JsonResponse({'message': "Violation added"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        violations = user.get_violations()
        serializer = ViolationSerializer(violations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def other_violations(request, username):
    user = request.user

    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'message': "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_friend(other_user) and other_user.is_shareable:
        return JsonResponse({'message': "User is private"}, status=status.HTTP_401_UNAUTHORIZED)

    violations = other_user.get_violations()
    serializer = ViolationSerializer(violations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def leaderboard_km_driven(request, page_number):
    users = User.objects.filter(is_shareable=True).order_by('-km_driven')
    paginator = Paginator(users, 20)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    serializer = UserSerializer(page.object_list, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def leaderboard_minutes_driven(request, page_number):
    users = User.objects.filter(is_shareable=True).order_by('-minutes_driven')
    paginator = Paginator(users, 20)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    serializer = UserSerializer(page.object_list, many=True)
    return JsonResponse(serializer.data, safe=False)


# Query the 'violation' table and return the number of violations for each user
# Make a leaderboard based on the number of violations
@api_view(['GET'])
def leaderboard_violations(request, page_number):
    objects = Violation.objects.raw('''
    SELECT backend_violation.id, backend_user.*, COUNT(*) AS num_violations FROM backend_violation
    INNER JOIN backend_user ON backend_violation.user_id = backend_user.id
    WHERE backend_user.is_shareable = 1
    GROUP BY username ORDER BY num_violations DESC
     ''')

    paginator = Paginator(objects, 20)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    result = []
    for object in page.object_list:
        user = UserSerializer(object).data
        user['violations'] = object.num_violations
        result.append(user)

    return JsonResponse(result, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_minutes_driven(request):
    user = request.user
    minutes = request.data.get('minutes')
    if minutes is None:
        return JsonResponse({'message': "Minutes not provided"}, status=status.HTTP_400_BAD_REQUEST)

    user.minutes_driven += float(minutes)
    user.save()
    return JsonResponse({'message': "Minutes added"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_km_driven(request):
    user = request.user
    kilometers = request.data.get('kilometers')
    if kilometers is None:
        return JsonResponse({'message': "Kilometers not provided"}, status=status.HTTP_400_BAD_REQUEST)

    user.km_driven += float(kilometers)
    user.save()
    return JsonResponse({'message': "Kilometers added"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_certificate(request):
    user = request.user
    form = AddCertificateForm(request.data)
    if form.is_valid():
        certificate = form.save(commit=False)
        certificate.user = user
        certificate.save()
        return JsonResponse({'message': "Certificate added"}, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_level_session(request):
    user = request.user
    form = AddLevelSessionForm(request.data)
    if form.is_valid():
        try:
            level = Level.objects.get(name=request.data.get('level_name'))
        except Level.DoesNotExist:
            return JsonResponse({'message': "Level does not exist"}, status=status.HTTP_404_NOT_FOUND)

        level_session = form.save(commit=False)
        level_session.user = user
        level_session.level = level
        level_session.save()
        return JsonResponse({'message': "Level session added"}, status=status.HTTP_201_CREATED)

    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_certificates(request):
    user = request.user
    certificates = Certificate.objects.filter(user=user)
    serializer = CertificateSerializer(certificates, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
