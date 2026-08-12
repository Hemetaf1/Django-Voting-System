from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Category(models.TextChoices):
    ENGINEERING = "ENG", _("فنی مهندسی")
    BASIC       = "BAS", _("علوم پایه و میان رشته‌ای")
    EXPERIMENT  = "EXP", _("علوم تجربی")
    HUMANITY    = "HUM", _("علوم انسانی")
    ARTWORK     = "ART", _("آثار هنری")

class Section(models.Model):
    name     = models.CharField(max_length=120)
    category = models.CharField(max_length=3, choices=Category.choices)
    order    = models.PositiveSmallIntegerField(default=0)
    slug     = models.SlugField(unique=True)                # ← new

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)                   # will produce a Latin slug if name in Latin
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Project(models.Model):
    section     = models.ForeignKey(Section, related_name='projects', on_delete=models.CASCADE)
    title       = models.CharField(max_length=180)
    slug        = models.SlugField(unique=True)
    synopsis    = models.TextField(blank=True)
    is_artwork  = models.BooleanField(default=False)
    image       = models.ImageField(upload_to='project_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Vote(models.Model):
    project    = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "ip_address")

class Feedback(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    score      = models.PositiveSmallIntegerField(help_text="1‑10")
    comment    = models.CharField(max_length=280, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
