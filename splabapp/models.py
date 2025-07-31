from django.db import models
import random

# Create your models here.

class Bug(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    CATEGORY_CHOICES = [
        ('ui', 'UI'),
        ('backend', 'Backend'),
        ('performance', 'Performance'),
        ('security', 'Security'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=200, verbose_name='Bug Title', help_text='Bug’s title')
    description = models.TextField(verbose_name='Description', help_text='Full bug description')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, verbose_name='Severity', help_text='Low / Medium / High / Critical')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other', verbose_name='Category', help_text='UI / Backend / Performance / Security / Other')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open', verbose_name='Status', help_text='Open / In Progress / Resolved / Closed')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At', help_text='Timestamp when bug was created')
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Reporter Name', help_text='Full name of the person reporting')
    email = models.EmailField(null=True, blank=True, verbose_name='Reporter Email', help_text='Email of the person reporting')
    phone = models.CharField(max_length=20, verbose_name='Reporter Phone', help_text='Phone number of the person reporting')
    splab_number = models.CharField(max_length=8, unique=True, blank=True, null=True, verbose_name='SPLAB Number', help_text='Auto-generated bug ID (e.g. SPLB1234)')
    logs = models.TextField(blank=True, help_text='Logs entered during bug submission (one per line)', verbose_name='Logs')
    tools_used = models.TextField(blank=True, help_text='List of tools used (one per line)', verbose_name='Tools Used')

    def __str__(self):
        return f"{self.title} ({self.severity}, {self.category})"

    def save(self, *args, **kwargs):
        if not self.splab_number:
            while True:
                num = f'SPLB{random.randint(1000, 9999)}'
                if not Bug.objects.filter(splab_number=num).exists():
                    self.splab_number = num
                    break
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('bug', 'Report a Bug'),
        ('tool', 'Tool Suggestion'),
        ('media', 'Media Inquiry'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"

class SuccessfulFixed(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='successful_fixes', verbose_name='Related Bug', help_text='The bug this fix is for')
    splab_number = models.CharField(max_length=8, unique=True, blank=True, null=True, verbose_name='SPLF Number', help_text='Auto-generated SPLF ID (e.g. SPLF5678)')
    description = models.TextField(verbose_name='Fix Description', help_text='Explanation of the fix')
    fixed_at = models.DateTimeField(auto_now_add=True, verbose_name='Fixed At', help_text='When the fix was submitted')
    evidence_media = models.FileField(upload_to='fix_evidence/media/', blank=True, null=True, verbose_name='Fix Evidence Media', help_text='Screenshot/video proof of the fix')
    evidence_code = models.FileField(upload_to='fix_evidence/code/', blank=True, null=True, verbose_name='Fix Evidence Code', help_text='Code patch or script that solved the issue')
    category = models.CharField(max_length=20, choices=Bug.CATEGORY_CHOICES, default='other', verbose_name='Category', help_text='Category of the bug')
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Fixed By Name', help_text='Full name of the person who fixed')
    email = models.EmailField(null=True, blank=True, verbose_name='Fixed By Email', help_text='Email of the person who fixed')
    phone = models.CharField(max_length=20, verbose_name='Fixed By Phone', help_text='Phone number of the person who fixed')

    def save(self, *args, **kwargs):
        if self.bug:
            self.category = self.bug.category
        if not self.splab_number:
            while True:
                num = f'SPLF{random.randint(1000, 9999)}'
                if not SuccessfulFixed.objects.filter(splab_number=num).exists():
                    self.splab_number = num
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Fix for {self.bug.title} at {self.fixed_at}"

class BugMedia(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='media_files', verbose_name='Related Bug', help_text='The bug this media is for')
    file = models.FileField(upload_to='bug_media/', verbose_name='Media File', help_text='Image or video file')  # Accepts images and videos
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At', help_text='When the media was uploaded')

class BugCodeFile(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='code_files', verbose_name='Related Bug', help_text='The bug this code file is for')
    file = models.FileField(upload_to='bug_code/', verbose_name='Code File', help_text='Code file (proof-of-concept, exploit, patch)')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At', help_text='When the code file was uploaded')

class BugWebsite(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='websites', verbose_name='Related Bug', help_text='The bug this website is for')
    url = models.URLField(verbose_name='Website URL', help_text='Site associated with the bug')
