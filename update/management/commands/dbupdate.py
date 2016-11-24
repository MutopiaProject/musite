"""Django command for updating the database from the AssetMap.
"""

import re
import os
import logging
from urllib.error import HTTPError
from django.core.management.base import BaseCommand
from django.db import transaction
from rdflib import Graph, URIRef, Namespace, URIRef
from rdflib.term import Literal
from mutopia.models import Composer, Style, Piece, Contributor
from mutopia.models import LPVersion, AssetMap, License
from update.models import Instrument, InstrumentMap
from mutopia.search import SearchTerm
from mutopia.utils import FTP_URL, parse_mutopia_id

logger = logging.getLogger('update')

MP = Namespace('http://www.mutopiaproject.org/piece-data/0.1/')


class Command(BaseCommand):
    help = """Database load utility for the mutopia application."""

    def update_instruments(self):
        """Update the instrument list for any piece that is missing
        instruments.
        """
        pat = re.compile('\W+')
        pieces = Piece.objects.all().filter(instruments__isnull=True)
        for p in pieces:
            mlist = set()
            ilist = pat.split(p.raw_instrument)
            for i in ilist:
                instrument = i.strip()
                if len(instrument) < 3: next
                t = InstrumentMap.translate(instrument)
                if t:
                    mlist.add(t)
            if len(mlist) == 0:
                logger.info('No instruments added for %s' % p)
                next

            for instr in mlist:
                p.instruments.add(instr)
                logger.info('Added %s to %s' % (instr,p))


    def update_pieces(self):
        # get all RDF specs with a null piece reference
        rmap = AssetMap.objects.all().filter(published=False)
        published = []
        for asset in rmap:
            path = asset.get_rdfspec()
            logger.info('Reading RDF %s' % path)
            try:
                graph = Graph().parse(URIRef(path))
            except (FileNotFoundError, HTTPError):
                # This AssetMap element is invalid somehow.
                logger.info('Removing %s from consideration.' % asset)
                asset.delete()
                continue

            # Because our RDF's are defined as 'rdf:about:"."' the subject
            # is an URI reference to the containing folder.
            mp_subj = URIRef('/'.join([FTP_URL, asset.folder,]) + '/')

            # A footer isn't stored in the database but its bit parts are.
            footer = graph.value(mp_subj, MP.id)
            if footer is None:
                logger.warning('RDF has no ID: %s' % path)
                break
            (pubdate, mutopia_id) = parse_mutopia_id(footer)

            # Determine if this is an update or a new piece
            piece = None
            status = None
            comp = Composer.objects.get(composer=graph.value(mp_subj, MP.composer))
            try:
                piece = Piece.objects.get(pk=mutopia_id)
                piece.title = graph.value(mp_subj, MP.title)
                piece.composer = comp
                status = 'update'
            except Piece.DoesNotExist:
                piece = Piece(piece_id = mutopia_id,
                              title = graph.value(mp_subj, MP.title),
                              composer = comp)
                status = 'new'

            # fill out the remainder of piece
            piece.style = Style.objects.get(pk=graph.value(mp_subj,MP.style))
            piece.raw_instrument = graph.value(mp_subj, MP['for'])
            piece.license = License.objects.get(name=graph.value(mp_subj, MP.licence))
            # use routines to get maintainer and version because we
            # might have to create them on the fly
            piece.maintainer = Contributor.find_or_create(
                graph.value(mp_subj, MP.maintainer),
                graph.value(mp_subj, MP.maintainerEmail),
                graph.value(mp_subj, MP.maintainerWeb))
            piece.version = LPVersion.find_or_create(
                graph.value(mp_subj, MP.lilypondVersion))
            piece.lyricist = graph.value(mp_subj, MP.lyricist)
            piece.date_composed = graph.value(mp_subj, MP.date)
            piece.date_published = pubdate
            piece.source = graph.value(mp_subj, MP.source)
            piece.moreinfo = graph.value(mp_subj, MP.moreInfo)
            piece.opus = graph.value(mp_subj, MP.opus)
            # Clear the relationships this piece has with instruments
            piece.instruments.clear()
            piece.save()

            # Associate the asset with the piece and mark it published
            asset.piece = piece
            asset.published = True
            asset.save()
            logger.info('  {0}: {1}'.format(status, piece))
            published.append(mutopia_id)

        return published


    def handle(self, *args, **options):
        with transaction.atomic():
            logger.info('Processing new or updated RDF files.')
            self.update_pieces()
            self.update_instruments()
            SearchTerm.refresh_view()
