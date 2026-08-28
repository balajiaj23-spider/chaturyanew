import re
from django import forms
from .models import Registration, SiteSettings, Course, CourseTopic, PreviousEvent

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = [
            'full_name', 'college_id', 'email', 'phone',
            'stream', 'course', 'year_of_study', 'section', 'has_laptop'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Rahul Sharma', 'id': 'fullName'}),
            'college_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 24CA001', 'id': 'idCardNumber', 'style': 'text-transform: uppercase;', 'oninput': 'this.value = this.value.toUpperCase();'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'rahul.sharma@gmail.com', 'id': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 9876543210', 'maxlength': '10', 'id': 'phone'}),
            'stream': forms.Select(attrs={'class': 'form-control', 'id': 'stream'}),
            'course': forms.Select(attrs={'class': 'form-control', 'id': 'course'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control', 'id': 'className'}),
            'section': forms.Select(attrs={'class': 'form-control', 'id': 'section'}),
            'has_laptop': forms.Select(attrs={'class': 'form-control', 'id': 'hasLaptop'}, choices=[('Yes', 'Yes'), ('No', 'No')]),
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Full name must be at least 2 characters.")
        return name

    def clean_college_id(self):
        college_id = self.cleaned_data.get('college_id', '').strip().upper()
        if college_id and college_id[0].isalpha():
            raise forms.ValidationError("College ID always starts with a number (e.g. 250CB024).")
        if not re.match(r'^[0-9][a-zA-Z0-9-]{2,14}$', college_id):
            raise forms.ValidationError("Please enter a valid College ID starting with a number (e.g. 250CB024).")
        return college_id

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not re.match(r'^[0-9]{10}$', phone):
            raise forms.ValidationError("Please enter a valid 10-digit mobile phone number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        college_id = cleaned_data.get('college_id')
        email = cleaned_data.get('email')

        if college_id:
            # Check for duplicate college_id across ALL courses (Strict 1 course per student)
            existing_id = Registration.objects.filter(college_id__iexact=college_id).first()
            if existing_id:
                raise forms.ValidationError(f"You are already registered for '{existing_id.course}' with College ID '{college_id}'. Students are allowed to register for only 1 course.")

        if email:
            # Check for duplicate email across ALL courses (Strict 1 course per student)
            existing_email = Registration.objects.filter(email__iexact=email).first()
            if existing_email:
                raise forms.ValidationError(f"You are already registered for '{existing_email.course}' with Email '{email}'. Students are allowed to register for only 1 course.")

        return cleaned_data


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'club_name': forms.TextInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'about_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'footer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'copyright_text': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'badge_text': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'who_can_attend': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'capstone_title': forms.TextInput(attrs={'class': 'form-control'}),
            'capstone_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'capstone_tech_flow': forms.TextInput(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CourseTopicForm(forms.ModelForm):
    class Meta:
        model = CourseTopic
        fields = '__all__'
        widgets = {
            'module_number': forms.TextInput(attrs={'class': 'form-control'}),
            'section_title': forms.TextInput(attrs={'class': 'form-control'}),
            'bullets': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'One bullet point per line'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PreviousEventForm(forms.ModelForm):
    class Meta:
        model = PreviousEvent
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_str': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RegistrationAdminForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'college_id': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'stream': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'has_laptop': forms.Select(attrs={'class': 'form-control'}, choices=[('Yes', 'Yes'), ('No', 'No')]),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_college_id(self):
        college_id = self.cleaned_data.get('college_id', '').strip().upper()
        return college_id
