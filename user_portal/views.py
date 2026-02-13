from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student, StudentAttempt, StudentResponse
from staff_portal.models import Assessment, Question, Option
from django.utils import timezone
from datetime import timedelta


# 1. Landing Page
def index(request):
    return render(request, 'index.html')

# 2. Student Registration
def register_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reg_number = request.POST.get('registration_number')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile_number')
        password = request.POST.get('password')

        if User.objects.filter(username=reg_number).exists():
            messages.error(request, 'Registration number already exists!')
            return redirect('student_register')

        user = User.objects.create_user(
            username=reg_number,
            first_name=name,
            email=email,
            password=password
        )
        
        Student.objects.create(
            user=user,
            registration_number=reg_number,
            mobile_number=mobile
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('student_login')

    # FIX: Change 'user_portal/register.html' to 'register.html'
    return render(request, 'register.html')

# 3. Student Login
def login_student(request):
    if request.method == 'POST':
        reg_number = request.POST.get('registration_number')
        password = request.POST.get('password')
        
        user = authenticate(username=reg_number, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid Registration Number or Password')
            
    # FIX: Change 'user_portal/login.html' to 'login.html' (or whatever you named the file)
    return render(request, 'login.html') 

# 4. Student Logout
def logout_student(request):
    logout(request)
    return redirect('index')

# 5. Student Dashboard
@login_required(login_url='student_login')
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    assessments = Assessment.objects.filter(is_active=True)
    attempted_ids = StudentAttempt.objects.filter(student=student).values_list('assessment_id', flat=True)
    
    # FIX: Change 'user_portal/dashboard.html' to 'student_dashboard.html'
    return render(request, 'student_dashboard.html', {
        'assessments': assessments,
        'attempted_ids': attempted_ids
    })


@login_required(login_url='student_login')
def take_assessment(request, assessment_id):
    print("--- DEBUG: VIEW IS RUNNING ---")  # Look for this in your terminal
    
    assessment = get_object_or_404(Assessment, id=assessment_id)
    student = Student.objects.get(user=request.user)
    
    # Get/Create Attempt
    attempt, created = StudentAttempt.objects.get_or_create(
        student=student,
        assessment=assessment
    )

    # Force the value to 3600 seconds (1 Hour) to test
    remaining_seconds = 3600 
    
    print(f"--- DEBUG: SENDING {remaining_seconds} TO TEMPLATE ---") 

    return render(request, 'take_assessment.html', {
        'assessment': assessment,
        'remaining_seconds': remaining_seconds
    })

# 7. Submit Assessment (UPDATED to save responses)
@login_required(login_url='student_login')
def submit_assessment(request, assessment_id):
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, id=assessment_id)
        student = Student.objects.get(user=request.user)
        attempt = get_object_or_404(StudentAttempt, student=student, assessment=assessment)
        
        if attempt.is_completed:
            return redirect('student_dashboard')

        score = 0
        total_questions = assessment.questions.count()
        
        for question in assessment.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            selected_option = None
            
            if selected_option_id:
                selected_option = Option.objects.get(id=selected_option_id)
                if selected_option.is_correct:
                    score += 1
            
            # SAVE THE STUDENT'S SPECIFIC ANSWER
            StudentResponse.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={'selected_option': selected_option}
            )
        
        attempt.score = score
        attempt.is_completed = True
        attempt.save()
        
        messages.success(request, f'Assessment Submitted! You scored {score}/{total_questions}')
        return redirect('student_dashboard')

# 8. View Detailed Results (NEW)
@login_required(login_url='student_login')
def view_results(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    student = Student.objects.get(user=request.user)
    attempt = get_object_or_404(StudentAttempt, student=student, assessment=assessment)
    
    # Package the data so the HTML template is easy to write
    results_data = []
    for question in assessment.questions.all():
        response = StudentResponse.objects.filter(attempt=attempt, question=question).first()
        selected = response.selected_option if response else None
        correct_option = question.options.filter(question=question, is_correct=True).first()
        
        results_data.append({
            'question': question,
            'selected': selected,
            'correct': correct_option,
            'is_correct': selected == correct_option if selected else False
        })
        
    return render(request, 'test_results.html', {
        'assessment': assessment,
        'attempt': attempt,
        'results_data': results_data
    })