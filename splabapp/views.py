from django.shortcuts import render, get_object_or_404, redirect
from .models import Bug, SuccessfulFixed, BugMedia, BugCodeFile, BugWebsite
from .forms import ContactForm, CombinedCreateForm, SuccessfulFixedForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404

# Dashboard

@staff_member_required
def dashboard(request):
    date_filter = request.GET.get('date_filter')
    now = timezone.now()
    bugs = Bug.objects.all()
    fixes = SuccessfulFixed.objects.all()
    if date_filter == 'day':
        bugs = bugs.filter(created_at__date=now.date())
        fixes = fixes.filter(fixed_at__date=now.date())
    elif date_filter == 'week':
        week_ago = now - timedelta(days=7)
        bugs = bugs.filter(created_at__gte=week_ago)
        fixes = fixes.filter(fixed_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = now - timedelta(days=30)
        bugs = bugs.filter(created_at__gte=month_ago)
        fixes = fixes.filter(fixed_at__gte=month_ago)
    elif date_filter == 'year':
        year_ago = now - timedelta(days=365)
        bugs = bugs.filter(created_at__gte=year_ago)
        fixes = fixes.filter(fixed_at__gte=year_ago)
    bug_count = bugs.count()
    successful_fixed_count = fixes.count()
    return render(request, 'dashboard.html', {
        'bug_count': bug_count,
        'successful_fixed_count': successful_fixed_count,
        'current_date_filter': date_filter or '',
    })

# Bug Views

def bug_list(request):
    bugs = Bug.objects.all().order_by('-created_at')
    return render(request, 'bug_list.html', {'bugs': bugs})

def bug_detail(request, pk):
    bug = get_object_or_404(Bug, pk=pk)
    return render(request, 'bug_detail.html', {'bug': bug})

# LogEntry Views

def log_list(request):
    logs = LogEntry.objects.all().order_by('-timestamp')
    return render(request, 'log_list.html', {'logs': logs})

def log_detail(request, pk):
    log = get_object_or_404(LogEntry, pk=pk)
    return render(request, 'log_detail.html', {'log': log})

# Tool Views

def tool_list(request):
    tools = Tool.objects.all()
    return render(request, 'tool_list.html', {'tools': tools})

def tool_detail(request, pk):
    tool = get_object_or_404(Tool, pk=pk)
    return render(request, 'tool_detail.html', {'tool': tool})

# MediaFile Views

def mediafile_list(request):
    mediafiles = MediaFile.objects.all().order_by('-uploaded_at')
    return render(request, 'mediafile_list.html', {'mediafiles': mediafiles})

def mediafile_detail(request, pk):
    mediafile = get_object_or_404(MediaFile, pk=pk)
    return render(request, 'mediafile_detail.html', {'mediafile': mediafile})

# Contact view remains public
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent!')
            form = ContactForm()  # Reset form after success
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def combined_create(request):
    if request.method == 'POST':
        form = CombinedCreateForm(request.POST, request.FILES)
        if form.is_valid():
            bug = Bug.objects.create(
                title=form.cleaned_data['bug_title'],
                description=form.cleaned_data['bug_description'],
                severity=form.cleaned_data['bug_severity'],
                category=form.cleaned_data['bug_category'],
                status=form.cleaned_data['bug_status'],
                logs=form.cleaned_data['logs'],
                tools_used=form.cleaned_data['tools_used'],
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
            )
            # Save media files
            for f in request.FILES.getlist('media_files'):
                BugMedia.objects.create(bug=bug, file=f)
            # Save code files
            for f in request.FILES.getlist('code_files'):
                BugCodeFile.objects.create(bug=bug, file=f)
            # Save website URLs
            websites = form.cleaned_data['websites']
            if websites:
                for url in websites.splitlines():
                    url = url.strip()
                    if url:
                        BugWebsite.objects.create(bug=bug, url=url)
            messages.success(request, 'reported success wait for fix the bug')
            return redirect('combined_create')
    else:
        form = CombinedCreateForm()
    return render(request, 'create.html', {'form': form, 'title': 'Create Bug', 'cancel_url': '/'})

def root_redirect(request):
    return redirect('home')

def docs(request):
    return render(request, 'docs.html')

def usage(request):
    return render(request, 'usage.html')

def setup(request):
    return render(request, 'setup.html')

def home(request):
    return render(request, 'home.html')

def successful_fixed_list(request):
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    bugs = Bug.objects.all()
    if category:
        bugs = bugs.filter(category=category)
    if status == 'fixed':
        bugs = [bug for bug in bugs if bug.successful_fixes.count()]
    elif status == 'not_fixed':
        bugs = [bug for bug in bugs if not bug.successful_fixes.count()]
    if search:
        bugs = bugs.filter(title__icontains=search)
    fixes = SuccessfulFixed.objects.select_related('bug').all()
    user_email = getattr(request.user, 'email', None)
    return render(request, 'successful_fixed_list.html', {
        'bugs': bugs,
        'fixes': fixes,
        'user_email': user_email,
        'categories': Bug.CATEGORY_CHOICES,
        'current_category': category,
        'current_status': status,
        'current_search': search,
    })

def successful_fixed_detail(request, pk):
    fix = get_object_or_404(SuccessfulFixed, pk=pk)
    return render(request, 'successful_fixed_detail.html', {'fix': fix})

def successful_fixed_create(request):
    bug = None
    if request.method == 'POST':
        form = SuccessfulFixedForm(request.POST, request.FILES)
        if form.is_valid():
            fix = form.save(commit=False)
            bug = fix.bug
            bug.status = form.cleaned_data['status']
            bug.save()
            fix.full_name = form.cleaned_data['full_name']
            fix.email = form.cleaned_data['email']
            fix.phone = form.cleaned_data['phone']
            if request.FILES.get('evidence_media'):
                fix.evidence_media = request.FILES['evidence_media']
            if request.FILES.get('evidence_code'):
                fix.evidence_code = request.FILES['evidence_code']
            fix.save()
            messages.success(request, 'Successfully fixed!')
            return redirect('successful_fixed_detail', pk=fix.pk)
    else:
        form = SuccessfulFixedForm(request.GET)
        bug_id = request.GET.get('bug')
        if bug_id:
            try:
                bug = Bug.objects.get(pk=bug_id)
            except Bug.DoesNotExist:
                bug = None
    return render(request, 'successful_fixed_form.html', {'form': form, 'title': 'Add Successful Fix', 'bug_details': bug})

def researcher_list(request):
    # Get filter/search params
    filter_category = request.GET.get('category', '')  # 'reporter', 'fixer', or ''
    filter_bug_type = request.GET.get('bug_type', '')
    search_query = request.GET.get('search', '').strip().lower()

    # Prepare researcher entries
    entries = []
    # Bug reporters
    for bug in Bug.objects.all():
        entry = {
            'sno': None,  # will set later
            'splf_id': '',
            'bug_type': bug.category,
            'category': 'Reporter',
            'full_name': bug.full_name,
            'email': bug.email,
            'phone': bug.phone,
            'bug_id': bug.id,
            'bug_title': bug.title,
        }
        entries.append(entry)
    # Successful fixers
    for fix in SuccessfulFixed.objects.select_related('bug').all():
        entry = {
            'sno': None,  # will set later
            'splf_id': fix.splab_number or '',
            'bug_type': fix.category,
            'category': 'Fixer',
            'full_name': fix.full_name,
            'email': fix.email,
            'phone': fix.phone,
            'fix_id': fix.id,
            'bug_id': fix.bug.id if fix.bug else None,
            'bug_title': fix.bug.title if fix.bug else '',
        }
        entries.append(entry)
    # Filtering
    if filter_category:
        entries = [e for e in entries if e['category'].lower() == filter_category.lower()]
    if filter_bug_type:
        entries = [e for e in entries if (e['bug_type'] or '').lower() == filter_bug_type.lower()]
    # Searching
    if search_query:
        entries = [e for e in entries if search_query in (str(e['full_name'] or '').lower() + str(e['email'] or '').lower() + str(e['phone'] or '').lower() + str(e['splf_id'] or '').lower() + str(e['bug_type'] or '').lower() + str(e['category'] or '').lower() + str(e['bug_title'] or '').lower())]
    # Set S.No
    for idx, entry in enumerate(entries, 1):
        entry['sno'] = idx
    # For filter dropdowns
    bug_types = sorted(set((e['bug_type'] or '') for e in entries if e['bug_type']))
    categories = ['Reporter', 'Fixer']
    return render(request, 'researcher_list.html', {
        'researchers': entries,
        'filter_category': filter_category,
        'filter_bug_type': filter_bug_type,
        'search_query': search_query,
        'bug_types': bug_types,
        'categories': categories,
    })

def researcher_detail(request, category, obj_id):
    # category: 'reporter' or 'fixer'
    # obj_id: bug_id (for reporter) or fix_id (for fixer)
    if category.lower() == 'reporter':
        try:
            bug = Bug.objects.get(id=obj_id)
        except Bug.DoesNotExist:
            raise Http404('Bug not found')
        researcher = {
            'splf_id': '',
            'bug_type': bug.category,
            'category': 'Reporter',
            'full_name': bug.full_name,
            'email': bug.email,
            'phone': bug.phone,
            'bug': bug,
            'fix': None,
        }
    elif category.lower() == 'fixer':
        try:
            fix = SuccessfulFixed.objects.select_related('bug').get(id=obj_id)
        except SuccessfulFixed.DoesNotExist:
            raise Http404('Fix not found')
        researcher = {
            'splf_id': fix.splab_number,
            'bug_type': fix.category,
            'category': 'Fixer',
            'full_name': fix.full_name,
            'email': fix.email,
            'phone': fix.phone,
            'bug': fix.bug,
            'fix': fix,
        }
    else:
        raise Http404('Invalid category')
    return render(request, 'researcher_detail.html', {'researcher': researcher})
