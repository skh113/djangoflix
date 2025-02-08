from django.test import TestCase
from django.utils import timezone

from .models import Video


class VideoModelTestCase(TestCase):
    MOVIE_TITLE = "A movie title for testing"
    OBJECTS_COUNT = 2
    DRAFT_OBJECTS_COUNT = 1
    PUBLISH_OBJECTS_COUNT = 1

    def setUp(self) -> None:
        Video.objects.create(title=self.MOVIE_TITLE, video_id="123")
        Video.objects.create(
            title=self.MOVIE_TITLE, state=Video.VideoStateOptions.PULISH, video_id="321"
        )

    def test_valid_title(self):
        query_set = Video.objects.filter(title=self.MOVIE_TITLE)
        self.assertTrue(query_set.exists())

    def test_created_count(self):
        query_set = Video.objects.all()
        self.assertEqual(query_set.count(), self.OBJECTS_COUNT)

    def test_draft_case(self):
        query_set = Video.objects.filter(state=Video.VideoStateOptions.DRAFT)
        self.assertEqual(query_set.count(), self.DRAFT_OBJECTS_COUNT)

    def test_publish_case(self):
        query_set = Video.objects.filter(
            state=Video.VideoStateOptions.PULISH, publish_timestamp__lte=timezone.now()
        )
        self.assertTrue(query_set.exists())
