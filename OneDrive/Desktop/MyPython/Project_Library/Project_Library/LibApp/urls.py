from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminLoginView, OfficeStaffLoginView, AdminLogoutView, UserCreateView, update_librarian, update_officestaff, GetLibrarianView, GetOfficeStaffView, CreateStdentView, ListStudentView, UpdateStudentView, DeleteStudentView, CreateLibraryView, ListLibraryView, UpdateLibraryView, DeleteLibraryView, CreateFeeView, ListFeeView, UpdateFeeView, DeleteFeeView, CreateLibHistoryView,ListLibHistoryView, UpdateLibHistoryView, DeleteLibHistoryView, CreateFeeHistoryView,ListFeeHistoryView, UpdateFeeHistoryView, DeleteFeeHistoryView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('adminlogin/', AdminLoginView.as_view(), name='admin-login'),
    # path('home/', HomePageView.as_view(), name='home'),
    path('officestafflogin/', OfficeStaffLoginView.as_view(), name='officestaff-login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('adminlogout/', AdminLogoutView.as_view(), name='admin-logout'),
    path('usercreate/', UserCreateView.as_view(), name='user_create'),
    path('librariandetails/',GetLibrarianView.as_view(), name='librarianview' ),
    path('officestaffdetails/', GetOfficeStaffView.as_view(), name='officestaffview'),
    path('librarian_update/<int:pk>/', update_librarian, name='librarian_update'),
    path('office_staff_update/<int:pk>/', update_officestaff, name='office_staff_update'),
    path('createstudent/', CreateStdentView.as_view(), name='Createstudent'),
    path('studentslist/', ListStudentView.as_view(), name='list-students'),  # List all students
    path('studentupdate/<int:id>/', UpdateStudentView.as_view(), name='update-student'),  # Update a student by ID
    path('studentdelete/<int:id>/delete/', DeleteStudentView.as_view(), name='delete-student'),  # Delete a student by ID
    path('createlibrary/', CreateLibraryView.as_view(), name='Createlibrary'),
    path('librarylist/', ListLibraryView.as_view(), name='list-library'),  # List all students
    path('libraryupdate/<int:id>/', UpdateLibraryView.as_view(), name='update-library'),  # Update a student by ID
    path('librarydelete/<int:id>/delete/', DeleteLibraryView.as_view(), name='delete-library'),  # Delete a student by ID
    path('createfee/', CreateFeeView.as_view(), name='Createfee'),
    path('feelist/', ListFeeView.as_view(), name='list-fee'),  # List all students
    path('feeupdate/<int:id>/', UpdateFeeView.as_view(), name='update-fee'),  # Update a student by ID
    path('feedelete/<int:id>/delete/', DeleteFeeView.as_view(), name='delete-fee'),  # Delete a student by ID
    path('createlibhistory/', CreateLibHistoryView.as_view(), name='Createstudent'),
    path('libhistorylist/', ListLibHistoryView.as_view(), name='list-students'),  # List all students
    path('libhistoryupdate/<int:id>/', UpdateLibHistoryView.as_view(), name='update-student'),  # Update a student by ID
    path('libhistorydelete/<int:id>/delete/', DeleteLibHistoryView.as_view(), name='delete-student'),  # Delete a student by ID
    path('createfeehistory/', CreateFeeHistoryView.as_view(), name='Createstudent'),
    path('feehistorylist/', ListFeeHistoryView.as_view(), name='list-students'),  # List all students
    path('feehistoryupdate/<int:id>/', UpdateFeeHistoryView.as_view(), name='update-student'),  # Update a student by ID
    path('feehistorydelete/<int:id>/delete/', DeleteFeeHistoryView.as_view(), name='delete-student'),  # Delete a student by ID

]






