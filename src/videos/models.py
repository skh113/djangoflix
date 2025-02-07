from django.db import models


class Video(models.Model):
    title = models.CharField()
    description = models.TextField()
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField()
    # timestamp
    # updated
    # state
    # publish_timestamp
