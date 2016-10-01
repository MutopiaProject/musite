"""This modules is used to customize the django `Admin` panels. Models
registered with the `Admin` can be created and deleted using the web
UI provided by django. This UI can be further manipulated if
necessary.

"""

from django.contrib import admin
from mutopia.models import Style, Composer, Instrument, License
from mutopia.models import Contributor, Piece, Collection

class StyleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("style",)}

# Contributor is built on publication but not used much. Basically, it
# is a re-factored entity and may be useful in the future.
admin.site.register(Contributor)

admin.site.register(Instrument)
admin.site.register(License)
admin.site.register(Style, StyleAdmin)

class ComposerAdmin(admin.ModelAdmin):
    list_display = ('composer', 'description')
admin.site.register(Composer, ComposerAdmin)

"""
    class PieceInline(admin.TabularInline):
        model = Collection.pieces.through

    class PieceAdmin(admin.ModelAdmin):
        inlines = [
            PieceInline,
        ]
"""

#    inlines = [
#        PieceInline,
#    ]
#    exclude = ('pieces',)
#
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('tag', 'title')
    raw_id_fields = ('pieces',)

admin.site.register(Collection, CollectionAdmin)
