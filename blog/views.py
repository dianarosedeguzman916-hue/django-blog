from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

def post_list_view(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=pk)
    else:
        form = CommentForm()
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form})

@login_required
def post_create_view(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:post_detail", pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, "blog/post_form.html", {"form": form})

@login_required
def post_update_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        return redirect("blog:post_list")
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form})

@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect("blog:post_list")

@login_required
def add_comment_view(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("blog:post_detail", pk=pk)