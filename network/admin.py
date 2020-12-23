from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post

# class CustomUserAdmin(UserAdmin):
#     filter_horizontal = ("following",)
#     fieldsets = UserAdmin.fieldsets + (
#         ("Following", {"fields": ("following",)}),
#     )


# Register your models here.
admin.site.register(User)
# admin.site.register(Follower)
admin.site.register(Post)