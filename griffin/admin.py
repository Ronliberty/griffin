from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            # Only superusers can assign staff status
            super().save_model(request, obj, form, change)
        else:
            # Prevent non-superusers from setting is_staff
            form.cleaned_data['is_staff'] = False
            super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
