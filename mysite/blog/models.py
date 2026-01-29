from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.


class PublishedManager(models.Manager):
    """A custom model manager which retrieves all posts that are published."""

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    objects = models.Manager()  # The default model manager
    publishedObjects = PublishedManager()  # Our custom model manager

    class Meta:
        ordering = ["-published"]
        indexes = [
            models.Index(fields=["-published"]),
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        """A canonical URL is the preferred URL for a resource. You can think
        of it as the URL of the most representative page for specific
        content."""
        return reverse("blog:post_detail", args=[self.id])  # type: ignore


class FavoritePost(models.Model):
    pk = models.CompositePrimaryKey("user", "post")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
