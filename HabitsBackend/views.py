from .models import User, Counter, Reward
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, CounterSerializer, RewardSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CounterList(generics.GenericAPIView, mixins.ListModelMixin,
                  mixins.CreateModelMixin,):
    serializer_class = CounterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): #overridden
        # Filter counters by the currently authenticated user
        return Counter.objects.filter(user=self.request.user)

    def get(self, request):
        return self.list(request)
        
    def post(self, request):
        return self.create(request)
    
        
    
class CounterDetails(generics.GenericAPIView, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CounterSerializer
    permission_classes = [IsAuthenticated]

    lookup_field ='id'

    def get_queryset(self):
        # Only return counters belonging to the logged-in user
        return Counter.objects.filter(user=self.request.user)

    def get(self, request, id):
        return self.retrieve(request, id=id)
    
    def put(self, request, id):
        return self.update(request, id=id)
    
    def delete(self, request, id):
        return self.destroy(request, id=id)
    
    
class RegisterView(generics.CreateAPIView): #post is automatically provided by CreateAPIView
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the authenticated user from the validated data
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)  # Create JWT refresh token
        access_token = refresh.access_token  # Get the access token

        return Response({
            'user': UserSerializer(user).data,
            'access_token': str(access_token),  # Send the access token back

        }, status=status.HTTP_200_OK)
