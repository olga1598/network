
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("save", views.save_changes, name="save"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("toggle_following/<str:profile_username>", views.toggle_following, name="toggle_following"),
    path("following", views.following, name="following"),

    # API route
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like")
]
