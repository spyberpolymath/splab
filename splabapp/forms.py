from django import forms
from .models import Bug, ContactMessage, SuccessfulFixed, BugMedia, BugCodeFile, BugWebsite

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Your Name',
            'email': 'Your Email',
            'phone': 'Your Phone',
            'subject': 'Subject',
            'message': 'Your Message'
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg shadow-sm'
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
            if field_name == 'message':
                field.widget.attrs['rows'] = 5

class SuccessfulFixedForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Bug.STATUS_CHOICES, label='Update Bug Status')
    full_name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Phone')
    evidence_media = forms.FileField(required=False, label='Evidence Image/Video')
    evidence_code = forms.FileField(required=False, label='Evidence Code File')
    class Meta:
        model = SuccessfulFixed
        fields = ['bug', 'description', 'status', 'full_name', 'email', 'phone', 'evidence_media', 'evidence_code']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'bug': 'Select Bug',
            'description': 'Describe how you fixed the bug',
            'status': 'Update Bug Status',
            'full_name': 'Your Name',
            'email': 'Your Email',
            'phone': 'Your Phone',
            'evidence_media': 'Upload image or video',
            'evidence_code': 'Upload code file',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg shadow-sm'
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
            if field_name == 'description':
                field.widget.attrs['rows'] = 5
        self.fields['bug'].widget.attrs['onchange'] = 'this.form.submit();'

class CombinedCreateForm(forms.Form):
    # Bug fields
    bug_title = forms.CharField(max_length=200, label='Bug Title')
    bug_description = forms.CharField(widget=forms.Textarea, label='Bug Description')
    bug_severity = forms.ChoiceField(choices=Bug.SEVERITY_CHOICES, label='Bug Severity')
    bug_category = forms.ChoiceField(choices=Bug.CATEGORY_CHOICES, label='Bug Category')
    bug_status = forms.ChoiceField(choices=Bug.STATUS_CHOICES, label='Bug Status')
    logs = forms.CharField(widget=forms.Textarea, required=False, label='Logs (one per line)')
    tools_used = forms.CharField(widget=forms.Textarea, required=False, label='Tools Used (one per line)')
    media_files = forms.FileField(required=False, label='Media Files (images/videos, multiple allowed)')
    code_files = forms.FileField(required=False, label='Code Files (multiple allowed)')
    websites = forms.CharField(widget=forms.Textarea, required=False, label='Website URLs (one per line)')
    full_name = forms.CharField(max_length=100, label='Full Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=20, label='Phone')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'bug_title': 'Enter bug title',
            'bug_description': 'Describe the bug',
            'bug_severity': 'Select severity',
            'bug_category': 'Select category',
            'bug_status': 'Select status',
            'logs': 'Paste logs here (one per line)',
            'tools_used': 'List tools used (one per line)',
            'media_files': 'Upload images/videos',
            'code_files': 'Upload code files',
            'websites': 'List website URLs (one per line)',
            'full_name': 'Your Name',
            'email': 'Your Email',
            'phone': 'Your Phone',
        }
        for field_name, field in self.fields.items():
            # FileFields don't support placeholder
            if field_name not in ['media_files', 'code_files']:
                field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
            field.widget.attrs['class'] = 'form-control form-control-lg shadow-sm'
            if field_name in ['bug_description', 'logs', 'tools_used', 'websites']:
                field.widget.attrs['rows'] = 5 