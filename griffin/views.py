from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from base.models import UserProject
from .models import Project
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required



def landing_page(request):
    return render(request, 'griffin/landing.html')

def staff_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('create_project')  # Redirect if staff member is already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate staff member
        if username is None or password is None:
            messages.error(request, 'Username and password are required.')
            return render(request, 'griffin/login.html')  # Replace with your actual template

        user = authenticate(request, username=username, password=password)  # Authenticate user

        if user is not None:
            if user.is_staff:  # Ensure the user is a staff member
                login(request, user)
                return redirect('create_project')  # Redirect to staff dashboard
            else:
                messages.error(request, 'You do not have permission to access this area.')
        else:
            messages.error(request, 'Invalid staff username or password.')

    return render(request, 'griffin/login.html')

def staff_required(user):
    return user.is_staff

@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def staff_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('staff_login')


@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        file = request.FILES.get('file')

        # Save the project in the database
        project = Project.objects.create(name=name, description=description, deadline=deadline)
        if file:  # If a file is uploaded, save it to the project (modify as needed)
            project.file = file
        project.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'name': project.name,
                'description': project.description,
                'deadline': project.deadline.strftime('%Y-%m-%d')
            })

        # Optionally add a success message
        messages.success(request, 'Project created successfully!')
        return redirect('create_project')  # Redirect to the same page to show the form again

    # Retrieve all projects from the database to display below the form
    projects = Project.objects.all().order_by('-created_at')
    for project in projects:
        if project.file:
            if project.file.url.endswith(('.jpg', '.jpeg', '.png')):
                project.file_type = 'image'
            elif project.file.url.endswith('.pdf'):
                project.file_type = 'pdf'
            else:
                project.file_type = 'other'
    return render(request, 'griffin/create_project.html', {'projects': projects})
@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def project_list(request):

    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'griffin/project_list.html', {'projects': projects})

@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def ongoing_projects_view(request):

    ongoing_projects = UserProject.objects.filter(user=request.user, status='ongoing')


    return render(request, 'griffin/continue.html', {'ongoing_projects': ongoing_projects})

@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def all_completed_projects(request):
    # Fetch all completed projects across all users
    completed_projects = UserProject.objects.filter(status='completed')

    return render(request, 'griffin/task.html', {'completed_projects': completed_projects})

@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def tasks(request):
    # Fetch all completed projects across all users
    completed_projects = UserProject.objects.filter(status='completed')

    return render(request, 'griffin/task.html', {'completed_projects': completed_projects})

@user_passes_test(lambda u: u.is_staff, login_url='staff_login')
@login_required(login_url='staff_login')
def user_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'griffin/user.html', {'users': users})