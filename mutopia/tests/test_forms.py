from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from mutopia.forms import AdvSearchForm
from . import tutils

class FormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        tutils.load_some_instruments()
        tutils.load_some_styles()
        tutils.load_some_composers()
        
    def test_default_form(self):
        form = AdvSearchForm({})
        self.assertTrue(form.is_valid())
        response = self.client.get(reverse('search'))
        self.assertTemplateUsed(response, 'mutopia/advsearch.html')
