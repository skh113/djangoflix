from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone, text


class PublishStateOptions(models.TextChoices):
    PUBLISH = "PU", "Publish"
    DRAFT = "DR", "Draft"
    UNLISTED = "UN", "Unlisted"
    PRIVATE = "PR", "Private"


class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=now
        )


class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    video_id = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    state = models.CharField(
        max_length=2,
        choices=PublishStateOptions.choices,
        default=PublishStateOptions.DRAFT,
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


def publish_state_pre_save(sender, instance, *args, **kwargs):
    is_publish = instance.state == PublishStateOptions.PUBLISH
    is_draft = instance.state == PublishStateOptions.DRAFT
    is_unlisted = instance.state == PublishStateOptions.UNLISTED
    is_private = instance.state == PublishStateOptions.PRIVATE

    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif is_draft or is_unlisted or is_private:
        instance.publish_timestamp = None


def slugify_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = text.slugify(instance.title)

    # Ensure unique slug
    original_slug = instance.slug
    counter = 1
    while Video.objects.filter(slug=instance.slug).exclude(id=instance.id).exists():
        instance.slug = f"{original_slug}-{counter}"
        counter += 1


pre_save.connect(publish_state_pre_save, sender=Video)
pre_save.connect(slugify_pre_save, sender=Video)
