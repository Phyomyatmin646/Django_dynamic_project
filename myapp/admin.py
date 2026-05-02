from django.contrib import admin
from .models import (
    CVModel, BannerModel, AboutModel, ServiceModel, CounterModel,
    EducationModel, SkillModel, ExperienceModel, ResumeModel,
    PortfolioModel, BlogSection, BlogPost, PortfolioSection,
    ContactMessage, ContactSection, Comment
)

admin.site.register(AboutModel)
admin.site.register(ServiceModel)
admin.site.register(CounterModel)
admin.site.register(EducationModel)
admin.site.register(SkillModel)
admin.site.register(ExperienceModel)
admin.site.register(ResumeModel)
admin.site.register(BlogSection)
admin.site.register(PortfolioSection)
admin.site.register(ContactMessage)
admin.site.register(ContactSection)


@admin.register(BannerModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'phone', 'email')


@admin.register(CVModel)
class CVAdmin(admin.ModelAdmin):
    list_display = ('cv_file', 'uploaded_at')


@admin.register(PortfolioModel)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'blog', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'body')
    list_editable = ('approved',)
    readonly_fields = ('name', 'email', 'body', 'blog', 'created_at')