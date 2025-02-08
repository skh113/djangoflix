from django.test import TestCase
from django.utils import timezone, text
from djangoflix.db.models import PublishStateOptions
from videos.models import Video

from .models import Playlist


class PlaylistModelTestCase(TestCase):
    VIDEO_A = {"title": "Test Video", "video_id": "123"}
    PLAYLIST_A = {"title": "A playlist title for testing"}
    PLAYLIST_B = {"title": "Another playlist title for testing"}
    OBJECTS_COUNT = 2
    DRAFT_OBJECTS_COUNT = 1
    PUBLISH_OBJECTS_COUNT = 1

    def setUp(self) -> None:
        self.video = Video.objects.create(
            title=self.VIDEO_A["title"], video_id=self.VIDEO_A["video_id"]
        )
        self.playlist_a = Playlist.objects.create(
            title=self.PLAYLIST_A["title"], video=self.video
        )
        self.playlist_b = Playlist.objects.create(
            title=self.PLAYLIST_B["title"],
            state=PublishStateOptions.PUBLISH,
            video=self.video,
        )

    def test_playlist_video(self):
        self.assertEqual(self.playlist_a.video, self.video)

    def test_video_playlist(self):
        query_set = self.video.playlist_set.all()
        self.assertEqual(query_set.count(), self.OBJECTS_COUNT)

    def test_valid_title(self):
        query_set = Playlist.objects.filter(title=self.playlist_a.title)
        self.assertTrue(query_set.exists())

    def test_created_count(self):
        query_set = Playlist.objects.all()
        self.assertEqual(query_set.count(), self.OBJECTS_COUNT)

    def test_slug_field(self):
        query_set = Playlist.objects.all()

        for item in query_set:
            slug = text.slugify(item.title)
            self.assertEqual(item.slug, slug)

    def test_draft_case(self):
        query_set = Playlist.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(query_set.count(), self.DRAFT_OBJECTS_COUNT)

    def test_publish_case(self):
        query_set = Playlist.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=timezone.now()
        )
        self.assertTrue(query_set.exists())

    def test_publish_manager(self):
        query_set = Playlist.objects.all().published()
        query_set_2 = Playlist.objects.published()
        self.assertTrue(query_set.exists())
        self.assertEqual(query_set.count(), query_set_2.count())
