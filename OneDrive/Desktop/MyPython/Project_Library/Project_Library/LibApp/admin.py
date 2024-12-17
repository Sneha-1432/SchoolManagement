from django.contrib import admin
from .models import User, Librarian, OfficeStaff, Student, Book, Fee, LibraryHistory, FeesHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Librarian)
admin.site.register(OfficeStaff)
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Fee)
admin.site.register(LibraryHistory)
admin.site.register(FeesHistory)