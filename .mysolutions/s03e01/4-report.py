
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# from OpenAIService import HttpService
import globals
from OpenAIService import HttpService, read_json, FileLocation

answer_data = read_json(__file__, '3-answer.json')

HttpService.send_report('dokumenty', answer_data)