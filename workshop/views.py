import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .models import SiteSettings, PreviousEvent, Course, CourseTopic, CourseProject, Registration, AttendanceRecord, SessionDayStatus
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
    
    # Custom template fallback if fullstack/data-analytics legacy exists
    if slug == 'fullstack-development':
        return render(request, 'workshop/fullstack.html', {'site_settings': site_settings, 'course': course})
    elif slug == 'data-analytics':
        return render(request, 'workshop/data_analytics.html', {'site_settings': site_settings, 'course': course})

    context = {
        'site_settings': site_settings,
        'course': course,
    }
    return render(request, 'workshop/courses.html', context)


def registration_view(request):
    site_settings = SiteSettings.load()
    selected_course_param = request.GET.get('course', '')
    
    initial_data = {}
    if selected_course_param.lower() in ['fullstack', 'fullstack-development', 'full stack development']:
        initial_data['course'] = 'Full Stack Development'
    elif selected_course_param.lower() in ['analytics', 'data-analytics', 'data analytics']:
        initial_data['course'] = 'Data Analytics'

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check duplicate registration protection
            email = form.cleaned_data.get('email')
            college_id = form.cleaned_data.get('college_id')
            course = form.cleaned_data.get('course')

            existing = Registration.objects.filter(
                (Q(email__iexact=email) | Q(college_id__iexact=college_id)),
                course=course
            ).first()

            if existing:
                messages.warning(request, f"You are already registered for '{course}' with ID: {existing.registration_id}.")
                return redirect('registration_success', reg_id=existing.registration_id)

            registration = form.save()
            messages.success(request, "Registration successful!")
            return redirect('registration_success', reg_id=registration.registration_id)
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


# ==================== CUSTOM ADMIN BACKEND VIEWS ====================

def admin_login_view(request):
    site_settings = SiteSettings.load()
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Access denied. Staff privileges required.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    context = {
        'site_settings': site_settings,
        'form': form,
    }
    return render(request, 'workshop/dashboard/login.html', context)


