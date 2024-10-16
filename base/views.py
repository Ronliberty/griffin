from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from griffin.models import Project
from .models import UserProject, Profile
from .forms import CompleteProjectForm
from .forms import ProfileForm, ProfilePictureForm, UserForm

from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'base/index.html')  # This path is correct based on your structure


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('available_projects')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user and redirect to the dashboard or home page
            login(request, user)
            return redirect('available_projects')  # replace 'home' with the name of the page you want to redirect to
        else:
            # Display an error message

            messages.error(request, 'Invalid username or password')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect(index)


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('available_projects')
        else:
            # Displaying the first error to the user, if needed
            for msg in form.errors.values():
                messages.error(request, msg)

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def available_projects(request):
    # Fetch all projects accepted by the logged-in user
    if request.user.is_authenticated:
        accepted_projects = UserProject.objects.filter(user=request.user).values_list('project_id', flat=True)
        # Fetch all available projects that the user has not accepted
        projects = Project.objects.exclude(id__in=accepted_projects)
    else:
        # If user is not authenticated, show all projects
        projects = Project.objects.all()

    # Pass the projects to the template
    return render(request, 'base/available.html', {'projects': projects})


@login_required(login_url='login')
def accept_project(request, project_id):
    project = Project.objects.get(id=project_id)
    # Create or update the UserProject entry to set accepted to True
    user_project, created = UserProject.objects.get_or_create(
        user=request.user, project=project, defaults={'status': 'ongoing', 'accepted': True})

    if not created:
        user_project.accepted = True
        user_project.status = 'ongoing'
        user_project.save()

        project.status = 'ongoing'
        project.save()

    messages.success(request, f'You have successfully accepted the project "{project.name}"!')
    return redirect('available_projects')


@login_required(login_url='login')
def ongoing_projects(request):
    # Fetch all projects accepted by the logged-in user
    ongoing_projects = UserProject.objects.filter(user=request.user, status='ongoing', accepted=True)

    # Pass the ongoing projects to the template
    return render(request, 'base/ongoing_projects.html', {'ongoing_projects': ongoing_projects})


@login_required(login_url='login')
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_project = get_object_or_404(UserProject, user=request.user, project=project, status='ongoing')

    if request.method == 'POST':
        form = CompleteProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Update the UserProject status to completed
            user_project.status = 'completed'
            user_project.description = form.cleaned_data['description']
            if 'file' in request.FILES:
                user_project.file = request.FILES['file']
            user_project.save()
            return redirect('ongoing_projects')  # Redirect back to ongoing projects list
    else:
        form = CompleteProjectForm()

    return render(request, 'base/complete_project.html', {'form': form, 'project': project})


@login_required(login_url='login')
def work_history(request):
    # Fetch all completed projects for the logged-in user
    completed_projects = UserProject.objects.filter(user=request.user, status='completed')

    return render(request, 'base/work_history.html', {'completed_projects': completed_projects})


@login_required(login_url='login')
def profile_view(request):
    # Display the profile
    profile = request.user.profile
    return render(request, 'base/profile.html', {'profile': profile})


@login_required(login_url='login')
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to view profile after editing
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'base/edit_profile.html', context)