
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm
from .models import JobApplication
from django.db.models import Q
from django.db.models import Count
from django.utils import timezone

def home(request):
    return render(request, 'applications/home.html')


def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'applications/register.html', {'form': form})
def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    else:
        form = AuthenticationForm()

    return render(request, 'applications/login.html', {'form': form})
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_application(request):

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            return redirect('home')

    else:
        form = JobApplicationForm()

    return render(request, 'applications/add_application.html', {'form': form})



@login_required
def application_list(request):
    search_query = request.GET.get('search', '')
    selected_status = request.GET.get('status', '')
    applications = JobApplication.objects.filter(user=request.user)
    if search_query:
        applications = applications.filter(
            Q(company_name__icontains=search_query) |
            Q(job_role__icontains=search_query)
        )
    if selected_status:
        applications = applications.filter(status=selected_status)
    return render(
        request,
        'applications/application_list.html',
        {
            'applications': applications,
            'search_query': search_query,
            'selected_status': selected_status
        }
    )

@login_required
def edit_application(request, id):

    application = JobApplication.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, instance=application)

        if form.is_valid():
            form.save()
            return redirect('application_list')

    else:
        form = JobApplicationForm(instance=application)

    return render(
        request,
        'applications/edit_application.html',
        {'form': form}
    )


@login_required
def delete_application(request, id):

    application = JobApplication.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        application.delete()
        return redirect('application_list')

    return render(
        request,
        'applications/delete_application.html',
        {'application': application}
    )


@login_required
def dashboard(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )

    total_applications = applications.count()

    applied_count = applications.filter(status='Applied').count()

    interview_count = applications.filter(status='Interview').count()

    selected_count = applications.filter(status='Selected').count()

    rejected_count = applications.filter(status='Rejected').count()

    context = {
        'total_applications': total_applications,
        'applied_count': applied_count,
        'interview_count': interview_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
    }

    return render(request, 'applications/dashboard.html', context)




@login_required
def upcoming_interviews(request):

    today = timezone.localdate()

    interviews = JobApplication.objects.filter(
        user=request.user,
        status='Interview',
        interview_date__gte=today
    ).order_by('interview_date')

    return render(
        request,
        'applications/upcoming_interviews.html',
        {'interviews': interviews}
    )


