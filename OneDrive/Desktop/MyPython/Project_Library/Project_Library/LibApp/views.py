from django.shortcuts import render
# from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User, Librarian, OfficeStaff, Student, Book, Fee, LibraryHistory, FeesHistory
from .serializers import UserSerializer, LibrarianSerializer, OfficeStaffSerializer, LibrarianUpdateSerializer, OfficestaffUpdateSerializer, StudentSerializer, LibrarySerializer, FeeSerializer, LibraryHistorySerializer, FeeHistorySerializer
from .permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from django.http import Http404
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


# Create your views here.

# ADMIN LOGIN VIEW
class AdminLoginView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user is an Admin
        if user.is_admin:
            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh_token}")

            # Return the tokens in the response
            return Response({
                'access': access_token,
                'refresh': refresh_token
            })

        # If the user is not an Admin
        return Response({"error": "You do not have admin rights"}, status=status.HTTP_403_FORBIDDEN)
        


class AdminLogoutView(APIView):
    # Custom logout view to blacklist the JWT token (optional)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklists the refresh token
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        

# OFFICE STAFF LOGIN VIEW
class OfficeStaffLoginView(APIView):
    permission_classes = [AllowAny]     # Allow any user (no need to be authenticated to log in)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # check if username and password are provided
        if not username or not password:
            return Response({"error" : "username and password are required to lgin"}, status=status.HTTP_400_BAD_REQUEST)
        
        #If Credentialis provide-Authenticate the user
        user = authenticate(username=username, password=password)

        # if provided credentials are wrong:
        if user is None:
            return Response({"error" : "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # check if the user is office staff
        if user.is_office_staff:
            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            print(f"Access Token : {access_token}")
            print(f"Refresh Token : {refresh_token}")

            # Return the tokens in response
            return Response({
                'access' : access_token, 
                'refresh' : refresh_token
                })
        
        # if the user is not office staff
        return Response({"error": "you dont have office staff rights"}, status=status.HTTP_403_FORBIDDEN)
        




class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Call the base class's create method to create a user
        response = super().create(request, *args, **kwargs)
        return response
    permission_classes = ['IsAdminUser']
    

# Get Librarain details
class GetLibrarianView(APIView):
    def get(self, request):
        librarians = Librarian.objects.all()
        serializer = LibrarianSerializer(librarians, many=True)
        return Response(serializer.data)
    
class GetOfficeStaffView(APIView):
    def get(self, request):
        officestaffs = OfficeStaff.objects.all()
        serializer = OfficeStaffSerializer(officestaffs, many=True)
        return Response(serializer.data)
    
    # update librarian details

@api_view(['PUT', 'PATCH'])
def update_librarian(request, pk):
    try:
        librarian = Librarian.objects.get(id=pk)
    except Librarian.DoesNotExist:
        return Response({'error': 'Librarian not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use the serializer to update the librarian and associated user data
    serializer = LibrarianUpdateSerializer(librarian, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
def update_officestaff(request, pk):
    try:
        officestaff = OfficeStaff.objects.get(id=pk)
    except Librarian.DoesNotExist:
        return Response({'error': 'Officestaff not found'}, status=status.HTTP_404_NOT_FOUND)

    # Use the serializer to update the librarian and associated user data
    serializer = OfficestaffUpdateSerializer(officestaff, data=request.data, partial=(request.method == 'PATCH'))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Student create view
class CreateStdentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer



# View to list all students
class ListStudentView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# View to update an existing student
class UpdateStudentView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'  # To use the student's ID for lookup


# View to delete a student
class DeleteStudentView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'  # To use the student's ID for lookup


# ------------------------------
# view to create Library

class CreateLibraryView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = LibrarySerializer



# View to list all students
class ListLibraryView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = LibrarySerializer


# View to update an existing student
class UpdateLibraryView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = LibrarySerializer
    lookup_field = 'id'  # To use the student's ID for lookup


# View to delete a student
class DeleteLibraryView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'  # To use the student's ID for lookup



# -------------------------------------
class CreateFeeView(generics.CreateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer



# View to list all students
class ListFeeView(generics.ListAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer


# View to update an existing student
class UpdateFeeView(generics.UpdateAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    lookup_field = 'id'  # To use the Fee's ID for lookup


# View to delete a student
class DeleteFeeView(generics.DestroyAPIView):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer
    lookup_field = 'id'  # To use the Fee's ID for lookup


# ---------------------------------------------
class CreateLibHistoryView(generics.CreateAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer



# View to list all students
class ListLibHistoryView(generics.ListAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer


# View to update an existing student
class UpdateLibHistoryView(generics.UpdateAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    lookup_field = 'id'  # To use the libhistory's ID for lookup


# View to delete a student
class DeleteLibHistoryView(generics.DestroyAPIView):
    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    lookup_field = 'id'  # To use the libhistory's ID for lookup


# ------------------------------------------------
class CreateFeeHistoryView(generics.CreateAPIView):
    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializer


# View to list all students
class ListFeeHistoryView(generics.ListAPIView):
    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializer


# View to update an existing student
class UpdateFeeHistoryView(generics.UpdateAPIView):
    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializer
    lookup_field = 'id'  # To use the Feehistory's ID for lookup


# View to delete a student
class DeleteFeeHistoryView(generics.DestroyAPIView):
    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializer
    lookup_field = 'id'  # To use the Feehistory's ID for lookup



