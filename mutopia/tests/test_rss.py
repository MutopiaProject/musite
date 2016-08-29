from django.test import TestCase
from mutopia.rss import AtomLatestFeed
from datetime import date
from . import tutils

class RSSTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        p = tutils.make_piece()
        p.date_published = date.today()
        p.title = 'RSS Test'
        p.save()

    def test_rss(self):
        feed = AtomLatestFeed()
        self.assertEqual(feed.items()[0].title, 'RSS Test')
