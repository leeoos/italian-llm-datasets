#!/usr/bin/env python

"""TASK 12 - TAG-it 

This script willconvert a sentiment classification dataset taken from https://sites.google.com/view/tag-it-2020/task into a QA dataset siutable for training LLMs"""

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
  print(f"Data: {data} moved to {dest}")


def check_quotes(data, FIXED_LEN=9, DEBUG=False):
  """ This function  check the presence of bad formatted double quotes inside the tweets """
  
  with open(data, newline='', encoding="utf-8") as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
      counter = 0

      # if a row contains more than the fixed number of columns 
      # then it means the quotes are bad fomatted
      for row in spamreader:
        if len(row) > FIXED_LEN:
          return True
      return False


def format(data, FIXED_LEN=9, DEBUG=False) :
  """This function fixes the original csv dataset by removing extra quotes that messed up the standard column delimeters."""

  big_list = []
  with open(data, newline='', encoding="utf-8") as csvfile:
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
          if "\\\\\\" in row:
              print(row)
              print(new_row)

      else:
        # removing extra double quotes 
        new_row = [int(i.strip('"')) for i in row[:8]]
        new_row.append(row[8][1:-1])
        big_list.append(new_row)
        if DEBUG and "\\\\\\" in row:
          print(row)

  print(f"Len original data --> {counter}")
  print(f"Bad formatted samples --> {bad_formatted}")
  print(f"Len after manipulation --> {len(big_list)}")  
  return big_list


def check_consistency(data, FIXED_LEN=9):
  """This function is used to verify that for all the rows the number of columns is consistent."""

  for d in data:
    if len(d) > FIXED_LEN:
      print(f"First Bad sample --> {d}")
      return False
  return True


def make_dataframe(data):
  """This function will generate a pandas dataframe after checking (and correcting) the format of the provided csv."""

  columns=['idtwitter', 'subj', 'opos', 'oneg', 'iro', 'lpos', 'lneg', 'top', 'text']

  print(f"Dataset: {data}")
  to_correct = check_quotes(data, DEBUG=False)
  print(f"Contains bad formatted quotes --> {to_correct}") 
  if to_correct:
    data = format(data, DEBUG=False)
    if check_consistency(data):
      df = pd.DataFrame(data, columns=columns)
      print(df.head, end="\n")
      return df
  
    else:
      print(f"Error: the csv file {test_data} is bad formatted")
      return 1
  
  else:
    df = pd.read_csv(data)
    print(df.head, end="\n")
    return df


def df_to_jsonl(output_jsonl, pandas_df, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""

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
  parser = argparse.ArgumentParser(description='Dataset Manipulation')
  parser.add_argument('--download', '-d', action='store_true')
  parser.add_argument('--task', '-t', type=int)
  args = parser.parse_args()

  download = True if args.download else False
  sub_task = args.task if args.task else 1

  if download:

    # download train data
    train_data_url = "https://live.european-language-grid.eu/catalogue/corpus/8112/download/"
    train_data_out = "final_package_train_test.zip"
    get_dat_from_url(train_data_url, train_data_out)

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
    test1_data = root_dir + "/data/12/test_task1.txt"
    test2a_data = root_dir + "/data/12/test_task2a.txt"
    test2b_data = root_dir + "/data/12/test_task2b.txt"
    test_data = root_dir + "/data/12/train.txt"
    
  train_df = make_dataframe(train_data)
  train_output_jsonl = "haspeede3-task" + str(sub_task) + "-train-data.jsonl"
  df_to_jsonl(train_output_jsonl, train_df, TASK=sub_task, DEBUG=False)
  move_data(train_output_jsonl, "results")

  print("\n" + "-"*80 + "\n")

  test_df = make_dataframe(test_data)
  test_output_jsonl = "haspeede3-task" + str(sub_task) + "-test-data.jsonl"
  df_to_jsonl(test_output_jsonl, test_df, TASK=sub_task, DEBUG=False)
  move_data(test_output_jsonl, "results")

  # to avoid pushing data on github
  if download:
    delete_data()