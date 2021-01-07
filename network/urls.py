
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("post/all", views.all_posts_view, name="view_all_posts"),
    path("post/id/<int:post_id>", views.single_post_view, name="view_single_post_by_id")
]
