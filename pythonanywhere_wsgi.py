import sys
import os

# Add your project directory to the sys.path
project_home = '/home/SumedhAmbhore/TextToSpeechApp'  # Replace with your actual path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the FLASK_ENV environment variable
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application

# Optional: Set up logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("WSGI application loaded successfully")
