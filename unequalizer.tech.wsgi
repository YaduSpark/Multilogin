#!/usr/bin/python3
import logging
import sys 
import os
os.environ["DB"] = 'unequalizer'
os.environ["DB_USER"] = 'unequalizer'
os.environ["DB_PASSWORD"] = 'U7%akuLzX5yt'
os.environ["PROD_ROOT"] = '/var/www/unequalizer/public_html'
os.environ["MEDIA_PATH"] = os.environ["PROD_ROOT"] + '/media'
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/unequalizer/public_html')
from main import app as application
