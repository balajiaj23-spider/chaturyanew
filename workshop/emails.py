import logging
import threading
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.utils import timezone
from .models import SiteSettings

logger = logging.getLogger(__name__)

def _get_smtp_connection():
    """
    Returns an explicit SMTP connection forcing Port 465 (SSL) for cloud hosting providers
    like Render where outbound Port 587 (TLS) connections are blocked or throttled.
    """
    user = getattr(settings, 'EMAIL_HOST_USER', '')
    pwd = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    host = getattr(settings, 'EMAIL_HOST', 'smtp.gmail.com') or 'smtp.gmail.com'
    
    # Always enforce Port 465 (SSL) for Gmail or default cloud outbound connections
    port = 465
    use_ssl = True
    use_tls = False

    return get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=host,
        port=port,
        username=user,
        password=pwd,
        use_ssl=use_ssl,
        use_tls=use_tls,
        timeout=30
    )

def _async_send_approval_email(registration_id):
    """
    Background worker thread to deliver approval email without blocking the web request.
    """
    from .models import Registration
    try:
        registration = Registration.objects.get(registration_id=registration_id)
    except Registration.DoesNotExist:
        logger.error(f"Registration {registration_id} not found for async approval email.")
        return

    site_settings = SiteSettings.load()
    college_name = site_settings.college_name or "Seshadripuram College"
    club_name = site_settings.club_name or "Chathurya Student Developers Club"

    subject = "Workshop Registration Approved – College Club Workshop"
    
    body = (
        f"Dear {registration.full_name},\n\n"
        f"Congratulations!\n\n"
        f"Your registration for the {registration.course} workshop has been approved.\n\n"
        f"Registration Details:\n\n"
        f"Name: {registration.full_name}\n"
        f"College ID: {registration.college_id}\n"
        f"Course: {registration.course}\n"
        f"Stream: {registration.stream}\n"
        f"Year: {registration.year_of_study}\n"
        f"Section: {registration.section}\n\n"
        f"Your registration status: APPROVED\n\n"
        f"We look forward to having you participate in the workshop.\n\n"
        f"Regards,\n"
        f"{club_name}\n"
        f"{college_name}\n"
    )

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Chathurya Club <chathuryastudentdeveloperclub@gmail.com>')

    try:
        conn = _get_smtp_connection()
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[registration.email],
            fail_silently=False,
            connection=conn
        )
        
        # Update tracking fields on success
        registration.approval_email_sent = True
        registration.notification_status = 'Sent'
        registration.notification_sent_at = timezone.now()
        registration.notification_type = 'Approval'
        registration.notification_error = ''
        registration.save(update_fields=[
            'approval_email_sent',
            'notification_status',
            'notification_sent_at',
            'notification_type',
            'notification_error'
        ])
        logger.info(f"Approval email successfully delivered to {registration.email} ({registration.registration_id})")

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to deliver approval email to {registration.email}: {error_msg}")
        
        # Record failure without rolling back Approved status
        registration.notification_status = 'Failed'
        registration.notification_type = 'Approval'
        registration.notification_error = error_msg
        registration.save(update_fields=[
            'notification_status',
            'notification_type',
            'notification_error'
        ])


def _async_send_rejection_email(registration_id):
    """
    Background worker thread to deliver rejection email without blocking the web request.
    """
    from .models import Registration
    try:
        registration = Registration.objects.get(registration_id=registration_id)
    except Registration.DoesNotExist:
        logger.error(f"Registration {registration_id} not found for async rejection email.")
        return

    site_settings = SiteSettings.load()
    college_name = site_settings.college_name or "Seshadripuram College"
    club_name = site_settings.club_name or "Chathurya Student Developers Club"

    subject = "Workshop Registration Update – College Club Workshop"
    
    body = (
        f"Dear {registration.full_name},\n\n"
        f"Thank you for registering for the {registration.course} workshop.\n\n"
        f"After reviewing the registrations, we regret to inform you that your registration has not been selected for this workshop.\n\n"
        f"Registration Details:\n\n"
        f"Name: {registration.full_name}\n"
        f"College ID: {registration.college_id}\n"
        f"Course: {registration.course}\n"
        f"Stream: {registration.stream}\n"
        f"Year: {registration.year_of_study}\n"
        f"Section: {registration.section}\n\n"
        f"Your registration status: NOT SELECTED\n\n"
        f"Thank you for your interest in the College Club Workshop.\n\n"
        f"Regards,\n"
        f"{club_name}\n"
        f"{college_name}\n"
    )

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Chathurya Club <chathuryastudentdeveloperclub@gmail.com>')

    try:
        conn = _get_smtp_connection()
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[registration.email],
            fail_silently=False,
            connection=conn
        )
        
        # Update tracking fields on success
        registration.rejection_email_sent = True
        registration.notification_status = 'Sent'
        registration.notification_sent_at = timezone.now()
        registration.notification_type = 'Rejection'
        registration.notification_error = ''
        registration.save(update_fields=[
            'rejection_email_sent',
            'notification_status',
            'notification_sent_at',
            'notification_type',
            'notification_error'
        ])
        logger.info(f"Rejection email successfully delivered to {registration.email} ({registration.registration_id})")

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to deliver rejection email to {registration.email}: {error_msg}")
        
        # Record failure without rolling back Rejected status
        registration.notification_status = 'Failed'
        registration.notification_type = 'Rejection'
        registration.notification_error = error_msg
        registration.save(update_fields=[
            'notification_status',
            'notification_type',
            'notification_error'
        ])


def send_approval_notification(registration, force_resend=False):
    """
    Triggers approval notification email asynchronously in a background thread.
    Prevents duplicate emails unless force_resend is True.
    """
    if registration.approval_email_sent and not force_resend:
        logger.info(f"Approval email already sent for {registration.registration_id}. Skipping.")
        return False, "Approval email already sent previously."

    # Launch background thread for instant web UI response
    thread = threading.Thread(
        target=_async_send_approval_email,
        args=(registration.registration_id,),
        daemon=True
    )
    thread.start()
    return True, "Approval notification queued and sending in background."


def send_rejection_notification(registration, force_resend=False):
    """
    Triggers rejection notification email asynchronously in a background thread.
    Prevents duplicate emails unless force_resend is True.
    """
    if registration.rejection_email_sent and not force_resend:
        logger.info(f"Rejection email already sent for {registration.registration_id}. Skipping.")
        return False, "Rejection email already sent previously."

    # Launch background thread for instant web UI response
    thread = threading.Thread(
        target=_async_send_rejection_email,
        args=(registration.registration_id,),
        daemon=True
    )
    thread.start()
    return True, "Rejection notification queued and sending in background."
