from django.shortcuts import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assessment, Question, Option


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_staff: 
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin.')
    
    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    
    assessments = Assessment.objects.all().order_by('-date_created')
    return render(request, 'admin_dashboard.html', {'assessments': assessments})


@login_required(login_url='admin_login')
def create_assessment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        
        assessment = Assessment.objects.create(title=title, description=description)
        messages.success(request, 'Assessment created! Now add questions.')
        
        
        return redirect('add_question', assessment_id=assessment.id)
        
    return render(request, 'create_assessment.html')


@login_required(login_url='admin_login')
def add_question(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        course_marks = request.POST.get('marks')
        
        # Create Question
        question = Question.objects.create(
            assessment=assessment, 
            text=question_text, 
            marks=course_marks
        )
        
        # Option 1
        Option.objects.create(
            question=question, 
            text=request.POST.get('option1'), 
            is_correct=(request.POST.get('correct_option') == 'option1')
        )
        # Option 2
        Option.objects.create(
            question=question, 
            text=request.POST.get('option2'), 
            is_correct=(request.POST.get('correct_option') == 'option2')
        )
        # Option 3
        Option.objects.create(
            question=question, 
            text=request.POST.get('option3'), 
            is_correct=(request.POST.get('correct_option') == 'option3')
        )
        # Option 4
        Option.objects.create(
            question=question, 
            text=request.POST.get('option4'), 
            is_correct=(request.POST.get('correct_option') == 'option4')
        )
        
        messages.success(request, 'Question added successfully!')
        # Stay on page to add more questions
        return redirect('add_question', assessment_id=assessment.id)

    return render(request, 'add_question.html', {'assessment': assessment})

@login_required(login_url='admin_login')
def delete_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    assessment.delete()
    messages.success(request, 'Assessment deleted successfully!')
    return redirect('admin_dashboard')