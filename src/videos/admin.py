from django.contrib import admin

from .models import VideoAllProxy, VideoPublishedProxy


class VideoAllAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "video_id",
        "is_published",
        "state",
        "playlist_ids",
    ]
    list_filter = [
        "is_active",
        "state",
    ]
    search_fields = ["title", "description", "video_id"]
    readonly_fields = [
        "id",
        "is_published",
        "publish_timestamp",
        "created",
        "updated",
        "playlist_ids",
    ]

    class Meta:
        model = VideoAllProxy


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "video_id",
        "playlist_ids",
    ]
    search_fields = ["title", "description", "video_id"]
    readonly_fields = ["id", "publish_timestamp", "created", "updated", "playlist_ids"]

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(is_active=True)


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
