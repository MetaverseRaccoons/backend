from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import UserSerializer


class UserView(APIView):
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


    def post(self):
        pass
