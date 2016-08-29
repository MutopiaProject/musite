from django.test import TestCase
from django.utils import timezone
from mutopia import Instrument
from update import Marker, InstrumentMap

class MarkerTest(TestCase):

    def test_marker(self):
        marker = Marker.create()
        self.assertTrue(isinstance(marker, Marker))
        self.assertTrue(str(marker))

class InstrumentMapTests(TestCase):

    def test_instrument_map(self):
        bagpipe,_ = Instrument.objects.get_or_create(instrument='bagpipe')
        self.assertTrue(isinstance(bagpipe, Instrument))
        InstrumentMap.objects.create(raw_instrument='Windbag',
                                     instrument=bagpipe)
        self.assertEqual(InstrumentMap.translate('Windbag'), bagpipe)