def admin_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('admin_login')


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_dashboard_view(request):
    site_settings = SiteSettings.load()
    total_registrations = Registration.objects.count()
    fullstack_count = Registration.objects.filter(course='Full Stack Development').count()
    analytics_count = Registration.objects.filter(course='Data Analytics').count()
    recent_registrations = Registration.objects.all()[:10]

    context = {
        'site_settings': site_settings,
        'total_registrations': total_registrations,
        'fullstack_count': fullstack_count,
        'analytics_count': analytics_count,
        'recent_registrations': recent_registrations,
    }
    return render(request, 'workshop/dashboard/dashboard.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_registrations_list_view(request):
    site_settings = SiteSettings.load()
    query = request.GET.get('q', '').strip()
    course_filter = request.GET.get('course', '')
    status_filter = request.GET.get('status', '')

    registrations = Registration.objects.all()

    if query:
        registrations = registrations.filter(
            Q(full_name__icontains=query) |
            Q(college_id__icontains=query) |
            Q(registration_id__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )

    if course_filter:
        registrations = registrations.filter(course=course_filter)

    if status_filter:
        registrations = registrations.filter(status=status_filter)

    context = {
        'site_settings': site_settings,
        'registrations': registrations,
        'query': query,
        'course_filter': course_filter,
        'status_filter': status_filter,
    }
    return render(request, 'workshop/dashboard/registrations_list.html', context)


from .emails import send_approval_notification, send_rejection_notification


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_update_registration_status_view(request, reg_id):
    if request.method == 'POST':
        registration = get_object_or_404(Registration, registration_id=reg_id)
        status_action = request.POST.get('status_action', '').lower()
        
        if status_action in ['accept', 'approve']:
            registration.status = 'Approved'
            registration.save()
            sent, msg = send_approval_notification(registration)
            if sent:
                messages.success(request, f"Registration {registration.registration_id} approved. {msg}")
            else:
                messages.warning(request, f"Registration {registration.registration_id} approved, but notification email status: {msg}")

        elif status_action in ['reject', 'cancel']:
            registration.status = 'Rejected'
            registration.save()
            sent, msg = send_rejection_notification(registration)
            if sent:
                messages.success(request, f"Registration {registration.registration_id} rejected. {msg}")
            else:
                messages.warning(request, f"Registration {registration.registration_id} rejected, but notification email status: {msg}")

        elif status_action == 'resend_email':
            if registration.status in ['Approved', 'Confirmed']:
                sent, msg = send_approval_notification(registration, force_resend=True)
            elif registration.status in ['Rejected', 'Cancelled']:
                sent, msg = send_rejection_notification(registration, force_resend=True)
            else:
                sent, msg = False, "Cannot send notification email for a Pending registration."
            
            if sent:
                messages.success(request, f"Notification email resent for {registration.registration_id}. {msg}")
            else:
                messages.error(request, f"Resend email failed: {msg}")
    
    redirect_url = request.META.get('HTTP_REFERER', 'admin_dashboard')
    return redirect(redirect_url)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_registration_detail_view(request, reg_id):
    site_settings = SiteSettings.load()
    registration = get_object_or_404(Registration, registration_id=reg_id)
    
    if request.method == 'POST':
        action = request.POST.get('action_type', '')
        if action == 'resend_email':
            if registration.status in ['Approved', 'Confirmed']:
                sent, msg = send_approval_notification(registration, force_resend=True)
            elif registration.status in ['Rejected', 'Cancelled']:
                sent, msg = send_rejection_notification(registration, force_resend=True)
            else:
                sent, msg = False, "Cannot send email for Pending status."
            
            if sent:
                messages.success(request, f"Email notification queued: {msg}")
            else:
                messages.error(request, f"Resend email failed: {msg}")
            return redirect('admin_registration_detail', reg_id=registration.registration_id)

        form = RegistrationAdminForm(request.POST, instance=registration)
        old_status = registration.status
        if form.is_valid():
            reg = form.save()
            # Trigger email if status changed to Approved or Rejected
            if old_status != reg.status:
                if reg.status in ['Approved', 'Confirmed']:
                    send_approval_notification(reg)
                elif reg.status in ['Rejected', 'Cancelled']:
                    send_rejection_notification(reg)
            messages.success(request, f"Registration {registration.registration_id} updated successfully.")
            return redirect('admin_registration_detail', reg_id=registration.registration_id)
    else:
        form = RegistrationAdminForm(instance=registration)

    context = {
        'site_settings': site_settings,
        'registration': registration,
        'form': form,
    }
    return render(request, 'workshop/dashboard/registration_detail.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_update_registration_status_view(request, reg_id):
    registration = get_object_or_404(Registration, registration_id=reg_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Registration.STATUS_CHOICES):
            registration.status = new_status
            registration.save()
            messages.success(request, f"Status updated to {new_status} for {registration.full_name}.")
    return redirect('admin_registrations_list')


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_courses_list_view(request):
    site_settings = SiteSettings.load()
    courses = Course.objects.all()
    context = {
        'site_settings': site_settings,
        'courses': courses,
    }
    return render(request, 'workshop/dashboard/courses_list.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_course_edit_view(request, course_id):
    site_settings = SiteSettings.load()
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.title}' updated successfully.")
            return redirect('admin_courses_list')
    else:
        form = CourseForm(instance=course)

    context = {
        'site_settings': site_settings,
        'course': course,
        'form': form,
    }
    return render(request, 'workshop/dashboard/course_edit.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_events_list_view(request):
    site_settings = SiteSettings.load()
    events = PreviousEvent.objects.all()
    context = {
        'site_settings': site_settings,
        'events': events,
    }
    return render(request, 'workshop/dashboard/events_list.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_event_edit_view(request, event_id=None):
    site_settings = SiteSettings.load()
    if event_id:
        event = get_object_or_404(PreviousEvent, id=event_id)
    else:
        event = None

    if request.method == 'POST':
        form = PreviousEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event saved successfully.")
            return redirect('admin_events_list')
    else:
        form = PreviousEventForm(instance=event)

    context = {
        'site_settings': site_settings,
        'event': event,
        'form': form,
    }
    return render(request, 'workshop/dashboard/event_edit.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_settings_edit_view(request):
    site_settings = SiteSettings.load()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=site_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Site settings updated successfully.")
            return redirect('admin_settings_edit')
    else:
        form = SiteSettingsForm(instance=site_settings)

    context = {
        'site_settings': site_settings,
        'form': form,
    }
    return render(request, 'workshop/dashboard/settings_edit.html', context)


# ==================== ATTENDANCE & COMPUTER VISION VIEWS ====================

@user_passes_test(is_staff_user, login_url='admin_login')
def admin_attendance_view(request):
    site_settings = SiteSettings.load()
    selected_course = request.GET.get('course', 'Full Stack Development')
    try:
        selected_day = int(request.GET.get('day', 1))
    except ValueError:
        selected_day = 1

    if selected_day < 1:
        selected_day = 1
    elif selected_day > 15:
        selected_day = 15

    # Get enrolled students for selected course
    students = Registration.objects.filter(course=selected_course).order_by('full_name')

    # Process bulk manual form submission or day completion toggle
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_day_completion':
            day_status, _ = SessionDayStatus.objects.get_or_create(
                course_name=selected_course,
                session_day=selected_day
            )
            day_status.is_completed = not day_status.is_completed
            from django.utils import timezone
            day_status.completed_at = timezone.now() if day_status.is_completed else None
            day_status.save()
            status_text = "Completed ✓" if day_status.is_completed else "In Progress"
            messages.success(request, f"Day {selected_day} for {selected_course} marked as {status_text}.")
            return redirect(f"{request.path}?course={selected_course}&day={selected_day}")
        else:
            present_student_ids = request.POST.getlist('present_students')
            for student in students:
                is_present = str(student.id) in present_student_ids
                AttendanceRecord.objects.update_or_create(
                    registration=student,
                    session_day=selected_day,
                    defaults={
                        'course_name': selected_course,
                        'is_present': is_present,
                    }
                )
            messages.success(request, f"Attendance updated for {selected_course} - Day {selected_day}.")
            return redirect(f"{request.path}?course={selected_course}&day={selected_day}")

    # Build attendance status map for current day
    attendance_records = AttendanceRecord.objects.filter(
        registration__course=selected_course,
        session_day=selected_day
    )
    attendance_map = {att.registration.registration_id: att.is_present for att in attendance_records}

    students_list = []
    for student in students:
        students_list.append({
            'id': student.id,
            'registration_id': student.registration_id,
            'full_name': student.full_name,
            'college_id': student.college_id,
            'section': student.section,
            'is_present': attendance_map.get(student.registration_id, False),
        })

    # Build day completion status map for all 15 days
    completed_days = set(
        SessionDayStatus.objects.filter(
            course_name=selected_course,
            is_completed=True
        ).values_list('session_day', flat=True)
    )

    days_info = []
    for d in range(1, 16):
        days_info.append({
            'day': d,
            'is_completed': d in completed_days
        })

    current_day_status = SessionDayStatus.objects.filter(
        course_name=selected_course,
        session_day=selected_day
    ).first()
    is_current_day_completed = bool(current_day_status and current_day_status.is_completed)

    context = {
        'site_settings': site_settings,
        'selected_course': selected_course,
        'selected_day': selected_day,
        'students': students_list,
        'days_info': days_info,
        'is_current_day_completed': is_current_day_completed,
        'courses_list': ['Full Stack Development', 'Data Analytics'],
    }
    return render(request, 'workshop/dashboard/attendance.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_attendance_scan_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            data = request.POST

        qr_payload = data.get('qr_payload', '').strip()
        course_name = data.get('course_name', 'Full Stack Development').strip()
        try:
            session_day = int(data.get('session_day', 1))
        except ValueError:
            session_day = 1

        if not qr_payload:
            return JsonResponse({'success': False, 'message': 'Empty QR payload scanned.'}, status=400)

        # Lookup registration by registration_id or college_id
        student = Registration.objects.filter(
            Q(registration_id__iexact=qr_payload) | Q(college_id__iexact=qr_payload)
        ).first()

        if not student:
            return JsonResponse({
                'success': False,
                'message': f"No student registration found matching ID '{qr_payload}'."
            }, status=404)

        # Check course match
        if student.course.lower() != course_name.lower():
            return JsonResponse({
                'success': False,
                'message': f"Student '{student.full_name}' is enrolled in '{student.course}', not in '{course_name}'!"
            }, status=400)

        # Check if already marked Present BEFORE updating
        existing_record = AttendanceRecord.objects.filter(
            registration=student,
            session_day=session_day
        ).first()

        already_marked = bool(existing_record and existing_record.is_present)

        # Record attendance
        record, created = AttendanceRecord.objects.update_or_create(
            registration=student,
            session_day=session_day,
            defaults={
                'course_name': course_name,
                'is_present': True,
            }
        )

        total_present = AttendanceRecord.objects.filter(
            registration__course=course_name,
            session_day=session_day,
            is_present=True
        ).count()

        if already_marked:
            return JsonResponse({
                'success': True,
                'already_marked': True,
                'student_id': student.registration_id,
                'full_name': student.full_name,
                'college_id': student.college_id,
                'course': student.course,
                'stream': student.stream,
                'year_of_study': student.year_of_study,
                'section': student.section,
                'session_day': session_day,
                'total_present_today': total_present,
                'message': f"⚠️ ALREADY MARKED: {student.full_name} ({student.college_id}) is already recorded Present for Day {session_day}!"
            })

        return JsonResponse({
            'success': True,
            'already_marked': False,
            'student_id': student.registration_id,
            'full_name': student.full_name,
            'college_id': student.college_id,
            'course': student.course,
            'stream': student.stream,
            'year_of_study': student.year_of_study,
            'section': student.section,
            'session_day': session_day,
            'total_present_today': total_present,
            'message': f"✓ SUCCESS: Marked Present for {student.full_name} ({student.college_id})!"
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_attendance_summary_view(request):
    site_settings = SiteSettings.load()
    selected_course = request.GET.get('course', 'Full Stack Development')
    students = Registration.objects.filter(course=selected_course).order_by('full_name')

    # Build student matrix stats
    summary_data = []
    for student in students:
        records = AttendanceRecord.objects.filter(registration=student)
        day_list = []
        present_count = 0
        for day in range(1, 16):
            rec = records.filter(session_day=day).first()
            is_p = bool(rec and rec.is_present)
            if is_p:
                present_count += 1
            day_list.append(is_p)

        percentage = round((present_count / 15.0) * 100, 1)
        eligible_for_certificate = percentage >= 50.0

        summary_data.append({
            'student': student,
            'day_list': day_list,
            'present_count': present_count,
            'percentage': percentage,
            'eligible': eligible_for_certificate,
        })

    context = {
        'site_settings': site_settings,
        'selected_course': selected_course,
        'summary_data': summary_data,
        'days_range': range(1, 16),
        'courses_list': ['Full Stack Development', 'Data Analytics'],
    }
    return render(request, 'workshop/dashboard/attendance_summary.html', context)


@user_passes_test(is_staff_user, login_url='admin_login')
def admin_export_attendance_csv(request):
    selected_course = request.GET.get('course', 'Full Stack Development')
    response = HttpResponse(content_type='text/csv')
    filename = f"Attendance_Report_{selected_course.replace(' ', '_')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    header = ['Registration ID', 'Student Name', 'College ID', 'Course', 'Stream', 'Year', 'Section'] + [f'Day {d}' for d in range(1, 16)] + ['Total Present', 'Percentage', 'Certificate Status']
    writer.writerow(header)

    students = Registration.objects.filter(course=selected_course).order_by('full_name')
    for student in students:
        records = AttendanceRecord.objects.filter(registration=student)
        day_cells = []
        present_count = 0
        for day in range(1, 16):
            rec = records.filter(session_day=day).first()
            if rec and rec.is_present:
                day_cells.append('P')
                present_count += 1
            else:
                day_cells.append('A')

        pct = round((present_count / 15.0) * 100, 1)
        cert_status = "Qualified (>=50%)" if pct >= 50.0 else "Not Qualified (<50%)"

        row = [
            student.registration_id,
            student.full_name,
            student.college_id,
            student.course,
            student.stream,
            student.year_of_study,
            student.section,
        ] + day_cells + [present_count, f"{pct}%", cert_status]

        writer.writerow(row)

    return response
