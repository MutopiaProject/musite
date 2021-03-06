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

logger = logging.getLogger(__name__)

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
                logger.info('Added %s to %s' % (instr,p.piece_id))


    def finalize_mapping(self, asset, piece, uses_svg):
        """ Check for a folder rename and remove the matching asset
        if found.

        The asset may be in one of two states,
          - it is a new piece and the only existing mapping
          - it is an existing piece that is being updated
          - it is an existing peice whose physical location is being
            changed (a folder rename).

        The first case will result in a is simple save of the given
        asset. The last two will be handled the same way by deleting
        the existing asset, allowing the new one to be saved.

        """
        try:
            old_asset = AssetMap.objects.get(piece=piece)
            if old_asset.folder != asset.folder:
                logging.info('Renaming asset, %s -> %s' % (old_asset,asset))
            old_asset.delete()
        except AssetMap.DoesNotExist:
            pass

        asset.piece = piece
        asset.published = True
        asset.uses_svg = uses_svg
        asset.save()


    def process_pending_pieces(self):
        # Get all assets that are ready to publish
        for asset in AssetMap.objects.all().filter(published=False):
            path = asset.get_rdfspec()
            logger.info('Reading RDF %s' % path)
            try:
                graph = Graph().parse(URIRef(path))
            except (FileNotFoundError, HTTPError):
                logger.info('Asset still pending: %s.' % asset)
                continue

            # Because our RDF's are defined as 'rdf:about:"."' the subject
            # is a URI reference to the containing folder.
            mp_subj = URIRef('/'.join([FTP_URL, asset.folder,]) + '/')

            try:
                footer = graph.value(mp_subj, MP.id)
                (pubdate, mutopia_id) = parse_mutopia_id(footer)
            except ValueError as exc:
                logger.info('%s, continuing.' % exc)
                continue

            # Determine if this is an update or a new piece
            comp = Composer.objects.get(
                composer=graph.value(mp_subj, MP.composer))
            try:
                piece = Piece.objects.get(piece_id=mutopia_id)
                logger.info('Found existing piece to update.')
                piece.title = graph.value(mp_subj, MP.title)
                piece.composer = comp
                if not graph.value(mp_subj, MP['for']).eq(piece.raw_instrument):
                    piece.instruments.clear()
            except Piece.DoesNotExist:
                logger.info('Creating new piece.')
                piece = Piece(piece_id=mutopia_id,
                              title=graph.value(mp_subj, MP.title),
                              composer=comp)

            # Fill out remainder of piece from the RDF.
            piece.style = Style.objects.get(pk=graph.value(mp_subj,MP.style))
            piece.raw_instrument = graph.value(mp_subj, MP['for'])
            piece.license = License.objects.get(
                name=graph.value(mp_subj, MP.licence))
            # Maintainer and Version objects may need to be created
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

            piece.save()
            image_name = str(graph.value(mp_subj, MP.pngFile))
            self.finalize_mapping(asset, piece, image_name.endswith('.svg'))
            logger.info('* Finished piece {0}'.format(piece))


    def handle(self, *args, **options):
        with transaction.atomic():
            logger.info('Processing new or updated RDF files.')
            self.process_pending_pieces()
            self.update_instruments()
            logger.info('Refreshing materialized view for FTS.')
            SearchTerm.refresh_view()
