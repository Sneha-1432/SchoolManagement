from rest_framework import serializers
from .models import User, Librarian, OfficeStaff, Student, Book, Fee, LibraryHistory, FeesHistory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=True)  # Role is only provided when creating the user
    password = serializers.CharField(write_only=True, required=False)  #optional for upadte

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        role = validated_data.get('role')

        # Create the user first, but don't save the role flags yet
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        # Initialize the related model (Librarian or OfficeStaff) based on the role
        related_object = None
        if role == 'librarian':
            related_object = Librarian(user=user)
        elif role == 'office_staff':
            related_object = OfficeStaff(user=user)

        # Ensure the related model is saved before saving the user with the role flag
        if related_object:
            related_object.save()

            # After saving the related object, set the role flag on the User model
            if role == 'librarian':
                user.is_librarian = True
            elif role == 'office_staff':
                user.is_office_staff = True

            # Now, save the user instance with the correct role flag
            user.save()

        return user



# Librarian serializer
class LibrarianSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Librarian
        fields = ['user', 'is_active']



# Office staff serializer
class OfficeStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = OfficeStaff
        fields = ['user', 'is_active']

    


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        # Update the existing user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance



class LibrarianUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()  # Nested serializer for updating user details

    class Meta:
        model = Librarian
        fields = ['user', 'is_active']

    def update(self, instance, validated_data):
        # Extract user data from the validated data
        user_data = validated_data.pop('user', None)
        if user_data:
            # Update the related user model instance
            user_instance = instance.user
            user_serializer = UserUpdateSerializer(user_instance, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Now update librarian-specific fields (e.g., is_active)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    

class OfficestaffUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()  # Nested serializer for updating user details

    class Meta:
        model = Librarian
        fields = ['user', 'is_active']

    def update(self, instance, validated_data):
        # Extract user data from the validated data
        user_data = validated_data.pop('user', None)
        if user_data:
            # Update the related user model instance
            user_instance = instance.user
            user_serializer = UserUpdateSerializer(user_instance, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

        # Now update librarian-specific fields (e.g., is_active)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance



# Student serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


#Library Serializer
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


#Library Serializer
class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fee
        fields = '__all__'


# Library History Serializer
class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = '__all__'
        

# Fee History Serializer
class FeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesHistory
        fields = '__all__'



