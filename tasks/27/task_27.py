#!/usr/bin/env python

"""TASK 27 - HaSpeeDe 3

This script will convert a sentiment classification dataset taken from http://www.di.unito.it/~tutreeb/haspeede-evalita23/data.html into a QA dataset siutable for training LLMs"""

# general imports 
import os
import shutil

# online resources
from git import Repo
import zipfile

# data manipulations
import json
import pandas as pd


# FUNCTIONS

def get_dat_from_url(data_url, data_out):
    """A function to download the dataset from given url"""
    if not( os.path.exists("./data") ):
      os.makedirs("./data", exist_ok = True)
      Repo.clone_from(data_url, data_out)
    # Iterate over each file in the directory
    for dir in os.listdir(data_out):
      dirpath = os.path.join(data_out, dir)
      if os.path.isdir(dirpath):
        for filename in os.listdir(dirpath):
          filepath = os.path.join(dirpath, filename)
          # Check if the file is a zip file
          if "zip" in filename and not os.path.exists(filepath[:-4]+".csv"):
              print(filepath)
              # Open the zip file
              with zipfile.ZipFile(filepath, 'r') as zip_ref:
                  # Extract or process filepath within the zip file
                  psw = "hS8KxCVQkaM2XhN"
                  zip_ref.extractall(path=dirpath, pwd=psw.encode())

def unzip(data_out):
  for dir in os.listdir(data_out):
    dirpath = os.path.join(data_out, dir)
    print(dirpath)
    if os.path.isdir(dirpath):
      for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        # Check if the file is a zip file
        if "zip" in filename and not os.path.exists(filepath[:-4]+".csv"):
            print(filepath)
            # Open the zip file
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                # Extract or process filepath within the zip file
                psw = "hS8KxCVQkaM2XhN"
                zip_ref.extractall(path=dirpath, pwd=psw.encode())
  print("Unzip!")

def make_list(filepaths):
  """This function will generate a list after checking (and correcting) the format of the provided csv."""

  data = {}
  for data_path in filepaths:
      with open(data_path, 'r', encoding='utf-8') as file:
        whole = file.read()
      if "contextual" in data_path:
        if "training" in filepaths[0] or "training" in filepaths[1]:
          whole = whole.split('"training_politics"\n')
        if "test" in filepaths[0] or "test" in filepaths[1]:
          whole = whole.split('"test_politics"\n')
          whole1 = []
          count = 0
          for line in whole:
             count += len(line.split('"test_religious"\n'))
             whole1.extend(line.split('"test_religious"\n'))
          whole = whole1
        for elem in whole[1:]:
          elem = elem.split('","')
          if elem == [''] or elem[1] == ',':
            continue
          elem[0] = elem[0][1:]
          elem[-1] = elem[-1][:-2]
          #print(elem[0])
          if elem[0] not in data:
            data[elem[0]] = {}
          data[elem[0]]["created_at"] = elem[1]
          data[elem[0]]["retweet_count"] = elem[2]
          data[elem[0]]["favorite_count"] = elem[3]
          data[elem[0]]["is_reply"] = elem[5]
          data[elem[0]]["is_retweet"] = elem[6]
          data[elem[0]]["is_quote"] = elem[7]
          data[elem[0]]["user_created_at"] = elem[9]
          data[elem[0]]["statuses_count"] = elem[10]
          data[elem[0]]["followers_count"] = elem[11]
          data[elem[0]]["friends_count"] = elem[12]
             
      else:
        if "training" in filepaths[0] or "training" in filepaths[1]:
          whole = whole.split('"training_politics"\n')
        if "test" in filepaths[0] or "test" in filepaths[1]:
          whole = whole.split('"test_politics"\n')
          whole1 = []
          count = 0
          for line in whole:
             count += len(line.split('"test_religious"\n'))
             whole1.extend(line.split('"test_religious"\n'))
          whole = whole1
        first = whole[0].split('","')
        id = first[3][10:]
        text = first[4]
        label = first[5][:-2]
        if id not in data:
          data[id] = {}
        data[id]["text"] = text
        data[id]["label"] = label
        for elem in whole[1:]:
          elem = elem.split('","')
          if elem == ['']:
            continue
          elem[0] = elem[0][1:]
          elem[2] = elem[2][:-2]
          if elem[0] not in data:
            data[elem[0]] = {}
          data[elem[0]]["text"] = elem[1]
          data[elem[0]]["label"] = elem[2]
  #print(data[195027074607893])
  return data

def dict_to_jsonl(output_jsonl, data, TASK, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2]."""
  print("task: ",TASK)
  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    DEBUG_COUNTER = 0

    for id, values in data.items():
      choices = ["si", "no"]
      if TASK == 1:
        #print(id)
        json_dict = {
          "id":       int(id),
          "text":     values["text"],
          "choices":  choices,
          "label":    int(values["label"])
        }
      elif TASK == 2:
        if 'created_at' in values.keys():
          #print(id)
          json_dict = {
            "id":       int(id),
            "text":     values["text"],
            "choices":  choices,
            "label":    int(values["label"]),
            "created_at": values['created_at'], 
            "retweet_count": values["retweet_count"],
            "favorite_count": values["favorite_count"],
            "is_reply": values["is_reply"],
            "is_retweet": values["is_retweet"],
            "is_quote": values["is_quote"],
            "user_created_at": values["user_created_at"],
            "statuses_count": values["statuses_count"],
            "followers_count": values["followers_count"],
            "friends_count": values["friends_count"]
          }
        else: 
          json_dict = {
          "id":       int(id),
          "text":     values["text"],
          "choices":  choices,
          "label":    int(values["label"])
        }
      else:
        raise NameError

      json_str = json.dumps(json_dict, ensure_ascii=False)
      jout.write(json_str + '\n')

      DEBUG_COUNTER += 1

  print(f"Sub-task --> {TASK} \t Data dumped into jsonl --> {DEBUG_COUNTER}/{len(data)}")

# MAIN
if __name__ == '__main__' : 

  download = False
 
  if download:

    # download train data
    train_data_url = "https://github.com/mirkolai/EVALITA2023-HaSpeeDe3"
    train_data_out = "./data"
    get_dat_from_url(train_data_url, train_data_out)
    #unzip(train_data_out)

  contextual_dev = "./data/development/training_contextual.csv"
  textual_dev = "./data/development/training_textual.csv"

  contextual_test = "./data/test/test_contextual.csv"
  textual_gold = "./data/gold/test_textual_gold.csv"


  dev_list = [textual_dev, contextual_dev]
  gold_list = [textual_gold, contextual_test]

  sub_task = 1
  output_jsonl = "haspeede3-task" + str(sub_task) + "-test-data.jsonl"
  data_list = make_list(gold_list)
  dict_to_jsonl(output_jsonl, data_list, sub_task, DEBUG=False)