from django.db import models
from django.utils import timezone

class Visitor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    otp_sent_at = models.DateTimeField(null=True, blank=True)
    blocked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

class Paper(models.Model):
    CATEGORY_CHOICES = [
        ("book", "Book"),
        ("publication", "Publication"),
    ]

    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to="pdfs/")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    def __str__(self):
        return self.title   
    
class AccessLog(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor.email} → {self.paper.title}"
    

class AcademicSection(models.Model):
    SECTION_CHOICES = [
        ("qualification", "Academic Qualification"),
        ("fellowship", "Visiting Fellowship"),
        ("honour", "Honour / Award"),
        ("major_project", "Major Project"),
        ("minor_project", "Minor Project"),
        ("timeline", "Timeline Entry"),
    ]

    section_type = models.CharField(max_length=50, choices=SECTION_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    year = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.section_type} — {self.title}"


from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.db import models

class GalleryEvent(models.Model):
    title = models.CharField(max_length=255)
    event_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    event = models.ForeignKey(
        GalleryEvent,
        related_name="images",
        on_delete=models.CASCADE,
        null=True,      # TEMP
        blank=True      # TEMP
    )
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255, blank=True)





    

 
