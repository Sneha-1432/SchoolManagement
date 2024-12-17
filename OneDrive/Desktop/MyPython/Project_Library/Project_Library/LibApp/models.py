from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_office_staff = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.username



class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = False

    def __str__(self):
        return self.user.username



class OfficeStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = False

    def __str__(self):
        return self.user.username



class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    class_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Fee(models.Model):
    fee_type = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.fee_type}"



class Book(models.Model):
    book_number = models.CharField(max_length=50)
    book_name = models.CharField(max_length=50)
    number_of_books = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.book_name}"
    


class LibraryHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField()
    return_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')])

    def __str__(self):
        return f"{self.book_name} borrowed by {self.student.first_name} {self.student.last_name}"
    



class FeesHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='fees_history_fee_type', related_query_name='fees_history_fee_type')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Can be blank initially
    payment_date = models.DateTimeField()
    remarks = models.TextField()

    def save(self, *args, **kwargs):
        # If fee_type is changed, update the amount
        if not self.amount or self._state.adding or (self.pk and self.fee_type != FeesHistory.objects.get(pk=self.pk).fee_type):
            self.amount = self.fee_type.amount  # Get the amount from the fee_type

        super().save(*args, **kwargs)  # Save the instance to the database

    def __str__(self):
        return f"Fees for {self.student.first_name} {self.student.last_name} - {self.fee_type}"

