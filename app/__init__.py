import os
import sys
from dotenv import load_dotenv

load_dotenv('../.flaskenv')
sys.path.append(os.getenv('PYTHONPATH'))