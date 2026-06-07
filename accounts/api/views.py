from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import (
    UserRegisterSerializer, LoginSerializer,
    UpdateRetrieveDeleteUserProfileSerializer
    )

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request=request, username=email, password=password)
            if user is not None:
                if not user.is_active:
                    return Response({'message':"your account is deactivated."},
                                    status=status.HTTP_403_FORBIDDEN
                                    )
                refresh = RefreshToken.for_user(user)
                refresh['role'] = user.role
                refresh['public_id'] = str(user.public_id)

                user_data = {
                    'full_name': user.full_name,
                    ##'profile_image':user.profile_image,
                    'trust_points': user.trust_points,
                }

                return Response({

                    'status':'success',
                    'message':'successfully logged in.',
                    'token': str(refresh.access_token),
                    'user_data': user_data
                }, status=status.HTTP_200_OK)

            else:
                return Response(
                    {'message':'Invalid email or password'
                     }, status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRetrieveDeleteUserProfileView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UpdateRetrieveDeleteUserProfileSerializer
    parser_classes = [MultiPartParser,FormParser]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):

        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(
            {'message':'User deactivated successfully.'},
            status=status.HTTP_200_OK
        )


