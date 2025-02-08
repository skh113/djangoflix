from django.db import models
from django.utils.text import slugify


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    video_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # timestamp
    # updated
    # state
    # publish_timestamp
    @property
    def is_published(self):
        return self.is_active

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is not already provided
            self.slug = slugify(self.title)  # Generate slug from title

        # Ensure unique slug
        original_slug = self.slug
        counter = 1
        while Video.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'


class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'
