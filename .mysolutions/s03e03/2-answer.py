x = """
        {
            "dc_id": "4278"
        },
        {
            "dc_id": "9294"
        }
"""

import os
from pathlib import Path
import sys
from uuid import uuid4

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from globals import aidevs_api_key
from OpenAIService import OpenAiService, HttpService
from VectorClient import VectorClient

HttpService.send_report('database', [4278, 9294])