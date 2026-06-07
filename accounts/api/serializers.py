from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = PhoneNumberField(region='NP')
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email','first_name','middle_name','last_name','bio','address','profile_image',
                  'phone_number','password','confirm_password']

    def validate_first_name(self, value):
        return value.strip().lower()

    def validate_middle_name(self,value):
        if value:
            return value.strip().lower()
        return value

    def validate_last_name(self,value):
        return value.strip().lower()

    def validate_profile_image(self,value):

        MAX_SIZE = 5*1024*1024

        if value.size > MAX_SIZE:
            raise serializers.ValidationError("Image should be less than 5MB.")

        return value

    def validate(self,data):

        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if User.objects.filter(email__iexact = email).exists():
            raise serializers.ValidationError("Email already exists.")

        if len(password) < 6:
            raise serializers.ValidationError("Password must be more than 6 characters.")

        if password != confirm_password:
            raise serializers.ValidationError("Password didn't match.")

        return data

    def create(self, validated_data):

        confirm_password = validated_data.pop('confirm_password', None)

        return User.objects.create_user(**validated_data)




class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)


class UpdateRetrieveDeleteUserProfileSerializer(serializers.ModelSerializer):

    public_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ['public_id','first_name','middle_name','last_name','email','bio','address','profile_image','phone_number','trust_points']
        read_only_fields = ['public_id','email','phone_number','trust_points']

    def validate_first_name(self, value):
        return value.strip().lower()

    def validate_middle_name(self, value):
        return value.strip().lower()

    def validate_last_name(self, value):
        return value.strip().lower()





