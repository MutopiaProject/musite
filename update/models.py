"""Update-related models.

.. moduleauthor:: Glen Larsen, glenl.glx at gmail.com

"""

from django.db import models
from mutopia.models import Piece, Instrument


class InstrumentMap(models.Model):
    """Normalize instruments by mapping names to specific instruments.

    We want users to specify known instruments in the
    :class:`mutopia.models.Instrument` table but this is not easily
    regulated with user input. The ``RawInstrumentMap`` maps these
    un-regulated names to rows in the
    :class:`mutopia.models.Instrument` table. This table can be used
    for nicknames (*uke* ==> *ukulele*) as well as common
    misspellings, plurals, or foreign names.

    """

    #:An instrument name that may be a nickname (*uke*) or a common
    #:non-English name (*guitarre*) that can be mapped to a name in
    #:the :class:`mutopia.models.Instrument` table.
    raw_instrument = models.CharField(primary_key=True, max_length=64)

    #:Reference to the :class:`mutopia.models.Instrument` table
    instrument = models.ForeignKey(Instrument, models.CASCADE)

    @classmethod
    def translate(cls, candidate):
        """Match a name to an internally known instrument.

        Given an instrument name of dubious quality, attempt to
        translate it to a pre-defined set of instrument names. The
        goal is smooth and accurate searches: we want users to be able
        to find music for a ukulele whether they search using the
        string *uke* or *ukulele*.

        If the given instrument matches one in the
        :class:`mutopia.Instrument` table, just return that name.
        Otherwise, look for match in
        :class:`mutopia.RawInstrumentMap`.

        :param str candidate: The candidate instrument name
        :return: The matched (normalized) instrument
        :rtype: Instrument

        """

        # First try the Instrument table directly
        try:
            instr = Instrument.objects.get(pk=candidate.capitalize())
            return instr
        except Instrument.DoesNotExist:
            # Handle expected exception
            pass

        try:
            imap = InstrumentMap.objects.get(raw_instrument=candidate)
            return imap.instrument
        except InstrumentMap.DoesNotExist:
            # Handle expected exception
            pass

        return None

    def __str__(self):
        return self.raw_instrument
