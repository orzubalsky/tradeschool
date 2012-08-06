from django.db.models import *
from tradeschool.models import Base, Branch


class Page(Base):
    """
    Each branch has dynamic content pages.
    """
            
    branch      = ForeignKey(Branch)
    title       = CharField(max_length=100)
    slug        = SlugField(max_length=120)
    content     = TextField()
            
                
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