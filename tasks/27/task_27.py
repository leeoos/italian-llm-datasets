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


def make_dataframe(data, columns):
    """This function will generate a pandas dataframe after checking (and correcting) the format of the provided csv."""
    
    print(f"Columns: {columns}")
    print(f"Dataset: {data}")

    to_correct = []
    for csv_path in data:
        with open(csv_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if '"' in content:
                to_correct.append(csv_path)

    print(f"Contains bad formatted quotes --> {to_correct}")

    if to_correct:
        for csv_path in to_correct:
          # Apply format correction function here
          for csv_path in to_correct:
            if correct_quotes_in_csv(csv_path):
                print(f"Quotes corrected successfully in {csv_path}")
            else:
                print(f"Failed to correct quotes in {csv_path}")

        if all(check_consistency(csv_path, column_sublist) for csv_path, column_sublist in zip(data, columns)):
            dfs = []
            for csv_path, column_sublist in zip(data, columns):
                df = pd.read_csv(csv_path, usecols=column_sublist)
                dfs.append(df)
            concatenated_df = pd.concat(dfs, ignore_index=True)
            print(concatenated_df.head())
            return concatenated_df
        else:
            print(f"Error: One or more CSV files are badly formatted.")
            return None
    else:
        dfs = []
        for csv_path, column_sublist in zip(data, columns):
            df = pd.read_csv(csv_path, usecols=format_columns(column_sublist))
            dfs.append(df)
        concatenated_df = pd.concat(dfs, ignore_index=True)
        print(concatenated_df.head())
        return concatenated_df

def df_to_jsonl(output_jsonl, pandas_df, TASK=1, DEBUG=False):
  """This is the main function used to generate the desired json dataset in output. This function produce a different output for each given sub-task in [1,2,3]."""
  print(TASK)
  with open(output_jsonl, "w",  encoding="utf-8") as jout:
    DEBUG_COUNTER = 0

    for data in pandas_df.itertuples():
      if hasattr(data, 'anonymized_tweet_id'):
          if DEBUG:
              print(f"data anonymized_tweet_id: {data.anonymized_tweet_id}")
              print(f"data created_at: {getattr(data, 'created_at', None)}")
              print(f"data retweet_count: {getattr(data, 'retweet_count', None)}")
              print(f"data favorite_count: {getattr(data, 'favorite_count', None)}")
              print(f"data source: {getattr(data, 'source', None)}")
              print(f"data is_reply: {getattr(data, 'is_reply', None)}")
              print(f"data is_retweet: {getattr(data, 'is_retweet', None)}")
              print(f"data is_quote: {getattr(data, 'is_quote', None)}")
              print(f"data anonymized_user_id: {getattr(data, 'anonymized_user_id', None)}")
              print(f"data user_created_at: {getattr(data, 'user_created_at', None)}")
              print(f"data statuses_count: {getattr(data, 'statuses_count', None)}")
              print(f"data followers_count: {getattr(data, 'followers_count', None)}")
              print(f"data friends_count: {getattr(data, 'friends_count', None)}")
              print(f"data anonymized_description: {getattr(data, 'anonymized_description', None)}")
              print(f"data dataset: {getattr(data, 'dataset', None)}")
      elif hasattr(data, 'anonymized_text'):
          if DEBUG:
              print(f"data anonymized_tweet_id: {data.anonymized_tweet_id}")
              print(f"data anonymized_text: {data.anonymized_text}")
              print(f"data label: {data.label}")
              print(f"data dataset: {data.dataset}")

      if TASK == 1:
        choices = ["si", "no"]
      
      elif TASK == 2:
        choices = ["politico", "religioso"]
            
      else:
        raise NameError
      
      json_dict = {
          "id":       int(data.anonymized_tweet_id),
          "text":     data.anonymized_text,
          "choices":  choices,
          "label":    int(data.label)
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
    train_data_url = "https://github.com/mirkolai/EVALITA2023-HaSpeeDe3"
    train_data_out = "./data"
    get_dat_from_url(train_data_url, train_data_out)
    #get_data_from_zip(train_data_out)

    # remove macos directory
    try:
      shutil.rmtree("./__MACOSX")
    except FileNotFoundError:
      pass

  # use cached datasel saved in local
  #training_contextual = "./data/development/training_contextual.csv"
  training_textual_dev = "./data/development/training_textual.csv"
  training_textual_gold = "./data/gold/test_textual_gold.csv"

  columns_training_contextual = ['anonymized_tweet_id', 'created_at', 'retweet_count', 'favorite_count', 'source', 'is_reply', 'is_retweet', 'is_quote', 'anonymized_user_id', 'user_created_at', 'statuses_count', 'followers_count', 'friends_count', 'anonymized_description', 'dataset']
  columns_training_textual_dev = ['anonymized_tweet_id', 'anonymized_text', 'label', 'dataset']
  columns_training_textual_gold = ['anonymized_tweet_id', 'anonymized_text', 'label', 'dataset']

  columns = [columns_training_textual_dev]
  columns_training_textual_gold_list = [columns_training_textual_gold]

  csv_files = [training_textual_dev]
  training_textual_gold_list = [training_textual_gold]
  json_path = "./data/TAG-it-train.jsonl"

  train_df = make_dataframe(csv_files, columns)
  sub_task = 1
  train_output_jsonl = "haspeede3-task" + str(sub_task) + "-train-data.jsonl"
  df_to_jsonl(train_output_jsonl, train_df, TASK=sub_task, DEBUG=True)