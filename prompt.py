#!/usr/bin/env python

"""TASK 24 - SENTIPOLC - PROMPT EVALUATION

This script automatize the evaluation of different prrompts for task 24"""

import os
import json


def load_jsonl(filename):
  with open(filename, 'r', encoding='utf-8') as file:
      return [json.loads(line) for line in file]



# load the data and prompt files
data_entries = load_jsonl('data.jsonl')
prompt_templates = load_jsonl('prompt.jsonl')

for prompt in prompt_templates:
  selected_prompt_template = prompt['prompt']
  print(prompt)

# for each entry in the data file, format the prompt with the data and print it
for entry in data_entries:
  formatted_prompt = selected_prompt_template.replace('{{passage}}', entry['passage']).replace('{{question}}', entry['question'])
  print(formatted_prompt)