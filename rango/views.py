from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Course, Assignment, TrackOfFinishedAssignment
from django.shortcuts import render
from django.db.models import Q

# --- Authentication: Register, Login & Logout (M1) ---

def register(request):
    """
    Requirement M1: Save registration info to the database.
    """
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        e = request.POST.get('email')
        phone = request.POST.get('phone')

        if u and p:
            # Create User with hashed password for security
            user = User.objects.create_user(username=u, password=p, email=e)
            # Link to Student profile
            Student.objects.create(user=user, phone_number=phone)
            return redirect(reverse('rango:login'))
            
    return render(request, 'rango/register.html')

def user_login(request):
    """
    Requirement M1: Authenticate and log in user.
    """
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user:
            login(request, user)
            return redirect(reverse('rango:view_courses'))
        else:
            return render(request, 'rango/login.html', {'error': 'Invalid username or password'})

    return render(request, 'rango/login.html')
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()

                return redirect('rango:login')
            else:
                return render(request, 'rango/change_password.html', {
                    'error': 'Old password incorrect'
                })

        except User.DoesNotExist:
            return render(request, 'rango/change_password.html', {
                'error': 'User does not exist'
            })

    return render(request, 'rango/change_password.html')

@login_required
def user_logout(request):
    """
    Safely log out the user.
    """
    logout(request)
    return redirect(reverse('rango:login'))

# --- Dashboard: View All (M4) ---

@login_required
def view_courses(request):
    """
    Requirement M4: Display user-specific assignments ordered by deadline.
    """
    # Fetch only the logged-in student's data
    student, _ = Student.objects.get_or_create(user=request.user)
    courses = Course.objects.filter(student=student)
    assignments = Assignment.objects.filter(student=student).order_by('deadline')
    
    return render(request, 'rango/dashboard.html', {
        'assignments': assignments,
        'courses': courses
    })

# --- Course Management (M2 & S1) ---

@login_required
def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            student, _ = Student.objects.get_or_create(user=request.user)

            Course.objects.create(
                name=name,
                student=student
            )

        return redirect('rango:view_courses')

    return render(request, 'rango/course_form.html')

@login_required
def edit_course(request, course_id):
    """
    Update an existing course name (Ownership check included).
    """
    course = get_object_or_404(Course, id=course_id, student=request.user.student)
    if request.method == 'POST':
        course.name = request.POST.get('name')
        course.save()
        return redirect(reverse('rango:view_courses'))
    return render(request, 'rango/courses_edit.html', {'course': course})

@login_required
def delete_course(request, course_id):
    """
    Requirement S1: Remove a course and its associated assignments.
    """
    course = get_object_or_404(Course, id=course_id, student=request.user.student)
    course.delete()
    return redirect(reverse('rango:view_courses'))

# --- Assignment Management (M3, S1, S2) ---

@login_required
def add_assignment(request):
    student, _ = Student.objects.get_or_create(user=request.user)
    courses = Course.objects.filter(student=student)

    if request.method == 'POST':
        course_id = request.POST.get('course')
        name = request.POST.get('name')          
        deadline = request.POST.get('deadline')  
        description = request.POST.get('description')

        if course_id and name and deadline:
            course = Course.objects.get(id=course_id, student=student)

            Assignment.objects.create(
                course=course,
                name=name,
                deadline=deadline,
                student=student,
                description=description
)

        return redirect('rango:view_courses')

    return render(request, 'rango/assignment_form.html', {'courses': courses})

@login_required
def edit_assignment(request, assignment_id):
    """
    Requirement S1: Modify assignment details.
    """
    student = request.user.student
    assignment = get_object_or_404(Assignment, id=assignment_id, student=student)
    courses = Course.objects.filter(student=student)
    
    if request.method == 'POST':
        assignment.name = request.POST.get('title')
        assignment.deadline = request.POST.get('deadline')
        course_id = request.POST.get('course_id')
        assignment.course = get_object_or_404(Course, id=course_id, student=student)
        assignment.save()
        return redirect(reverse('rango:view_courses'))
        
    return render(request, 'rango/edit_assignment.html', {
    'assignment': assignment,
    'courses': courses
})

@login_required
def delete_assignment(request, assignment_id):
    """
    Requirement S1: Remove an assignment record.
    """
    assignment = get_object_or_404(Assignment, id=assignment_id, student=request.user.student)
    assignment.delete()
    return redirect(reverse('rango:view_courses'))

@login_required
def mark_assignment_done(request, assignment_id):
    """
    Requirement S2: Mark as completed and move to track record.
    """
    assignment = get_object_or_404(Assignment, id=assignment_id, student=request.user.student)
    
    # Create history record per spec [cite: 73]
    TrackOfFinishedAssignment.objects.create(
        student=assignment.student,
        name=assignment.name[:15], # Truncate for Char(15)
        finished_time="2026-03-18" # Example fixed date format
    )
    
    # Update status or delete from active list
    assignment.state = True
    assignment.save()
    
    return redirect(reverse('rango:view_courses'))

# --- Search & Filter (C2) ---

from django.db.models import Q

@login_required
def filter_assignment(request):
    student = request.user.student

    course_id = request.GET.get('course_id')
    query = request.GET.get('q')
    assignments = Assignment.objects.filter(student=student)

    if course_id:
        assignments = assignments.filter(course_id=course_id)

    if query:
        assignments = assignments.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)|
            Q(course__name__icontains=query)
        )
    assignments = assignments.order_by('deadline')
    courses = Course.objects.filter(student=student)

    return render(request, 'rango/assignments.html', {
        'assignments': assignments,
        'courses': courses
    })

@login_required
def assignment_detail(request, assignment_id):
    student = request.user.student
    assignment = get_object_or_404(Assignment, id=assignment_id, student=student)

    return render(request, 'rango/assignment_detail.html', {
        'assignment': assignment
    })

@login_required
def view_courses_page(request):
    student = request.user.student
    courses = Course.objects.filter(student=student)

    return render(request, 'rango/courses_view.html', {
        'courses': courses
    })

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()

                return redirect('rango:login')

            else:
                return render(request, 'rango/change_password.html', {
                    'error': 'Old password incorrect'
                })

        except User.DoesNotExist:
            return render(request, 'rango/change_password.html', {
                'error': 'User does not exist'
            })

    return render(request, 'rango/change_password.html')