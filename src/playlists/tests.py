from django.test import TestCase
from django.utils import timezone, text
from djangoflix.db.models import PublishStateOptions
from videos.models import Video

from .models import Playlist


class PlaylistModelTestCase(TestCase):
    VIDEO_A = {"title": "Test Video 1", "video_id": "123"}
    VIDEO_B = {"title": "Test Video 2", "video_id": "12"}
    VIDEO_C = {"title": "Test Video 3", "video_id": "1"}
    PLAYLIST_A = {"title": "A playlist title for testing"}
    PLAYLIST_B = {"title": "Another playlist title for testing"}
    OBJECTS_COUNT = 2
    DRAFT_OBJECTS_COUNT = 1
    PUBLISH_OBJECTS_COUNT = 1

    def create_videos(self):
        self.video_a = Video.objects.create(
            title=self.VIDEO_A["title"], video_id=self.VIDEO_A["video_id"]
        )
        self.video_b = Video.objects.create(
            title=self.VIDEO_B["title"], video_id=self.VIDEO_B["video_id"]
        )
        self.video_c = Video.objects.create(
            title=self.VIDEO_C["title"], video_id=self.VIDEO_C["video_id"]
        )
        self.videos = [self.video_a, self.video_b, self.video_c]

    def setUp(self) -> None:
        self.create_videos()
        self.playlist_a = Playlist.objects.create(
            title=self.PLAYLIST_A["title"], video=self.video_a
        )
        self.playlist_b = Playlist.objects.create(
            title=self.PLAYLIST_B["title"],
            state=PublishStateOptions.PUBLISH,
            video=self.video_a,
        )
        self.playlist_b.videos.set(self.videos)
        self.playlist_b.save()

    def test_playlist_video(self):
        self.assertEqual(self.playlist_a.video, self.video_a)

    def test_playlist_video_items(self):
        count = self.playlist_b.videos.all().count()
        self.assertEqual(count, len(self.videos))

    def test_video_playlist_ids_propery(self):
        ids = self.playlist_a.video.playlist_ids()
        acutal_ids = list(
            Playlist.objects.filter(video=self.video_a).values_list("id", flat=True)
        )
        self.assertEqual(ids, acutal_ids)

    def test_video_playlist(self):
        query_set = self.video_a.playlist_featured.all()
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
