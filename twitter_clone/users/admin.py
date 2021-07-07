from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User, UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = _('User Profile')
    extra = 0


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    inlines = [ProfileInline]
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        },),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Personal info"), {"fields": ("name", "email", "followers")})
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

# admin.site.register(UserProfile)
