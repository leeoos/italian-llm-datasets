#!/usr/bin/env python

"""TASK 24 - SENTIPOLC - PROMPT EVALUATION

This script automatize the evaluation of different prompts for task 24."""

import os
import json
import random

# read json file
def load_jsonl(filename):
  with open(filename, 'r', encoding='utf-8') as file:
      return [json.loads(line) for line in file]

def check_data(data):
  for json_obj in data:
    print(json_obj["id"])
    print(json_obj["text"])
    print(json_obj["topic"])
    print(json_obj["choices"])
    print(json_obj["label"])

data = "../results/sentipolc16-task1-train-data.jsonl"
# data = "./results/sentipolc16-task1-test-data.jsonl"
prompts = "sentipolc16-task1-prompt.jsonl"

# data = "./results/sentipolc16-task2-train-data.jsonl"
# data = "./results/sentipolc16-task2-test-data.jsonl"
# prompts = "sentipolc16-task2-prompt.jsonl"

# data = "./results/sentipolc16-task3-train-data.jsonl"
# data = "./results/sentipolc16-task3-test-data.jsonl"
# prompts = "sentipolc16-task3-prompt.jsonl"

# load the data and prompt files
data_entries = load_jsonl(data)
prompt_templates = load_jsonl(prompts)

check_data(data_entries)

# for prompt in prompt_templates:
#   selected_prompt_template = prompt['prompt']
#   print("\n" + "-"*100 + "\n")
#   print(prompt)
#   print()

#   for i in range(6):
#     rand_index = random.randint(0, len(data_entries))
#     entry = data_entries[rand_index]
#     print(entry)

     
     

# # for each entry in the data file, format the prompt with the data and print it
# for entry in data_entries:
#   formatted_prompt = selected_prompt_template.replace('{{text}}', entry['text']).replace('{{topic}}', entry['topic'])
#   print(formatted_prompt)