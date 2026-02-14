from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.contrib import messages 
from .models import (
    CVModel, BannerModel, AboutModel, ServiceModel, CounterModel,
    EducationModel, SkillModel, ExperienceModel, ResumeModel, 
    PortfolioModel, BlogSection, BlogPost, PortfolioSection, ContactMessage, ContactSection
)

def Homepage(request):
   
    if request.method == "POST":
        name = request.POST.get('contact-name')
        email = request.POST.get('contact-email')
        phone = request.POST.get('contact-phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('contact-message')

        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text
        )

        
        messages.success(request, "Thank you! Your message has been sent successfully.")
        
       
        return redirect('/#contacts') 
    
    resume = ResumeModel.objects.first()
    education = EducationModel.objects.all()
    design_skills = SkillModel.objects.filter(skill_type='design')
    dev_skills = SkillModel.objects.filter(skill_type='development')
    experience = ExperienceModel.objects.all()
    about = AboutModel.objects.first()
    services = ServiceModel.objects.all()
    counters = CounterModel.objects.all()
    profile = BannerModel.objects.first()
    portfolio_items = PortfolioModel.objects.all().order_by('-created_at')
    blog_header = BlogSection.objects.first() 
    blog_posts = BlogPost.objects.all()
    portfolio_section = PortfolioSection.objects.first()
    contact_section = ContactSection.objects.first()

    context = {
        'profile': profile,
        'about': about,
        'services': services,
        'counters': counters,
        'resume': resume,
        'education': education,
        'design_skills': design_skills,
        'dev_skills': dev_skills,
        'experience': experience,
        'portfolio_items': portfolio_items,
        'blog_header': blog_header, 
        'blog_posts': blog_posts,
        'portfolio_section': portfolio_section,
        'contact_section': contact_section,
    }

    return render(request, 'index.html', context)

def download_cv(request):
    try:
        cv = CVModel.objects.latest('uploaded_at')
        return FileResponse(cv.cv_file.open(), as_attachment=True)
    except CVModel.DoesNotExist:
        raise Http404("CV not found")