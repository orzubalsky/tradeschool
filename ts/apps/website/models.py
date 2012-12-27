from django.db.models import *
from tradeschool.models import Base, Branch
from chunks.models import Chunk

class Photo(Base):
    """
    Each branch has photos that can go in a gallery
    """
    def photo_filename (self, filename):
        # branch image files are stored in the branch's id directory
       if not self.id:
           raise Error('branch image folder does not exist')
       return 'branches/%i/photos/%s' % (self.id,filename)

    branch      = ForeignKey(Branch)
    filename    = ImageField("Photo",upload_to=photo_filename)    
    
    
class SiteChunk(Chunk):
    class Meta:
        proxy = True
        verbose_name = "Site Content Block"