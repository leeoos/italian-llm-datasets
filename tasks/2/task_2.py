#!/usr/bin/env python

"""TASK 2 - NERMuD 

This script is designed to convert a series of dataset for extraction and classification of named-entities in a document from https://github.com/dhfbk/KIND/tree/main/evalita-2023 into a QA dataset suitable for training Large Language Models (LLMs)."""

# general imports 
import os
import sys
import shutil
# from git import Repo

# online resources
import wget

# data manipulations
import json
import csv
import pandas as pd
import numpy as np

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
    shutil.move(d, dest + "/" + d)
    print(f"Data: {d} moved to {dest}")


def make_dataframe(dataset, dtype):
  """This finction read the TSV file while preserving empty lines and return a pandas dataframe"""
  
  header_names = ["word", "label"]
  with open(dataset, "r", encoding="utf-8") as f:
    try:
      df = pd.read_csv(f, sep='\t', header=None, skip_blank_lines=False, names=header_names, quoting=csv.QUOTE_NONE)
      return df
    except Exception as e:
      print(f"An error occurred: {e}")


def to_jsonl(
    output_jsonl,
    pandas_df, 
    dataset_splits, 
    dsplit,
    DEBUG=False
  ):
  """This is the main function used to generate the desired json dataset. Each samples as an array of choices associated to it:
  B-PER
  B-ORG
  B-LOC
  I-PER
  I-ORG
  I-LOC
  """

  with open(output_jsonl, "a",  encoding="utf-8") as jout:

    previous = {
      "label": np.nan,
      "word": np.nan
    }
    entity = []

    for data in pandas_df.itertuples():

      if DEBUG:
        # print(f"word --> {data.word}")
        # print(f"label --> {type(data.label)}")
        ...

      # check wheter the sentence is changing or not
      if pd.isna(data.word):
        # save previous
        entity_name = " ".join(entity)
        print(entity_name)
        print()
        entity = []
        # break
        # check for new sentence
        ...

      else:

        if (data.label[0] == "B" and previous["label"] in ["B", "I"]) or \
          (data.label[0] == "O"  and previous["label"] == "B"):
          # save previous
          entity_name = " ".join(entity)
          print(entity_name)
          print()
          entity = []
          # go on 
          entity.append(data.word)
        
        elif (data.label[0] == "O"  and previous["label"] == "I"):
          # save previous
          entity_name = " ".join(entity)
          print(entity_name)
          print()
          entity = []

        elif (data.label[0] == "B" and previous["label"] not in ["B", "I"]) or \
            (data.label[0] == "I" and previous["label"] in ["B", "I"]) :
          # go on
          entity.append(data.word)


        else:
          # do nothing
          pass
      
        if data.label[0] in {'B', 'I'}:
          print(data.Index, end=" ")
          print(data.word, end=" ") 
          print(data.label)

      # sentence_id = dataset_splits[dsplit]
      # choices = [
      #   "a"
      # ]
      # json_dict ={
      #   "sentence_id": sentence_id, 
      #   # "text": 
      #   # "target_entity":
      #   # "choices":
      #   # "label": 
      # }

      # json_str = json.dumps(json_dict, ensure_ascii=False)
      # jout.write(json_str + '\n')
      # dataset_splits[dsplit] += 1

      if not pd.isna(data.label) :
        previous["label"] = data.label[0] 
      else:
        previous["label"] = np.nan
      previous["word"] = data.word

      


# MAIN
if __name__ == '__main__' : 

  # global variables
  results_dir = "./results/"
  data_dir = "./data/"
  os.makedirs(data_dir, exist_ok=True)
  dataset_splits = {
    "train": 0,
    "test": 0,
    "dev": 0,
  }
  dataset_types = ["ADG", "FIC", "WN"]
  jsonl_files = set()

  # get datasets
  for dtype in dataset_types:
    for dsplit in  dataset_splits.keys():
      dataset = dtype + "_" + dsplit +".tsv"
      if not os.path.exists(data_dir + dataset):
        data_url = "https://github.com/dhfbk/KIND/raw/main/evalita-2023/" + dataset
        wget.download(url=data_url, out=data_dir+dataset, bar=progress_bar)    
        print()
      else:
        # print(f"Dataset: {dataset} already present")
        ...

  # clear previous results just to be sure
  try:
    shutil.rmtree(results_dir)
  except FileNotFoundError:
    pass

  # make json files
  dataset_types = ["WN"] # JUST FOR DEBUG
  for dtype in dataset_types:
    for dsplit in  dataset_splits.keys():
      dataset = dtype + "_" + dsplit +".tsv"
      output_json = "NERMuD_" + dsplit + ".jsonl"
      print(f"Dataset --> {dataset}")

      df = make_dataframe(data_dir + dataset, dtype)
      print(f"Dataset len: {len(df)}")
      to_jsonl(output_json, df, dataset_splits, dsplit, DEBUG=True)
      jsonl_files.add(output_json)
      print(f"JSONL output --> {output_json}")

      break
    break

  print(jsonl_files)
  # move_data(list(jsonl_files), results_dir)