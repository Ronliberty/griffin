from django.db import models
from django.contrib.auth.models import User  # Import User model
from griffin.models import Project  # Assuming Project is in the griffin app



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    fb_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('available', 'available'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('on-hold', 'On Hold'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    accepted = models.BooleanField(default=False)
    completed_on = models.DateTimeField(auto_now_add=True)  # Allow null if not yet completed

    def __str__(self):
        return f"{self.user.username} accepted {self.project.name}"
