from django.db import models
from django.contrib.auth.models import User # Import the built-in User model

class Student(models.Model):
    # This links Student to a User model instance
    # It handles 'username', 'email', and 'password' 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Keep additional fields from ER diagram 
    phone_number = models.CharField(max_length=15) 

    def __str__(self):
        return self.user.username
    
class Course(models.Model):
    """
    Represents a course managed by a student.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # StudentID which database automatically generates by order
    name = models.CharField(max_length=15) # Char(15) 

    def __str__(self):
        return self.name

class Assignment(models.Model):
    """
    Represents a coursework assignment.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # StudentID 
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # CourseID 
    name = models.CharField(max_length=128) # Name Char(128) 
    state = models.BooleanField(default=False) # State Boolean 
    deadline = models.CharField(max_length=15) # Deadline Char(15) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class TrackOfFinishedAssignment(models.Model):
    """
    Tracks successfully completed assignments.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE) # StudentID 
    name = models.CharField(max_length=15) # Name Char(15) 
    finished_time = models.CharField(max_length=15) # FinishedTime Char(15) 

    def __str__(self):
        return self.name