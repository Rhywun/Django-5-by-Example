from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import EmailPostForm
from .models import Post


# Create your views here.


def post_list(request):
    """
    List all posts.
    """
    post_list = Post.publishedObjects.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.get_page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    """
    Display a specific post.
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        published__year=year,
        published__month=month,
        published__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})


def post_share(request, post_id):
    """
    Share a post with another person.
    """
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # We are submitting the form.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # TODO send email
    else:
        # We are displaying an empty form.
        form = EmailPostForm()
    return render(request, "blog/post/share.html",
                  {"post": post, "form": form})


# Class-based views


class PostListView(ListView):
    """
    Alternative view for listing all posts.
    """
    queryset = Post.publishedObjects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
