#!/usr/bin/env python

"""TASK 24 - SENTIPOLC - PROMPT EVALUATION

This script automatize the evaluation of different prompts for task 12"""

import json

def load_jsonl(filename):
  with open(filename, 'r', encoding='utf-8') as file:
      return [json.loads(line) for line in file]



# load the data and prompt files
data_entries = load_jsonl('../TAG-it-train.jsonl')
prompt_templates = load_jsonl('./prompt.jsonl')

for prompt in prompt_templates:
  selected_prompt_template = prompt['prompt']
  print(prompt)

# for each entry in the data file, format the prompt with the data and print it
for entry in data_entries:
  formatted_prompt = selected_prompt_template.replace('{{post1}}', entry['post1']).replace('{{post2}}', entry['post2']).replace('{{post3}}', entry['post3']).replace('{{post4}}', entry['post4']).replace('{{post5}}', entry['post5'])
  choices = ""
  for choice in entry['choices']:
    choices += choice+", "
  formatted_prompt = formatted_prompt.replace('{{choices}}', choices) 
  print(formatted_prompt)
