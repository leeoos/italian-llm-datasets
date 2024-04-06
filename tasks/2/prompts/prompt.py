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
    print(json_obj["sentence_id"])
    print(json_obj["text"])
    print(json_obj["target_entity"])
    print(json_obj["choices"])
    print(json_obj["label"])

def make_prompt(data_entries, selected_prompt_template, index):
    entry = data_entries[index]
    print("ID:" + str(entry["sentence_id"]))
    formatted_prompt = selected_prompt_template.replace('{{text}}', entry['text']).replace('{{target_entity}}', entry['target_entity'])
    print(formatted_prompt)
    print("ANSWER: " + entry["choices"][entry["label"]] + "\n")
  
parser = argparse.ArgumentParser(description='Dataset Manipulation')
parser.add_argument('--task', '-t', type=int)
args = parser.parse_args()
TASK = args.task


# dev_data_entries = load_jsonl("test.jsonl")

# dev_data_entries = load_jsonl("../results/NERMuD_WN_dev.jsonl")

if TASK == 1:
  train_data = "../results/NERMuD_ADG_train.jsonl"
  test_data = "../results/NERMuD_ADG_test.jsonl"
  dev_data = "../results/NERMuD_ADG_dev.jsonl"
  prompts = "NERMuD_ADG_prompt.jsonl"

elif TASK == 2:
  train_data = "../results/NERMuD_FIC_train.jsonl"
  test_data = "../results/NERMuD_FIC_test.jsonl"
  dev_data = "../results/NERMuD_FIC_dev.jsonl"
  prompts = "NERMuD_FIC_prompt.jsonl"

elif TASK == 3:
  train_data = "../results/NERMuD_WN_train.jsonl"
  test_data = "../results/NERMuD_WN_test.jsonl"
  dev_data = "../results/NERMuD_WN_dev.jsonl"
  prompts = "NERMuD_WN_prompt.jsonl"

else:
  print(f"Error: no task {TASK}")
  exit(1)

# load the data and prompt files
train_data_entries = load_jsonl(train_data)
test_data_entries = load_jsonl(test_data)
dev_data_entries = load_jsonl(dev_data)
prompt_templates = load_jsonl(prompts)

# check_data(train_data_entries)
# check_data(test_data_entries)
# check_data(dev_data_entries)

num_samples = 1

random_train_sampels = [random.randint(0, len(train_data_entries)) for i in range(num_samples)]
random_test_sampels = [random.randint(0, len(test_data_entries))for i in range(num_samples)]
random_dev_sampels = [random.randint(0, len(dev_data_entries))for i in range(num_samples)]

for prompt in prompt_templates:
  selected_prompt_template = prompt['prompt']
  print("\n" + "-"*100 + "\n")
  print(f"Template: {prompt['prompt']}")
  print()

  for train_i, test_i, dev_i in zip(random_train_sampels, random_test_sampels, random_dev_sampels):
    print("Train data ", end="")
    make_prompt(train_data_entries, selected_prompt_template, train_i)
    print("Test data ", end="")
    make_prompt(test_data_entries, selected_prompt_template, test_i)
    print("Dev data ", end="")
    make_prompt(dev_data_entries, selected_prompt_template, dev_i)
