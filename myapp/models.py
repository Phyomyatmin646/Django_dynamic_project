from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class BannerModel(models.Model):
    name      = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    phone     = models.CharField(max_length=20, null=True, blank=True)
    email     = models.EmailField(null=True, blank=True)
    image     = models.ImageField(upload_to='profile/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "No Name"


class CVModel(models.Model):
    cv_file     = models.FileField(upload_to='cv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cv_file.name


class AboutModel(models.Model):
    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class ServiceModel(models.Model):
    icon        = models.CharField(max_length=100)
    title       = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class ResumeModel(models.Model):
    title       = models.CharField(max_length=100)
    subtitle    = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class CounterModel(models.Model):
    number = models.IntegerField()
    suffix = models.CharField(max_length=10, blank=True)
    title  = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class EducationModel(models.Model):
    title       = models.CharField(max_length=100)
    year        = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class SkillModel(models.Model):
    SKILL_TYPE = (
        ('design', 'Design'),
        ('development', 'Development'),
    )
    name       = models.CharField(max_length=50)
    percent    = models.IntegerField()
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPE)

    def __str__(self):
        return self.name


class ExperienceModel(models.Model):
    title       = models.CharField(max_length=100)
    year        = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class PortfolioModel(models.Model):
    CATEGORY_CHOICES = (
        ('development', 'Development'),
        ('design', 'Design'),
        ('wordpress', 'WordPress'),
        ('other', 'Other'),
    )
    title        = models.CharField(max_length=200)
    description  = RichTextField(blank=True, null=True)
    category     = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='development')
    image        = models.ImageField(upload_to='portfolio/')
    project_link = models.URLField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogSection(models.Model):
    title       = models.CharField(max_length=200, default="My Recent Post")
    subtitle    = models.CharField(max_length=255, default="Elevate your brand")
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Blog Section Header"

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    author         = models.CharField(max_length=100, default="Admin")
    date           = models.DateField()
    image          = models.ImageField(upload_to='blog/')
    title          = models.CharField(max_length=255)
    content        = RichTextUploadingField(blank=True, null=True)
    excerpt        = models.TextField(blank=True, help_text="Short summary shown in listing")
    slug           = models.SlugField(unique=True, blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog       = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    body       = models.TextField()
    approved   = models.BooleanField(default=True, help_text="Uncheck to hide this comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.name} on '{self.blog.title}'"


class PortfolioSection(models.Model):
    title       = models.CharField(max_length=200, default="My Completed Work")
    subtitle    = models.CharField(max_length=255, default="Elevate your brand")
    description = models.TextField()

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20)
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class ContactSection(models.Model):
    title       = models.CharField(max_length=200, default="Contact Me")
    subtitle    = models.CharField(max_length=255, default="Get in Touch")
    description = models.TextField()

    def __str__(self):
        return self.title