from django.utils import timezone, text

from .models import PublishStateOptions


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
    # Lazy import to avoid circular import issues
    from videos.models import Video

    if not instance.slug:
        instance.slug = text.slugify(instance.title)

    # Ensure unique slug
    original_slug = instance.slug
    counter = 1
    while Video.objects.filter(slug=instance.slug).exclude(id=instance.id).exists():
        instance.slug = f"{original_slug}-{counter}"
        counter += 1
