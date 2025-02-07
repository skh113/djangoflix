from django.test import TestCase

from .models import Video


class VideoModelTestCase(TestCase):
    MOVIE_TITLE = 'A movie title for testing'

    def setUp(self) -> None:
        Video.objects.create(title=self.MOVIE_TITLE)

    def test_valid_title(self):
        query_set = Video.objects.filter(title=self.MOVIE_TITLE)
        self.assertTrue(query_set.exists())

    def test_created_count(self):
        query_set = Video.objects.all()
        self.assertEqual(query_set.count(), 1)
