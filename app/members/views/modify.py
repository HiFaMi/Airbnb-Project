from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.permissions import IsAuthenticated
from ..serializers.user import UserProfileSerializer

User = get_user_model()


class UserProfileModified(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
