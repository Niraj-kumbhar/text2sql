import os
import json
from config.settings import TESTING,TEST_OUTPUT_DIR

def return_llm_output():
    file_path = TEST_OUTPUT_DIR/"test_llm_output.json"
    with open(file_path, 'r') as f:
        return json.load(f)