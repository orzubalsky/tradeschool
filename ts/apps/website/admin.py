from website.models import *
from django.contrib import admin
from chunks.models import Chunk
from tradeschool.admin import BaseAdmin

class SiteChunkAdmin(BaseAdmin):
    """ 
        
    """     
    pass

admin.site.register(Photo)
admin.site.register(SiteChunk, SiteChunkAdmin)