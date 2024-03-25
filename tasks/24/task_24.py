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

# FUNCTIONS

def progress_bar(current, total, width=80):
  """Plain progress bar to monitor download status"""

  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()

def get_dat_from_url(data_url, data_out):
    """A function to download the dataset from given url"""

    wget.download(url=data_url, out=data_out, bar=progress_bar)    
    print()
    with zipfile.ZipFile(data_out, "r") as zip_ref:
      zip_ref.extractall()

def delete_data():
  """A simple function used to remove the original dataset file from the pwd after the script execution. This is done to avoid pushing large files on github."""

  try:
    os.remove("sentipolc_train_data.zip")
    os.remove("training_set_sentipolc16.csv")
    os.remove("sentipolc_test_data.zip")
    os.remove("test_set_sentipolc16_gold2000.csv")

  except OSError:
      pass
  
def move_data(data, dest="results"):
  """Just to move the final dtaset in the destination folder and once again avoid pushing large files."""

  os.makedirs(dest, exist_ok=True)
  shutil.move(data, dest + "/" + data)

def correct(data, FIXED_LEN=9, DEBUG=False) :
  """This function fixes the original csv dataset by removing extra quotes that messed up the standard column delimeters."""

  big_list = []
  with open(data, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    counter = 0
    bad_formatted = 0

    for row in spamreader:
      counter += 1
      if len(row) > FIXED_LEN:
        # removing extra double quotes 
        new_row = [int(i.strip('"')) for i in row[:(FIXED_LEN -1)]]
        new_row.append(''.join(i for i in row[(FIXED_LEN - 1):])[1:-1])
        big_list.append(new_row)

        if DEBUG:
          print(f"before--> {len(row)}", end="-->")
          print(row)
          print(f"after --> {len(new_row)}", end="-->")
          print(new_row)

      else:
        # removing extra double quotes 
        new_row = [int(i.strip('"')) for i in row[:8]]
        new_row.append(row[8][1:-1])
        big_list.append(new_row)

  print(f"Len original data --> {counter}")
  print(f"Bad formatted samples --> {bad_formatted}")
  print(f"Len after manipulation --> {len(big_list)}")  
  return big_list

def check_quotes(data, FIXED_LEN=9):
  """ This function  check the presence of double quote inside the tweets and make sure that those are preserved since they are a meaningful communication device. """
  
  with open(data, newline='') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

      # check for extra quotes only in the text
      for row in spamreader:
        for elem in row[(FIXED_LEN - 1):]:
          val = '”' in elem
          if val:
            print(f"before --> {elem}")
            new_elem = elem.strip('"') 
            print(f"after --> {new_elem}", end="\n\n")


def check_consistency(data, FIXED_LEN=9):
  """This function is used to verify that no samples are discarded after the correction process."""

  error_counter = 0   
  for d in data:
    if len(d) > FIXED_LEN:
      error_counter += 1
      print(f"Bad sample --> {d}")

  print(f"Errors --> {error_counter}")
  return error_counter == 0

def make_jsonl(output_jsonl, pandas_df, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""

  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    DEBUG_COUNTER = 0

    for data in pandas_df.itertuples():
      if DEBUG:
        print(f"data index: {data.Index}")
        print(f"data id: {data.idtwitter}")
        print(f"data subj: {data.subj}")
        print(f"data subj: {data.opos}")
        print(f"data subj: {data.oneg}")
        print(f"data subj: {data.iro}")
        print(f"data subj: {data.lpos}")
        print(f"data subj: {data.lneg}")
        print(f"data subj: {data.top}")
        print(f"data text: {data.text}")

      if TASK == 1:
        choices = ["oggettivo", "soggettivo"]
        label = 0 if data.subj == 0 else 1
      
      elif TASK == 2:
        choices = ["positivo", "negativo", "misto", "neutrale"]
        combos = {
          (1,0): 0,
          (0,1): 1,
          (1,1): 2,
          (0,0): 3
        }
        label = combos[(data.opos, data.oneg)]

      elif TASK == 3:
        choices = ["serio", "ironico"]
        label = 0 if data.iro == 0 else 1
            
      else:
        raise NameError
      
      json_dict = {
        "id": data.idtwitter,
        "text": data.text,
        "choices":  choices,
        "label": label 
      }

      json_str = json.dumps(json_dict)
      jout.write(json_str + '\n')

      DEBUG_COUNTER += 1
      if DEBUG and DEBUG_COUNTER > 1: 
        break

  print(f"Sub-task --> {TASK} \t Data dumped into jsonl --> {DEBUG_COUNTER}/{len(pandas_df)}")

# MAIN

if __name__ == '__main__' : 

  # set up command line args
  parser = argparse.ArgumentParser(description='Dataset Manipulation')
  parser.add_argument('--download', '-d', action='store_true')
  parser.add_argument('--task', '-t', type=int)
  args = parser.parse_args()

  download = True if args.download else False
  sub_task = args.task if args.task else 1

  if download:

    # download train data
    train_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/training_set_sentipolc16.csv.zip"
    train_data_out = "sentipolc_train_data.zip"
    get_dat_from_url(train_data_url, train_data_out)
    train_data = "training_set_sentipolc16.csv"

    # download test data
    test_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/test_set_sentipolc16_gold2000.csv.zip"
    test_data_out = "sentipolc_test_data.zip"
    get_dat_from_url(test_data_url, test_data_out)
    test_data = "test_set_sentipolc16_gold2000.csv"

    # remove macos directory
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
    test_data = root_dir + "/data/24/test_set_sentipolc16_gold2000.csv"

  print(f"Train dataset: {train_data}")
  train_df = pd.read_csv(train_data)

  print(f"Test dataset: {test_data}")
  test_data = correct(test_data, DEBUG=False)

  if check_consistency(test_data):
    columns = list(train_df)
    test_df = pd.DataFrame(test_data, columns=columns)

    # print header just to be on the safe side
    check_quotes(train_data)
    print(train_df.head, end="\n")
    print(test_df.head)
    
  else:
    print("Error: the csv file is bad formatted")
      
  train_output_jsonl = "haspeede3-task" + str(sub_task) + "-train-data.jsonl"
  make_jsonl(train_output_jsonl, train_df, TASK=sub_task, DEBUG=False)
  move_data(train_output_jsonl, "results")

  test_output_jsonl = "haspeede3-task" + str(sub_task) + "-test-data.jsonl"
  make_jsonl(test_output_jsonl, test_df, TASK=sub_task, DEBUG=False)
  move_data(test_output_jsonl, "results")

  # to avoid pushing data on github
  if download:
    delete_data()