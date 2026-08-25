import uuid
from django.db import models
from django.utils import timezone

class SiteSettings(models.Model):
    club_name = models.CharField(max_length=200, default='Chathurya Student Developers Club')
    college_name = models.CharField(max_length=200, default='Tech Campus, College Block B')
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    hero_title = models.CharField(max_length=200, default='Learn. Build. Launch.')
    hero_subtitle = models.TextField(default='Welcome to Chathurya Student Developers Club. Join our hands-on technical workshops designed to help students build practical skills, explore modern software technologies, and launch real-world projects.')
    about_text = models.TextField(default='Chathurya Student Developers Club is a premier student-led technical community dedicated to nurturing coding talent, practical software engineering, and data science skills.')
    contact_email = models.EmailField(default='chathuryasdc@gmail.com')
    contact_phone = models.CharField(max_length=50, default='', blank=True)
    address = models.TextField(default='Tech Building Block B, Innovation Way, College Campus, 560100')
    instagram_url = models.URLField(blank=True, default='https://instagram.com')
    facebook_url = models.URLField(blank=True, default='https://facebook.com')
    linkedin_url = models.URLField(blank=True, default='https://linkedin.com')
    github_url = models.URLField(blank=True, default='https://github.com')
    footer_text = models.TextField(default='Official Student Technical & Developer Community dedicated to practical coding bootcamps, workshops, and student tech growth.')
    copyright_text = models.CharField(max_length=200, default='© 2026 Chathurya Student Developers Club. All Rights Reserved.')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.club_name

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class PreviousEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback static image path e.g. images/cs50p.svg")
    date_str = models.CharField(max_length=100, default='2025 – 2026')
    year = models.CharField(max_length=20, default='2026')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    badge_text = models.CharField(max_length=100, default='5-Day Workshop')
    short_description = models.TextField()
    detailed_description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True, help_text="Fallback static image path e.g. images/fullstack.svg")
    duration = models.CharField(max_length=100, default='5 Days (Intensive Sessions)')
    who_can_attend = models.TextField(default='Students from any stream interested in technology.')
    requirements = models.TextField(default='Basic computer knowledge, Laptop recommended')
    capstone_title = models.CharField(max_length=200, blank=True)
    capstone_description = models.TextField(blank=True)
    capstone_tech_flow = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class CourseTopic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    module_number = models.CharField(max_length=20)
    section_title = models.CharField(max_length=200)
    bullets = models.TextField(help_text="Enter bullet points separated by newlines")
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.course.title} - Module {self.module_number}: {self.section_title}"

    def get_bullets_list(self):
        return [b.strip() for b in self.bullets.split('\n') if b.strip()]


class CourseProject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.course.title} Project: {self.title}"


class Registration(models.Model):
    STREAM_CHOICES = [
        ('', 'Select Stream'),
        ('BCA', 'BCA'),
        ('B.Com', 'B.Com'),
        ('BBA', 'BBA'),
        ('B.Com A/F', 'B.Com A/F'),
        ('B.Com Logistics', 'B.Com Logistics'),
        ('B.Com with CA', 'B.Com with CA'),
    ]

    COURSE_CHOICES = [
        ('', 'Select Course'),
        ('Full Stack Development', 'Full Stack Development'),
        ('Data Analytics', 'Data Analytics'),
    ]

    YEAR_CHOICES = [
        ('', 'Select Year of Study'),
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
    ]

    SECTION_CHOICES = [('', 'Select Section')] + [(c, c) for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']]

    LAPTOP_CHOICES = [
        ('', 'Select Laptop Availability'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    registration_id = models.CharField(max_length=50, unique=True, editable=False)
    full_name = models.CharField(max_length=200)
    college_id = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    stream = models.CharField(max_length=50, choices=STREAM_CHOICES)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES)
    year_of_study = models.CharField(max_length=50, choices=YEAR_CHOICES)
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    has_laptop = models.CharField(max_length=50, choices=LAPTOP_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    registration_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registration_date']

    def save(self, *args, **kwargs):
        if not self.registration_id:
            self.registration_id = f"REG-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.college_id}) - {self.course}"


class AttendanceRecord(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='attendance_records')
    course_name = models.CharField(max_length=100)
    session_day = models.IntegerField(default=1, help_text="Day 1 to 15")
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=True)
    scan_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('registration', 'session_day')
        ordering = ['-scan_timestamp']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"Day {self.session_day} - {self.registration.full_name}: {status}"
