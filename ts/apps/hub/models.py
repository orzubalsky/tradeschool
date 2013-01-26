from django.conf import settings
from django.db.models import *
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from chunks.models import Chunk



# signals are separated to signals.py 
# just for the sake of organization
import signals