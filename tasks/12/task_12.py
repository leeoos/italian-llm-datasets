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
import re

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

def create_list_of_lists(strings_list, sublist_length=5):
    list_of_lists = []
    for i in range(0, len(strings_list), sublist_length):
        sublist = strings_list[i:i + sublist_length]
        list_of_lists.append(sublist)
    return list_of_lists



def txt_to_jsonl(output_jsonl, txt_file_paths, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""

  # create dict topic:posts the for each topic create sample

  start_user_flag = "<user"
  end_user_flag = "</user"
  start_post_flag = "<post"
  end_post_flag = "</post"

  topic_post = {}

  # Define a regular expression pattern to match the topic attribute
  pattern = r'topic="([^"]+)"'


  for txt_file_path in txt_file_paths:
    with open(txt_file_path) as txt_file:
      for line in txt_file:
        if start_user_flag in line:
          # Use re.search to find the first occurrence of the pattern
          match = re.search(pattern, line)
          topic = match.group(1)
          topic_post[topic] = []
        elif start_post_flag in line or end_post_flag in line or end_user_flag in line:
          continue
        elif line == "\n":
          continue
        else:
          topic_post[topic].append(line)


  with open(output_jsonl, "w",  encoding="utf-8") as jout:

    topics = list(topic_post.keys())
    print(topics)

    for topic, posts in topic_post.items():


      if DEBUG:
        
        print(topic, posts)



      else:
        choices = [topic, topics[0], topics[1]]
        label = 0

        posts_list = create_list_of_lists(posts, 5)
        for list_post in posts_list:
          json_dict = {}

          for i, sublist in enumerate(list_post):
              key = f"post{i+1}"
              if i < 5:
                  json_dict[key] = sublist
              else:
                  json_dict[key] = ""
          json_dict["choices"] = choices
          json_dict["label"] = label

          json_str = json.dumps(json_dict, ensure_ascii=False)
          jout.write(json_str + '\n')




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
  test1_data = "./final_package_train_test/test_task1.txt"
  test2a_data = "./final_package_train_test/test_task2a.txt"
  test2b_data = "./final_package_train_test/test_task2b.txt"
  train_data = "./final_package_train_test/training.txt"

  txt_files = [test1_data, test2a_data, test2b_data, train_data]

  json_path = "./data/TAG-it-train.jsonl"

  txt_to_jsonl(json_path, txt_files, DEBUG=False) # put json in data
