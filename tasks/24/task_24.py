#!/usr/bin/env python

"""TASK 24 - SENTIPOLC 

This script willconvert a sentiment classification dataset taken from http://www.di.unito.it/~tutreeb/sentipolc-evalita16/index.html into a QA dataset siutable for training LLMs"""

# general imports 
import os
import sys
import shutil
import argparse
from git import Repo

# online resources
import wget
import zipfile

# data manipulations
import json
import csv
import jsonlines
import pandas as pd



def progress_bar(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

def get_dat_from_url(data_url, data_out):
    wget.download(url=data_url, out=data_out, bar=progress_bar)    
    print()
    with zipfile.ZipFile(data_out, "r") as zip_ref:
      zip_ref.extractall()

def delete_data():
  try:
    os.remove("sentipolc_train_data.zip")
    os.remove("training_set_sentipolc16.csv")
    os.remove("sentipolc_test_data.zip")
    os.remove("test_set_sentipolc16_gold2000.csv")
  except OSError:
      pass


if __name__ == '__main__' : 

  parser = argparse.ArgumentParser(description='Run training and evaluation')
  parser.add_argument('--download', '-d', action='store_true')
  args = parser.parse_args()

  global download 
  download = True if args.download else False

  if download:

    # download test data
    train_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/training_set_sentipolc16.csv.zip"
    train_data_out = "sentipolc_train_data.zip"
    get_dat_from_url(train_data_url, train_data_out)
    train_data = "training_set_sentipolc16.csv"

    # download train data
    test_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/test_set_sentipolc16_gold2000.csv.zip"
    test_data_out = "sentipolc_test_data.zip"
    get_dat_from_url(test_data_url, test_data_out)
    test_data = "test_set_sentipolc16_gold2000.csv"

    try:
      shutil.rmtree("./__MACOSX")
    except FileNotFoundError:
      pass

  else:

    # get the root directory of the Git project
    repo = Repo(".", search_parent_directories=True)
    root_dir = repo.git.rev_parse("--show-toplevel")

    # use cached datasel saved in local
    train_data = root_dir + "/data/24/training_set_sentipolc16.csv"
    test_data = root_dir + "./data/24/test_set_sentipolc16_gold2000.csv"

  print(f"train dataset: {train_data}")
  print(f"test dataset: {test_data}")

  train_df = pd.read_csv(train_data)
  print(train_df.head)
  # print(type(train_df))

  # Task 1

  # output files 
  output_jsonl = "haspeede3-task1-train-data.jsonl"

  DEBUG = False
  with open(output_jsonl, "w",  encoding="utf-8") as jout:

    DEBUG_COUNTER = 0
    for data in train_df.itertuples():

      if DEBUG:
        print(f"data index: {data.Index}")
        print(f"data id: {data.idtwitter}")
        print(f"data text: {data.text}")
        print(f"data subj: {data.subj}")

      label = 0 if data.subj == 0 else 1

      json_dict = {
        "id": data.idtwitter,
        "text": data.text,
        "choices":  ["objective", "subjective"],
        "label": label # Make sure 'label' exists in your DataFrame
      }

      json_str = json.dumps(json_dict)
      jout.write(json_str + '\n')

      DEBUG_COUNTER += 1
      if DEBUG and DEBUG_COUNTER > 1: 
        break

  print(f"Total data from {train_data} dumpet into jsonl: {DEBUG_COUNTER}")

  # to free up memory and avoid pushing data on github
  if download:
    delete_data()