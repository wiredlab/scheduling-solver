import sys
import os

# Change these values for your environment
# THIS FILE SHOULD NOT BE READABLE BY OTHERS,
# UPDATE THE FILE PERMISSIONS ACCORDINGLY
#
#os.environ['PHOTOROSTER_JPG_CACHE'] = '/var/www/apps/scheduling-solver/cache'

# uncomment to save inputs and temp files

# change to the location of this file
sys.path.append('/var/www/apps/scheduling-solver')

from app import app as application
