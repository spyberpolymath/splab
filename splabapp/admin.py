from django.contrib import admin
from .models import Bug, ContactMessage, SuccessfulFixed, BugMedia, BugCodeFile, BugWebsite

class BugMediaInline(admin.TabularInline):
    model = BugMedia
    extra = 0
    readonly_fields = ('file', 'uploaded_at')

class BugCodeFileInline(admin.TabularInline):
    model = BugCodeFile
    extra = 0
    readonly_fields = ('file', 'uploaded_at')

class BugWebsiteInline(admin.TabularInline):
    model = BugWebsite
    extra = 0
    readonly_fields = ('url',)

class BugAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'status', 'category', 'created_at', 'full_name', 'email', 'phone', 'splab_number')
    search_fields = ('title', 'description', 'full_name', 'email', 'splab_number')
    list_filter = ('severity', 'status', 'category')
    readonly_fields = ('created_at', 'splab_number')
    inlines = [BugMediaInline, BugCodeFileInline, BugWebsiteInline]
    fieldsets = (
        (None, {'fields': ('title', 'description', 'severity', 'category', 'status', 'created_at', 'logs', 'tools_used', 'full_name', 'email', 'phone', 'splab_number')}),
    )

class BugMediaAdmin(admin.ModelAdmin):
    list_display = ('bug', 'file', 'uploaded_at')
    search_fields = ('bug__title', 'file')
    readonly_fields = ('uploaded_at',)

class BugCodeFileAdmin(admin.ModelAdmin):
    list_display = ('bug', 'file', 'uploaded_at')
    search_fields = ('bug__title', 'file')
    readonly_fields = ('uploaded_at',)

class BugWebsiteAdmin(admin.ModelAdmin):
    list_display = ('bug', 'url')
    search_fields = ('bug__title', 'url')

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('subject',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')}),
    )

class SuccessfulFixedAdmin(admin.ModelAdmin):
    list_display = ('bug', 'splab_number', 'description', 'fixed_at', 'evidence_media', 'evidence_code', 'category', 'full_name', 'email', 'phone')
    search_fields = ('bug__title', 'splab_number', 'description', 'full_name', 'email')
    list_filter = ('category', 'fixed_at')
    readonly_fields = ('fixed_at', 'splab_number')
    fieldsets = (
        (None, {'fields': ('bug', 'splab_number', 'description', 'fixed_at', 'evidence_media', 'evidence_code', 'category', 'full_name', 'email', 'phone')}),
    )

admin.site.register(Bug, BugAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(SuccessfulFixed, SuccessfulFixedAdmin)
admin.site.register(BugMedia, BugMediaAdmin)
admin.site.register(BugCodeFile, BugCodeFileAdmin)
admin.site.register(BugWebsite, BugWebsiteAdmin)
