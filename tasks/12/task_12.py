#!/usr/bin/env python

"""TASK 12 - TAG-it 

This script willconvert a sentiment classification dataset taken from https://sites.google.com/view/tag-it-2020/task into a QA dataset siutable for training LLMs"""

# general imports 
import os
import sys
import shutil
import argparse

# online resources
import wget
import zipfile

# data manipulations
import json
import jsonlines

# FUNCTIONS

def progress_bar(current, total, width=80):
  """Plain progress bar to monitor download status"""

  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()


def get_dat_from_url(data_url, data_out):
    """A function to download the dataset from given url"""
    os.makedirs("./data", exist_ok = True)
    wget.download(url=data_url, out=data_out, bar=progress_bar)    
    print()
    with zipfile.ZipFile(data_out, "r") as zip_ref:
      zip_ref.extractall()

def get_data_from_zip(data_out):

    with zipfile.ZipFile(data_out, "r") as zip_ref:
      zip_ref.extractall()

def move_data(data, dest="results"):
  """Just to move the final dtaset in the destination folder and once again avoid pushing large files."""

  os.makedirs(dest, exist_ok=True)
  shutil.move(data, dest + "/" + data)
  print(f"Data: {data} moved to {dest}")

def txt_to_jsonl(output_jsonl, pandas_df, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""

  # create dict topic:posts the for each topic create sample 

  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    DEBUG_COUNTER = 0

    topics = ["generico", "politico", "socio politico"]

    for data in pandas_df.itertuples():
      if DEBUG:
        print(f"data index: {data.Index}")
        print(f"data idtwitter: {data.idtwitter}")
        print(f"data subj: {data.subj}")
        print(f"data opos: {data.opos}")
        print(f"data oneg: {data.oneg}")
        print(f"data iro: {data.iro}")
        print(f"data lpos: {data.lpos}")
        print(f"data lneg: {data.lneg}")
        print(f"data top: {data.top}")
        if "\\\\\\" in data.text:
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
        "topic": topics[data.top],
        "choices":  choices,
        "label": label 
      }

      json_str = json.dumps(json_dict, ensure_ascii=False)
      jout.write(json_str + '\n')

      DEBUG_COUNTER += 1
      # if DEBUG and DEBUG_COUNTER > 10: 
      #   break

  print(f"Sub-task --> {TASK} \t Data dumped into jsonl --> {DEBUG_COUNTER}/{len(pandas_df)}")



# MAIN
if __name__ == '__main__' : 

  # set up command line args

  download = True
 
  if download:

    # download train data
    train_data_url = "https://s3.cbk.cloud.syseleven.net/elg-datasets/23ea2522f1ff4198a7848ef1867a2807/14633443ac104f05ad2f86d44e3d196a/final_package_train_test.zip?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=371f3c77a96342b4b179abb16728fd60%2F20240327%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240327T151534Z&X-Amz-Expires=10&X-Amz-SignedHeaders=host&X-Amz-Signature=46b996d4d42b0fc763f88d4e615dc754e2ca41f47d8424d33a8499670b4f1593"
    train_data_out = "./data/final_package_train_test.zip"
    #get_dat_from_url(train_data_url, train_data_out)
    get_data_from_zip(train_data_out)

    # remove macos directory
    try:
      shutil.rmtree("./__MACOSX")
    except FileNotFoundError:
      pass

  # use cached datasel saved in local
  test1_data = "./final_package_train_test/12/test_task1.txt"
  test2a_data = "./final_package_train_test/12/test_task2a.txt"
  test2b_data = "./final_package_train_test/12/test_task2b.txt"
  train_data = "./final_package_train_test/12/train.txt"

  txt_to_jsonl(test1_data, train_data, TASK=1, DEBUG=False) # put json in data
