from django.contrib import admin
from .models import SiteSettings, PreviousEvent, Course, CourseTopic, CourseProject, Registration

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('club_name', 'college_name', 'contact_email', 'contact_phone')

@admin.register(PreviousEvent)
class PreviousEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'date_str', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    search_fields = ('title', 'description')

class CourseTopicInline(admin.TabularInline):
    model = CourseTopic
    extra = 1

class CourseProjectInline(admin.TabularInline):
    model = CourseProject
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'duration', 'is_active', 'display_order')
    list_editable = ('is_active', 'display_order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseTopicInline, CourseProjectInline]

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'registration_id', 'full_name', 'college_id', 'email',
        'phone', 'stream', 'course', 'year_of_study', 'section',
        'has_laptop', 'status', 'registration_date'
    )
    list_filter = ('course', 'stream', 'year_of_study', 'section', 'status', 'has_laptop')
    search_fields = ('registration_id', 'full_name', 'college_id', 'email', 'phone')
    readonly_fields = ('registration_id', 'registration_date')
    ordering = ('-registration_date',)
