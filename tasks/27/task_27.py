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

def check_consistency(csv_path, expected_columns):
    """
    Checks if the columns in the CSV file match the expected columns.
    
    Parameters:
        csv_path (str): The path to the CSV file.
        expected_columns (list): The list of expected column names.
        
    Returns:
        bool: True if the columns match, False otherwise.
    """
    try:
        df = pd.read_csv(csv_path, nrows=1)
        actual_columns = df.columns.tolist()
        return actual_columns == expected_columns
    except Exception as e:
        print(f"Error checking consistency for {csv_path}: {str(e)}")
        return False

def format_columns(columns):
    """Formats column names with quotes and commas between every word."""
    formatted_columns = ['"' + '", "'.join(column.split()) + '"' for column in columns]
    return formatted_columns



def correct_quotes_in_csv(csv_path):
    """
    Corrects the badly formatted quotes in the CSV file.
    
    Parameters:
        csv_path (str): The path to the CSV file.
        
    Returns:
        bool: True if quotes are corrected successfully, False otherwise.
    """
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        corrected_content = content.replace('""', '"')
        
        with open(csv_path, 'w', encoding='utf-8') as file:
            file.write(corrected_content)
        
        return True
    except Exception as e:
        print(f"Error correcting quotes in {csv_path}: {str(e)}")
        return False


def make_list(data, columns):
    """This function will generate a pandas dataframe after checking (and correcting) the format of the provided csv."""
    
    print(f"Columns: {columns}")
    print(f"Dataset: {data}")


    for csv_path in data:
        with open(csv_path, 'r', encoding='utf-8') as file:
          whole = file.read()
    whole = whole.split('"training_politics"\n')

    csv = []
    for elem in whole[1:]:
      elem = elem.split('","')
      if elem == ['']:
        continue
      elem[0] = elem[0][1:]
      elem[2] = elem[2][:-2]
      csv.append(elem)
      if len(elem)!=3:
        print("error!", elem)

    return csv

def list_to_jsonl(output_jsonl, csv, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""
  print(TASK)
  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    DEBUG_COUNTER = 0

    for id, text, label in csv:
      if TASK == 1:
        choices = ["si", "no"]
      
      elif TASK == 2:
        choices = ["politico", "religioso"]
            
      else:
        raise NameError
      
      json_dict = {
          "id":       int(id),
          "text":     text,
          "choices":  choices,
          "label":    int(label)
      }

      json_str = json.dumps(json_dict, ensure_ascii=False)
      jout.write(json_str + '\n')

      DEBUG_COUNTER += 1
      # if DEBUG and DEBUG_COUNTER > 10: 
      #   break

  print(f"Sub-task --> {TASK} \t Data dumped into jsonl --> {DEBUG_COUNTER}/{len(csv)}")





# MAIN
if __name__ == '__main__' : 

  # set up command line args

  download = False
 
  if download:

    # download train data
    train_data_url = "https://github.com/mirkolai/EVALITA2023-HaSpeeDe3"
    train_data_out = "./data"
    get_dat_from_url(train_data_url, train_data_out)
    #get_data_from_zip(train_data_out)

    # remove macos directory
    try:
      shutil.rmtree("./__MACOSX")
    except FileNotFoundError:
      pass
  #train_data_out = "./data"
  #unzip(train_data_out)

  # use cached datasel saved in local
  #training_contextual = "./data/development/training_contextual.csv"
  training_textual_dev = "./data/development/training_textual.csv"
  training_textual_gold = "./data/gold/test_textual_gold.csv"

  #columns_training_contextual = ['anonymized_tweet_id', 'created_at', 'retweet_count', 'favorite_count', 'source', 'is_reply', 'is_retweet', 'is_quote', 'anonymized_user_id', 'user_created_at', 'statuses_count', 'followers_count', 'friends_count', 'anonymized_description', 'dataset']
  columns_training_textual_dev = ['"anonymized_tweet_id"', '"anonymized_text"', '"label"', '"dataset"']
  columns_training_textual_gold = ['"anonymized_tweet_id"', '"dataset"', '"label"', '"anonymized_text"']

  columns = [columns_training_textual_dev]
  columns_training_textual_gold_list = [columns_training_textual_gold]

  csv_files = [training_textual_dev]
  training_textual_gold_list = [training_textual_gold]

  json_path = "./data/TAG-it-train.jsonl"

  print(csv_files)
  train_list = make_list(csv_files, columns)
  sub_task = 1
  train_output_jsonl = "haspeede3-task" + str(sub_task) + "-train-data.jsonl"
  list_to_jsonl(train_output_jsonl, train_list, TASK=sub_task, DEBUG=False)