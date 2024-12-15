from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_products.models import ProductsModel
from .models import UserModel, UserRoleChoice, UserStatusChoice
from .serializers import (
    UserModelSerializer, LoginSerializer, ProductModelSerializer,
    UpdatePasswordSerializer, LoginWithUsernameSerializer
)


class LoginView(APIView):
    """
        API endpoint that allows users to login.
    """
    serializer_class = LoginSerializer
    queryset = UserModel

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            user = self.queryset.objects.filter(phone_number=phone_number)

            success = True

            if not user.exists():
                user = self.queryset.objects.create(
                    phone_number=phone_number,
                    password=password,
                    username="user"+phone_number,
                    role=UserRoleChoice.USER,
                    status=UserStatusChoice.ACTIVE,
                )
                refresh = RefreshToken.for_user(user)
                response = {
                    'success': True,
                    'message': 'Login successful but another datas necessary!',
                    'token': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user_id': user.id,
                        'phone_number': user.phone_number
                    }
                }
                return Response(response, status=status.HTTP_200_OK)

            user = user.first()
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                response = {
                    'success': True,
                    'message': 'Login successful',
                    'token': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user_id': user.id,
                        'phone_number': user.phone_number
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'success': False,
                    'message': 'User does not exist or password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                'success': False,
                'message': 'User does not exist or password is incorrect'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LoginWithUsernameView(APIView):
    """
        API endpoint that allows users with username to login.
    """
    serializer_class = LoginWithUsernameSerializer
    queryset = UserModel

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = self.queryset.objects.filter(username=username)

            if not user.exists():
                response = {
                   'success': False,
                   'message': 'User does not exist'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user = user.first()
            if user.role not in [UserRoleChoice.RESTAURANT, UserRoleChoice.BRANCH,
                                 UserRoleChoice.COURIER, UserRoleChoice.ADMIN]:
                response = {
                   'success': False,
                   'message': 'User is not allowed'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                response = {
                    'success': True,
                    'message': 'Login successful',
                    'token': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user_id': user.id,
                        'username': user.phone_number
                    }
                }
                return Response(response, status=status.HTTP_200_OK)

            else:
                response = {
                    'success': False,
                    'message': 'User does not exist or password is incorrect'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response = {
                'success': False,
                'message': 'User does not exist or password is incorrect'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
        API endpoirouter.register('users', user_views.UserListView, basename='user')nt that allows users to logout.
    """

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = {
                'success': True,
                'message': 'Logout successful'

            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'message': str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GetAllProductsView(APIView):
    serializer_class = ProductModelSerializer
    queryset = ProductsModel.objects.all()

    def get(self, request, *args, **kwargs):
        products = ProductsModel.objects.all()
        serializer = ProductModelSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserView(APIView):
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()

    def put(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=request.user.id)
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'message': 'User updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=request.user.id)
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'message': 'User updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UpdatePasswordView(APIView):
    serializer_class = UpdatePasswordSerializer
    queryset = UserModel.objects.all()

    def put(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=request.user.id)
        serializer = UpdatePasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success': True,
            'message': 'Password updated successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
