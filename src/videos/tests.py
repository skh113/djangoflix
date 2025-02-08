from django.test import TestCase
from django.utils import timezone, text

from .models import Video, PublishStateOptions


class VideoModelTestCase(TestCase):
    MOVIE_TITLE_A = "A movie title for testing"
    MOVIE_TITLE_B = "Another movie title for testing"
    OBJECTS_COUNT = 2
    DRAFT_OBJECTS_COUNT = 1
    PUBLISH_OBJECTS_COUNT = 1

    def setUp(self) -> None:
        Video.objects.create(title=self.MOVIE_TITLE_A, video_id="123")
        Video.objects.create(
            title=self.MOVIE_TITLE_B,
            state=PublishStateOptions.PUBLISH,
            video_id="321",
        )

    def test_valid_title(self):
        query_set = Video.objects.filter(title=self.MOVIE_TITLE_A)
        self.assertTrue(query_set.exists())

    def test_created_count(self):
        query_set = Video.objects.all()
        self.assertEqual(query_set.count(), self.OBJECTS_COUNT)

    def test_slug_field(self):
        query_set = Video.objects.all()

        for item in query_set:
            slug = text.slugify(item.title)
            self.assertEqual(item.slug, slug)

    def test_draft_case(self):
        query_set = Video.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(query_set.count(), self.DRAFT_OBJECTS_COUNT)

    def test_publish_case(self):
        query_set = Video.objects.filter(
            state=PublishStateOptions.PUBLISH, publish_timestamp__lte=timezone.now()
        )
        self.assertTrue(query_set.exists())

    def test_publish_manager(self):
        query_set = Video.objects.all().published()
        query_set_2 = Video.objects.published()
        self.assertTrue(query_set.exists())
        self.assertEqual(query_set.count(), query_set_2.count())
