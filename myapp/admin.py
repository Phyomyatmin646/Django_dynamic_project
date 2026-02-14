from django.contrib import admin
from .models import CVModel, BannerModel,AboutModel, ServiceModel, CounterModel,EducationModel, SkillModel, ExperienceModel,ResumeModel,PortfolioModel,BlogSection,BlogPost,PortfolioSection,ContactMessage,ContactSection

admin.site.register(AboutModel)
admin.site.register(ServiceModel)
admin.site.register(CounterModel)
admin.site.register(EducationModel)
admin.site.register(SkillModel)
admin.site.register(ExperienceModel)
admin.site.register(ResumeModel)
admin.site.register(BlogSection)
admin.site.register(BlogPost)
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

