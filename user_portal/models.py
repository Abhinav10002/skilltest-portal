from django.db import models
from django.contrib.auth.models import User
from staff_portal.models import Assessment, Question, Option

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.registration_number} - {self.user.first_name}"
    

class StudentAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    date_attempted = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.assessment.title}"
    
class StudentResponse(models.Model):
    attempt = models.ForeignKey(StudentAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.attempt.student.user.username} - {self.question.text[:20]}"