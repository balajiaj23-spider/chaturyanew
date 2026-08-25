from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import SiteSettings, PreviousEvent, Course, CourseTopic, CourseProject, Registration
from .forms import RegistrationForm, SiteSettingsForm, CourseForm, CourseTopicForm, PreviousEventForm, RegistrationAdminForm

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# ==================== FRONTEND PUBLIC VIEWS ====================

def home_view(request):
    site_settings = SiteSettings.load()
    previous_events = PreviousEvent.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    context = {
        'site_settings': site_settings,
        'previous_events': previous_events,
        'courses': courses,
    }
    return render(request, 'workshop/index.html', context)


def courses_list_view(request):
    site_settings = SiteSettings.load()
    courses = Course.objects.filter(is_active=True)
    context = {
        'site_settings': site_settings,
        'courses': courses,
    }
    return render(request, 'workshop/courses.html', context)


def course_detail_view(request, slug):
    site_settings = SiteSettings.load()
    course = get_object_or_404(Course, slug=slug, is_active=True)
    topics = course.topics.all()
    projects = course.projects.all()
    
    context = {
        'site_settings': site_settings,
        'course': course,
        'topics': topics,
        'projects': projects,
    }
    
    if slug == 'fullstack':
        return render(request, 'workshop/fullstack.html', context)
    elif slug == 'data-analytics':
        return render(request, 'workshop/data_analytics.html', context)
    else:
        return render(request, 'workshop/fullstack.html', context)


def registration_view(request):
    site_settings = SiteSettings.load()
    course_param = request.GET.get('course', '')
    
    initial_data = {}
    if course_param.lower() in ['fullstack', 'full stack development']:
        initial_data['course'] = 'Full Stack Development'
    elif course_param.lower() in ['data-analytics', 'data analytics', 'dataanalytics']:
        initial_data['course'] = 'Data Analytics'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            messages.success(request, 'Registration Successful!')
            return redirect('registration_success', reg_id=registration.registration_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm(initial=initial_data)

    context = {
        'site_settings': site_settings,
        'form': form,
    }
    return render(request, 'workshop/registration.html', context)


def registration_success_view(request, reg_id):
    site_settings = SiteSettings.load()
    registration = get_object_or_404(Registration, registration_id=reg_id)
    context = {
        'site_settings': site_settings,
        'registration': registration,
    }
    return render(request, 'workshop/registration_success.html', context)


# ==================== CUSTOM ADMIN DASHBOARD VIEWS ====================

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Access denied. Staff/Admin privileges required.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'workshop/dashboard/login.html', {'form': form})


def admin_logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('admin_login')


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_dashboard_view(request):
    total_registrations = Registration.objects.count()
    fullstack_count = Registration.objects.filter(course='Full Stack Development').count()
    data_analytics_count = Registration.objects.filter(course='Data Analytics').count()
    total_events = PreviousEvent.objects.count()
    total_courses = Course.objects.count()
    recent_registrations = Registration.objects.all()[:10]

    context = {
        'total_registrations': total_registrations,
        'fullstack_count': fullstack_count,
        'data_analytics_count': data_analytics_count,
        'total_events': total_events,
        'total_courses': total_courses,
        'recent_registrations': recent_registrations,
    }
    return render(request, 'workshop/dashboard/dashboard.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_registrations_list_view(request):
    registrations = Registration.objects.all()
    
    # Filter parameters
    course_filter = request.GET.get('course', '')
    stream_filter = request.GET.get('stream', '')
    year_filter = request.GET.get('year', '')
    section_filter = request.GET.get('section', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '').strip()

    if course_filter:
        registrations = registrations.filter(course=course_filter)
    if stream_filter:
        registrations = registrations.filter(stream=stream_filter)
    if year_filter:
        registrations = registrations.filter(year_of_study=year_filter)
    if section_filter:
        registrations = registrations.filter(section=section_filter)
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    if search_query:
        registrations = registrations.filter(
            Q(full_name__icontains=search_query) |
            Q(college_id__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    context = {
        'registrations': registrations,
        'course_filter': course_filter,
        'stream_filter': stream_filter,
        'year_filter': year_filter,
        'section_filter': section_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'streams': [s[0] for s in Registration.STREAM_CHOICES],
        'courses': [c[0] for c in Registration.COURSE_CHOICES],
        'years': [y[0] for y in Registration.YEAR_CHOICES],
        'sections': [s[0] for s in Registration.SECTION_CHOICES],
    }
    return render(request, 'workshop/dashboard/registrations_list.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_registration_detail_view(request, reg_id):
    registration = get_object_or_404(Registration, registration_id=reg_id)
    
    if request.method == 'POST':
        if 'delete_registration' in request.POST:
            registration.delete()
            messages.success(request, 'Registration deleted successfully.')
            return redirect('admin_registrations_list')
        
        form = RegistrationAdminForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration status updated successfully.')
            return redirect('admin_registration_detail', reg_id=registration.registration_id)
    else:
        form = RegistrationAdminForm(instance=registration)

    context = {
        'registration': registration,
        'form': form,
    }
    return render(request, 'workshop/dashboard/registration_detail.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_courses_list_view(request):
    courses = Course.objects.all()
    return render(request, 'workshop/dashboard/courses_list.html', {'courses': courses})


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_course_edit_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.title}' updated successfully.")
            return redirect('admin_courses_list')
    else:
        form = CourseForm(instance=course)

    topics = course.topics.all()
    return render(request, 'workshop/dashboard/course_edit.html', {'form': form, 'course': course, 'topics': topics})


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_events_list_view(request):
    events = PreviousEvent.objects.all()
    return render(request, 'workshop/dashboard/events_list.html', {'events': events})


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_event_edit_view(request, event_id=None):
    if event_id:
        event = get_object_or_404(PreviousEvent, id=event_id)
    else:
        event = None

    if request.method == 'POST':
        if 'delete_event' in request.POST and event:
            event.delete()
            messages.success(request, 'Previous event deleted.')
            return redirect('admin_events_list')

        form = PreviousEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event saved successfully.')
            return redirect('admin_events_list')
    else:
        form = PreviousEventForm(instance=event)

    return render(request, 'workshop/dashboard/event_edit.html', {'form': form, 'event': event})


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_settings_edit_view(request):
    site_settings = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site Settings updated successfully.')
            return redirect('admin_settings_edit')
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(request, 'workshop/dashboard/settings_edit.html', {'form': form, 'site_settings': site_settings})
