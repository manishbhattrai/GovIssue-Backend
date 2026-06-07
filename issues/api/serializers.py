from rest_framework import serializers
from django.contrib.auth import get_user_model
from issues.models import Category, Issue, Location

User=get_user_model()

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','name','slug','description','created_at','updated_at']
        read_only_fields = ['id','slug','created_at','updated_at']

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['latitude','longitude']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['full_name','profile_image']



class CreateIssueSerializer(serializers.ModelSerializer):

    location = LocationSerializer()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Issue
        fields = ['title','description',
                  'category','address','image','location']

    def validate_image(self,value):

        MAX_SIZE = 5*1024*1024


        if value.size > MAX_SIZE:
            raise serializers.ValidationError("Image should be less than 2MB.")


        return value

    def create(self,validated_data):

        location_data = validated_data.pop('location')

        issue = Issue.objects.create(**validated_data)
        Location.objects.create(issue=issue, **location_data)
        return issue

class ListIssueSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    created_by = UserProfileSerializer()
    location = LocationSerializer()

    class Meta:
        model = Issue
        fields = ['issue_id','created_by','title','description','category',
                  'address','image','status','location','created_at','updated_at']


class RetrieveUpdateIssueSerializer(serializers.ModelSerializer):

    location = LocationSerializer()
    category_details = CategorySerializer(source='category', read_only=True)
    created_by = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset= Category.objects.all()
    )

    class Meta:
        model = Issue
        fields = ['issue_id','created_by','title','description',
                  'category','address','image','category_details',
                  'status','location','created_at','updated_at']

        read_only_fields = ['issue_id','created_by','category_details','created_at','updated_at']

    def get_created_by(self,obj):
        return obj.created_by.full_name

    def update(self, instance, validated_data):

        request = self.context.get('request')
        location_data = validated_data.pop('location',None)

        if 'status' in validated_data and not request.user.is_staff:
            validated_data.pop('status')

        if location_data:
            location_instance = instance.location
            if location_instance:
                for attr, value in location_data.items():
                    setattr(location_instance, attr, value)
                location_instance.save()
            else:

                Location.objects.create(issue=instance, **location_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance