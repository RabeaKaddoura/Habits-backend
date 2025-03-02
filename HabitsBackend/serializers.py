from rest_framework import serializers
from .models import User, Counter, Reward
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}  # Ensure password is not returned

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # Hash password before saving
        return super().create(validated_data) #equivalent to User.objects.create(....)
    

class LoginSerializer(serializers.Serializer): #used ser.Ser instead of ser.ModelSer cuz we don't need to update a model, we just need to validate.
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        user = authenticate(username=username_or_email, password=password)

        if user is None:
            # Try to authenticate using email if username failed
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        data["user"] = user
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
    

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ["title", "trigger"]                   


class CounterSerializer(serializers.ModelSerializer):
    validRewards = RewardSerializer(many=True, required=False) #to link rewards to counter 
    class Meta:
        model = Counter
        fields = ["id", "counterTitle", "validRewards", "createdOn", "value", "updatedAt"] #rewards linked to counter 

    def create(self, validated_data): #takes in counter object and extracts rewards from the object. Then counter and rewards objects are saved in their respective model (table).
        rewards_data = validated_data.pop("validRewards", [])

        user = self.context['request'].user
        counter = Counter.objects.create(user=user,**validated_data)  #turns data to key-value pairs to match the model 

        for rewards in rewards_data:
             Reward.objects.create(counter=counter, **rewards)

        return counter
    
    def update(self, instance, validated_data):
        instance.counterTitle = validated_data.get('counterTitle', instance.counterTitle)
        instance.value = validated_data.get('value', instance.value)
        instance.updatedAt = validated_data.get('updatedAt', instance.updatedAt)
        instance.save()
        
        return instance