import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import SiteSettings

logger = logging.getLogger(__name__)

def send_approval_notification(registration, force_resend=False):
    """
    Sends an automated approval email to the student.
    Prevents duplicate emails unless force_resend is explicitly True.
    """
    if registration.approval_email_sent and not force_resend:
        logger.info(f"Approval email already sent for {registration.registration_id}. Skipping.")
        return False, "Approval email already sent previously."

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

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'chathuryasdc@gmail.com')

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[registration.email],
            fail_silently=False,
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
        logger.info(f"Approval email successfully sent to {registration.email} ({registration.registration_id})")
        return True, "Approval email delivered successfully."

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to send approval email to {registration.email}: {error_msg}")
        
        # Record failure without rolling back Approved status
        registration.notification_status = 'Failed'
        registration.notification_type = 'Approval'
        registration.notification_error = error_msg
        registration.save(update_fields=[
            'notification_status',
            'notification_type',
            'notification_error'
        ])
        return False, f"Email delivery failed: {error_msg}"


def send_rejection_notification(registration, force_resend=False):
    """
    Sends an automated rejection email to the student.
    Prevents duplicate emails unless force_resend is explicitly True.
    """
    if registration.rejection_email_sent and not force_resend:
        logger.info(f"Rejection email already sent for {registration.registration_id}. Skipping.")
        return False, "Rejection email already sent previously."

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

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'chathuryasdc@gmail.com')

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[registration.email],
            fail_silently=False,
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
        logger.info(f"Rejection email successfully sent to {registration.email} ({registration.registration_id})")
        return True, "Rejection email delivered successfully."

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to send rejection email to {registration.email}: {error_msg}")
        
        # Record failure without rolling back Rejected status
        registration.notification_status = 'Failed'
        registration.notification_type = 'Rejection'
        registration.notification_error = error_msg
        registration.save(update_fields=[
            'notification_status',
            'notification_type',
            'notification_error'
        ])
        return False, f"Email delivery failed: {error_msg}"
