from django.db import models
from django.utils import timezone, text


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=Video.VideoStateOptions.PUBLISH, publish_timestamp__lte=now
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    class VideoStateOptions(models.TextChoices):
        PUBLISH = "PU", "Publish"
        DRAFT = "DR", "Draft"
        UNLISTED = "UN", "Unlisted"
        PRIVATE = "PR", "Private"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    video_id = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2, choices=VideoStateOptions.choices, default=VideoStateOptions.DRAFT
    )
    publish_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = VideoManager()

    @property
    def is_published(self):
        return self.is_active

    def save(self, *args, **kwargs):
        if (
            self.state == self.VideoStateOptions.PUBLISH
            and self.publish_timestamp is None
        ):
            self.publish_timestamp = timezone.now()
        elif (
            self.state == self.VideoStateOptions.DRAFT
            or self.state == self.VideoStateOptions.UNLISTED
            or self.state == self.VideoStateOptions.PRIVATE
        ):
            self.publish_timestamp = None

        if not self.slug:  # If slug is not already provided
            self.slug = text.slugify(self.title)  # Generate slug from title

        # Ensure unique slug
        original_slug = self.slug
        counter = 1
        while Video.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"
