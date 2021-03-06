from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from mutopia.forms import KeySearchForm
from mutopia.views import handler404, key_results
from mutopia.models import Composer, Instrument, Style, AssetMap, LPVersion
from . import tutils


class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        tutils.load_some_composers()
        tutils.load_some_styles()
        tutils.load_some_instruments()
        tutils.init_fts()
        # To test piece info we need to create the piece as well as
        # the asset map.
        cls.p = tutils.make_piece(piece_id=2, title='St. James Infirmary')
        asset = AssetMap.objects.create(piece=cls.p,
                                        folder='/'.join([str(cls.p.composer),
                                                         'various',]),
                                        name='st-james-infirmary',
                                        has_lys=False)
        asset.save()

    def test_404(self):
        factory = RequestFactory()
        request = factory.get('/badurl')
        response = handler404(request)
        self.assertEqual(response.status_code, 404)


    def check_menu(self, name, template):
        response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)


    def test_all_menus(self):
        p = [('home', 'index.html'),
             ('browse', 'browse.html'),
             ('search', 'advsearch.html'),
             ('legal', 'legal.html'),
             ('contribute', 'contribute.html'),
             ('contact', 'contact.html'),
        ]
        for (name,template) in p:
            self.check_menu(name, '/'.join(['mutopia', template,]))


    def test_adv_results(self):
        response = self.client.get(reverse('adv-results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/results.html')


    def test_key_results(self):
        response = self.client.get(reverse('key-results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/results.html')


    def test_piece_info(self):
        response = self.client.get(reverse('piece-info', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_info.html')


    def test_piece_by_version(self):
        # Just get the first version we find. It has to be there since
        # we created a piece in setup.
        v = LPVersion.objects.all()[0]
        response = self.client.get(reverse('piece-by-version',
                                           args=[v.version]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_version.html')


    def test_piece_by_composer(self):
        c = Composer.objects.all()[0]
        response = self.client.get(reverse('piece-by-composer',
                                           args=[c.composer]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_composer.html')


    def test_piece_by_style(self):
        s = Style.objects.all()[0]
        response = self.client.get(reverse('piece-by-style', args=[s.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_style.html')


    def test_piece_by_instrument(self):
        i = Instrument.objects.all()[0]
        response = self.client.get(reverse('piece-by-instrument',
                                           args=[i.instrument]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_instrument.html')


    def test_log_info(self):
        response = self.client.get(reverse('piece-log', args=[self.p.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mutopia/piece_log.html')
