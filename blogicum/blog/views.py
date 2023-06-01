from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post


def index(request):
    template = 'blog/index.html'
    current_time = timezone.now()
    post_list = (
        Post.objects.select_related('category')
        .filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        )
        .order_by('-pub_date')
    )
    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    current_time = timezone.now()
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = (
        Post.objects.select_related('category')
        .filter(
            category__slug=category_slug,
            is_published=True,
            pub_date__lte=current_time
        )
        .order_by('-pub_date')
    )
    posts_per_page = 10
    paginator = Paginator(post_list, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=id, is_published=True)
    comments = post.comments.all().order_by('pub_date')
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, template, context)


@login_required
def create_post(request):
    template = 'blog/create.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', request.user.username)
    else:
        form = PostForm()
    return render(request, template, {'form': form})


@login_required
def edit_post(request, post_id):
    template = 'blog/create.html'
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = PostForm(instance=post)
    return render(request, template, {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    template = 'blog/create.html'
    post = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', request.user.username)
    return render(request, template, {'form': form, 'post': post})


@login_required
def add_comment(request, post_id):
    template = 'blog/comment.html'
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = CommentForm()
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


@login_required
def edit_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post=post,
        author=request.user
    )

    if request.method == 'POST':
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    template = 'blog/comment.html'
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post=post,
        author=request.user
    )

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', id=post_id)

    context = {
        'post': post,
        'comment': comment,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile).order_by('-pub_date')
    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def edit_profile(request):
    template = 'blog/user.html'
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username)
    else:
        form = ProfileForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, template, context)
