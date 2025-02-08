from django.contrib import admin

from .models import VideoAllProxy, VideoPublishedProxy


class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    list_filter = ['video_id']
    search_fields = ['title', 'description', 'video_id']

    class Meta:
        model = VideoAllProxy


admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    list_filter = ['video_id']
    search_fields = ['title', 'description', 'video_id']

    class Meta:
        model = VideoPublishedProxy

    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(is_active=True)


admin.site.register(VideoPublishedProxy, VideoProxyAdmin)
