#!/usr/bin/env python

"""TASK 24 - SENTIPOLC - PROMPT EVALUATION

This script automatize the evaluation of different prompts for task 24."""

import os
import json
import random
import argparse

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

def make_prompt(data_entries, selected_prompt_template, index):
    entry = data_entries[index]
    print("ID:" + str(entry["id"]))
    formatted_prompt = selected_prompt_template.replace('{{text}}', entry['text']).replace('{{topic}}', entry['topic'])
    print(formatted_prompt)
    print("ANSWER: " + entry["choices"][entry["label"]])
  
parser = argparse.ArgumentParser(description='Dataset Manipulation')
parser.add_argument('--task', '-t', type=int)
args = parser.parse_args()
TASK = args.task

if TASK == 1:
  train_data = "../results/sentipolc16-task1-train-data.jsonl"
  test_data = "../results/sentipolc16-task1-test-data.jsonl"
  prompts = "sentipolc16-task1-prompt.jsonl"

elif TASK == 2:
  train_data = "../results/sentipolc16-task2-train-data.jsonl"
  test_data = "../results/sentipolc16-task2-test-data.jsonl"
  prompts = "sentipolc16-task2-prompt.jsonl"

elif TASK == 3:
  train_data = "../results/sentipolc16-task3-train-data.jsonl"
  test_data = "../results/sentipolc16-task3-test-data.jsonl"
  prompts = "sentipolc16-task3-prompt.jsonl"

else:
  print(f"Error: no task {TASK}")
  exit(1)

# load the data and prompt files
train_data_entries = load_jsonl(train_data)
test_data_entries = load_jsonl(test_data)
prompt_templates = load_jsonl(prompts)

# check_data(data_entries)

random_train_sampels = [random.randint(0, len(train_data_entries)) for i in range(1) ]
random_test_sampels = [random.randint(0, len(test_data_entries))for i in range(1) ]

for prompt in prompt_templates:
  selected_prompt_template = prompt['prompt']
  print("\n" + "-"*100 + "\n")
  print(f"Template: {prompt['prompt']}")
  print()

  for train_i, test_i in zip(random_train_sampels, random_test_sampels):
    print("Train data ", end="")
    make_prompt(train_data_entries, selected_prompt_template, train_i)
    print("Test data ", end="")
    make_prompt(test_data_entries, selected_prompt_template, test_i)
