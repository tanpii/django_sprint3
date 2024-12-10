from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = get_relevant_posts(Post.objects.all())[0:5]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_relevant_posts(Post.objects.all()),
        id=post_id
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.all().filter(is_published=True),
        slug=category_slug
    )
    post_list = get_relevant_posts(
        category.posts.filter(category=category)
    )
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)


def get_relevant_posts(posts):
    return (
        posts.filter(
            is_published=True
        ).filter(
            pub_date__lte=timezone.now()
        ).filter(
            category__is_published=True
        )
    )
