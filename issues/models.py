from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.text import slugify

User = get_user_model()

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

class Issue(models.Model):

    STATUS_CHOICES = [

        ('p','Pending'),
        ('v','Verified'),
        ('o', 'Open'),
        ('ip', 'In Progress'),
        ('r', 'Resolved')
    ]

    issue_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='issues', null=True, blank=True)
    address = models.TextField()
    image = models.ImageField(upload_to="issues/", null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='p')
    verified_point_awarded = models.BooleanField(default=False)
    resolved_point_awarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Location(models.Model):

    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name='location')
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.latitude}, {self.longitude}"