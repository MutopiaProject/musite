from django.test import TestCase
from mutopia.utils import Singleton

@Singleton
class Adder:
    def __init__(self):
        self.ivalue = 0

    def increment(self):
        self.ivalue += 1
        return self.ivalue

    def value(self):
        return self.ivalue


class UtilityTests(TestCase):

    def test_singleton(self):
        s = Adder.Instance()
        self.assertTrue(isinstance(s, Adder))
        s.increment()
        self.assertEqual(s.value(), 1)
        # Get the singleton via another variable
        t = Adder.Instance()
        t.increment()
        self.assertEqual(t.value(), 2)
        # Increment the adder instance directly
        self.assertEqual(Adder.Instance().increment(), 3)

        with self.assertRaises(TypeError):
            bad = Adder()
