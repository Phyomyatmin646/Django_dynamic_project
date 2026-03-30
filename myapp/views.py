from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    CVModel, BannerModel, AboutModel, ServiceModel, CounterModel,
    EducationModel, SkillModel, ExperienceModel, ResumeModel, 
    PortfolioModel, BlogSection, BlogPost, PortfolioSection, ContactMessage, ContactSection
)

def Homepage(request):
    if request.method == "POST":
       
        form_type = request.POST.get('form_type', 'appointment')
        
        name = request.POST.get('contact-name')
        email = request.POST.get('contact-email')
        phone = request.POST.get('contact-phone')
        subject = request.POST.get('subject', 'No Subject')
        message_text = request.POST.get('contact-message', 'No Message Provided')

       
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=f"[{form_type.upper()}] {subject}",
            message=message_text
        )

       
        if form_type == "hire_me":
            project_type = request.POST.get('project_type', 'N/A')
            freelance_type = request.POST.get('freelance_type', 'N/A')
            
            full_email_body = f"""
            Hello Phyo Myat Min,
            
            You have a new Hire Request (Freelance).
            
            Client: {name}
            Email: {email}
            Phone: {phone}
            
            Project Details:
            - Category: {project_type}
            - Freelance Type: {freelance_type}
            
            Subject: {subject}
            Message:
            {message_text}
            """

            try:
                send_mail(
                    subject=f"Freelance Inquiry: {subject}",
                    message=full_email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['phyomyatmin646@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Hire request sent to Gmail successfully!")
            except Exception as e:
                messages.warning(request, "Message saved, but failed to send Gmail notification.")
        else:
            
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