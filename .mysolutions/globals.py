import os

openapi_api_key = os.getenv('OPENAPI_API_KEY')
aidevs_api_key = os.getenv('AIDEVS_API_KEY')

import types

models = types.SimpleNamespace()
models.gpt41 = "gpt-4.1"
models.gpt40 = "gpt-4o"
models.gpt04mini = "o4-mini"
