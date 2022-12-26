from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User

"""Get page_obj"""


def _page_obj(request, mod_obj):
    paginator = Paginator(mod_obj, settings.COUNT_POSTS_ON_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.select_related(
        "group",
        "author",
    ).all()
    page_obj = _page_obj(request, posts)
    context = {
        "page_obj": page_obj,
    }
    template = "posts/index.html"
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = _page_obj(request, posts)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    template = "posts/group_list.html"
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related("group")
    post_count = posts.count()
    page_obj = _page_obj(request, posts)
    following = False
    following = Follow.objects.filter(
        user=request.user.is_authenticated,
        author=author,
    ).exists()
    context = {
        "post_count": post_count,
        "author": author,
        "page_obj": page_obj,
        "following": following,
    }
    template = "posts/profile.html"
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    count = post.author.posts.all().count()
    form = CommentForm(request.POST or None)
    comment = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "count": count,
        "form": form,
        "comments": comment,
    }
    template = "posts/post_detail.html"
    return render(request, template, context)


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    template_name = "posts/create_post.html"
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        username = form.author
        form.save()
        return redirect("posts:profile", username)
    context = {
        "form": form,
        "is_edit": False,
    }
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    template_name = "posts/create_post.html"
    if form.is_valid():
        post.save()
        return redirect("posts:post_detail", post_id)
    context = {
        "post": post,
        "form": form,
        "is_edit": True,
    }
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    post = Post.objects.select_related("author").filter(
        author__following__user=request.user
    )
    page_obj = _page_obj(request, post)
    context = {"page_obj": page_obj}
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if (
        author != request.user
        and not Follow.objects.filter(
            user=request.user,
            author=author
        ).exists()
    ):
        Follow.objects.create(user=request.user, author=author)
    return redirect("posts:profile", username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:profile", username)
