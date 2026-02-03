from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import EmailPostForm
from .models import Post


# Create your views here.


def post_list(request: HttpRequest) -> HttpResponse:
    """
    List all posts.
    """
    post_list = Post.publishedObjects.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(
    request: HttpRequest,
    year: int,
    month: int,
    day: int,
    post: Post,
) -> HttpResponse:
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


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Share a post with another person.
    """
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)

    # Keep track of whether we have sent an email for this post.
    sent = False

    if request.method == "POST":
        # We are submitting the form
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['your_name']} ({cd['your_email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read \"{post.title}\" at {post_url}!\n\n"
                f"{cd['your_name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to_email"]],
            )
            sent = True
    else:
        # We are displaying an empty form
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {
            "post": post,
            "form": form,
            "sent": sent,
        },
    )


# Class-based views


class PostListView(ListView):
    """
    Alternative view for listing all posts.
    """

    queryset = Post.publishedObjects.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"
