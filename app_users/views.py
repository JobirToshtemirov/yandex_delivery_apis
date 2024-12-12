from app_common.pagination import CustomPagination
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app_products.models import ProductsModel
from .models import UserModel
from .serializers import UserModelSerializer, LoginSerializer, ProductModelSerializer


class UserListView(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited. This api for super admin only.
    """
    serializer_class = UserModelSerializer
    queryset = UserModel.objects.all()
    # permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save()


class LoginView(APIView):
    """
        API endpoint that allows users to login.
    """
    serializer_class = LoginSerializer
    queryset = UserModel.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        user = UserModel.objects.get(phone_number=phone_number)
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


class LogoutView(APIView):
    """
        API endpoint that allows users to logout.
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
