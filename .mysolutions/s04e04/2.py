import json
import os
import sys
from pathlib import Path
import re
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key, models
from OpenAIService import OpenAiService, HttpService
import requests

url = 'https://77895e163c2c.ngrok-free.app/find-drone-location'

HttpService.send_report('webhook', url)