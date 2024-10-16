from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import models
from django.utils import timezone


class StaffRequiredMixin(UserPassesTestMixin):
    # Define the test function to check if the user is staff
    def test_func(self):
        return self.request.user.is_staff

    # Redirect if the user fails the test (not staff)
    def handle_no_permission(self):
        return redirect('staff_login')


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    file = models.FileField(upload_to='projects/files/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Set default to current time
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
