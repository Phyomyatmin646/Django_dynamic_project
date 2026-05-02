from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    CVModel, BannerModel, AboutModel, ServiceModel, CounterModel,
    EducationModel, SkillModel, ExperienceModel, ResumeModel,
    PortfolioModel, BlogSection, BlogPost, PortfolioSection,
    ContactMessage, ContactSection, Comment
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

   
    context = {
        'profile': BannerModel.objects.first(),
        'about': AboutModel.objects.first(),
        'services': ServiceModel.objects.all(),
        'counters': CounterModel.objects.all(),
        'resume': ResumeModel.objects.first(),
        'education': EducationModel.objects.all(),
        'design_skills': SkillModel.objects.filter(skill_type='design'),
        'dev_skills': SkillModel.objects.filter(skill_type='development'),
        'experience': ExperienceModel.objects.all(),
        'portfolio_items': PortfolioModel.objects.all().order_by('-created_at'),
        'blog_header': BlogSection.objects.first(),
        'blog_posts': BlogPost.objects.all().order_by('-created_at'),
        'portfolio_section': PortfolioSection.objects.first(),
        'contact_section': ContactSection.objects.first(),
    }

    return render(request, 'index.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == "POST":
        name  = request.POST.get("comment-name", "").strip()
        email = request.POST.get("comment-email", "").strip()
        body  = request.POST.get("comment-body", "").strip()

        if name and email and body:
            Comment.objects.create(blog=post, name=name, email=email, body=body)
            messages.success(request, "Your comment has been posted! It will appear once approved.")
        else:
            messages.error(request, "Please fill in all fields before submitting.")

        return redirect("blog_detail", slug=slug)

   
    comments  = post.comments.filter(approved=True).order_by("-created_at")
    related   = BlogPost.objects.exclude(pk=post.pk).order_by("-created_at")[:3]
    
  
    prev_post = BlogPost.objects.filter(created_at__lt=post.created_at).order_by("-created_at").first()
    next_post = BlogPost.objects.filter(created_at__gt=post.created_at).order_by("created_at").first()

    return render(request, "blog-details.html", {
        "post":      post,
        "comments":  comments,
        "related":   related,
        "prev_post": prev_post,
        "next_post": next_post,
    })


def download_cv(request):
    try:
        cv = CVModel.objects.latest('uploaded_at')
        return FileResponse(cv.cv_file.open(), as_attachment=True)
    except CVModel.DoesNotExist:
        raise Http404("CV not found")