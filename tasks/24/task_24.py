#!/usr/bin/env python

"""TASK 24 - SENTIPOLC 

This script willconvert a sentiment classification dataset taken from http://www.di.unito.it/~tutreeb/sentipolc-evalita16/index.html into a QA dataset siutable for training LLMs"""

# general imports 
import os
import sys
import shutil
from git import Repo

# online resources
import wget
import zipfile

# data manipulations
import json
import csv
import pandas as pd


global download 
download = False

def progress_bar(current, total, width=80):
  progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
  sys.stdout.write("\r" + progress_message)
  sys.stdout.flush()


def delete_data():
  try:
    os.remove("sentipolc_train_data.zip")
    os.remove("training_set_sentipolc16.csv")
    os.remove("sentipolc_test_data.zip")
    os.remove("test_set_sentipolc16_gold2000.csv")
  except OSError:
      pass


if __name__ == '__main__' : 

  if download:

    # download test data
    train_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/training_set_sentipolc16.csv.zip"
    train_data_out = "sentipolc_train_data.zip"
    wget.download(url=train_data_url, out=train_data_out, bar=progress_bar)    
    print() 
    shutil.rmtree("./__MACOSX")
    with zipfile.ZipFile(train_data_out, "r") as zip_ref:
      zip_ref.extractall()
    train_data = "training_set_sentipolc16.csv"

    # download train data
    test_data_url = "http://www.di.unito.it/~tutreeb/sentipolc-evalita16/test_set_sentipolc16_gold2000.csv.zip"
    test_data_out = "sentipolc_test_data.zip"
    wget.download(url=test_data_url, out=test_data_out, bar=progress_bar) 
    print() 
    shutil.rmtree("./__MACOSX")
    with zipfile.ZipFile(test_data_out, "r") as zip_ref:
      zip_ref.extractall()
    test_data = "test_set_sentipolc16_gold2000.csv"

  else:

    # get the root directory of the Git project
    repo = Repo(".", search_parent_directories=True)
    root_dir = repo.git.rev_parse("--show-toplevel")

    # use cached datasel saved in local
    train_data = root_dir + "/data/24/training_set_sentipolc16.csv"
    test_data = root_dir + "./data/24/test_set_sentipolc16_gold2000.csv"

  print(train_data)
  print(test_data)
  # with open('file.csv', 'r') as file:
  #     reader = csv.reader(file)
  #     for row in reader:
  #         print(row)

  # to free up memory and avoid pushing data on github
  if download:
    delete_data()