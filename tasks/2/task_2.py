#!/usr/bin/env python

"""TASK 2 - NERMuD 

This script is designed to convert a series of dataset for extraction and classification of named-entities in a document from https://github.com/dhfbk/KIND/tree/main/evalita-2023 into a QA dataset suitable for training Large Language Models (LLMs)."""

# general imports 
import os
import sys
import shutil
import argparse
# from git import Repo

# online resources
import wget
import zipfile

# data manipulations
import json
import csv
import pandas as pd

# FUNCTIONS

def progress_bar(current, total, width=80):
  """Plain progress bar to monitor download status"""

  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()    


def move_data(data, dest="results"):
  """Just to move the final dtaset in the destination folder and once again avoid pushing large files."""

  os.makedirs(dest, exist_ok=True)
  for d in data:
    shutil.move(d, dest + "/" + data)
    print(f"Data: {d} moved to {dest}")


def make_dataframe(dataset, dtype):
  """This finction read the TSV file while preserving empty lines and return a pandas dataframe"""
  
  header = ["word", "label"]
  with open(dataset, "r", encoding="utf-8") as f:
    df = pd.read_csv(f, sep='\t', header=None, skip_blank_lines=True)
    return df


def to_jsonl(output_jsonl, pandas_df, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset """

  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    json_dict ={
      "sentence_id": int, # an incremental integer (starting from zero)
      "text": str, # the input sentence,
      "target_entity": str, # can be a multi-word
      "choices": list[str],
      "label": int, # the correct answer
    }

    json_str = json.dumps(json_dict, ensure_ascii=False)
    jout.write(json_str + '\n')


# MAIN
if __name__ == '__main__' : 

  # global variables
  dataset_splits = {
    "train": 0,
    "test": 0,
    "dev": 0,
  }
  dataset_types = ["ADG", "FIC", "WN"]
  os.makedirs("./data", exist_ok=True)

  for dtype in dataset_types:
    for dsplit in  dataset_splits.keys():
      dataset = dtype + "_" + dsplit +".tsv"
      if not os.path.exists("./data/" + dataset):
        data_url = "https://github.com/dhfbk/KIND/raw/main/evalita-2023/" + dataset
        wget.download(url=data_url, out="./data/" + dataset, bar=progress_bar)    
        print()
      else:
        print(f"Dataset: {dataset} already present")

  for dtype in dataset_types:
    for dsplit in  dataset_splits.keys():
      dataset = dtype + "_" + dsplit +".tsv"
      df = make_dataframe("./data/" + dataset, dtype)
      print(df.head) 
      break