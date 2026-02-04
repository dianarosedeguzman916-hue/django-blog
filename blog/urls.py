from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path("post/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("post/create/", views.post_create_view, name="post_create"),
    path("post/<int:pk>/update/", views.post_update_view, name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    path("post/<int:pk>/comment/", views.add_comment_view, name="add_comment"),
]