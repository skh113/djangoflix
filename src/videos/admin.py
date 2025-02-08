from django.contrib import admin

from .models import VideoAllProxy, VideoPublishedProxy


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_id', 'is_published']
    list_filter = ['is_active']
    search_fields = ['title', 'description', 'video_id']
    readonly_fields = ['id', 'is_published']

    class Meta:
        model = VideoAllProxy


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title', 'description', 'video_id']

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(is_active=True)


admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
