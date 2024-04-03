#!/usr/bin/env python

"""TASK 2 - NERMuD 

This script is designed to convert a series of dataset for extraction and classification of named-entities in a document from https://github.com/dhfbk/KIND/tree/main/evalita-2023 into a QA dataset suitable for training Large Language Models (LLMs)."""

# general imports 
import os
import sys
import shutil
import argparse
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


def join_strings_smartly(words):
    """ Joins a list of words smartly:
    - Adds spaces between words when appropriate.
    - Avoids adding spaces before punctuation.
    """
    punctuation = {'.', ',', ';', ':', '!', '?'}
    result = words[0]
    prev = result

    for word in words[1:]:
      if word in punctuation or \
        "'" in prev or \
        word.startswith("'") or \
        ("." in prev and "." in word) :
        # add word without space
        result += word
      else:
        # add with space
        result += " " + word
      # keep track of previous word  
      prev = word

    return result


def make_json(output_jsonl, sentence_id, sentence_text, entities, DEBUG=False):
  """This function is used to generate a desired json object. Each samples as an array of choices associated to it:
  PER --> person
  ORG --> organization
  LOC --> location
  """

  choices = ["persona", "organizzazione", "luogo"]
  with open(output_jsonl, "a",  encoding="utf-8") as jout:
    for ent in entities:
      entity_name = ent[0]
      label = ent[1]

      json_dict ={
        "sentence_id": sentence_id, 
        "text": sentence_text,
        "target_entity": entity_name,
        "choices": choices,
        "label": label
      }

      json_str = json.dumps(json_dict, ensure_ascii=False)
      jout.write(json_str + '\n')
  

def update_entity(entities, entity, label, DEBUG=False):
  entity_name = join_strings_smartly(entity)
  entities.append((entity_name, label))
  if DEBUG:
    print(f"named entity: {entity_name} --> {label}")
  return []


def add_to_json(output_jsonl, pandas_df, dataset_splits, dsplit, DEBUG=False):
  """This function select the elements of a pandas dataframe that represent a named entity, (i.e., the words tagged with B-xxx, I-xxx) and add them to a given jsonl dataset."""

  labels_map = {
    "PER": 0,
    "ORG": 1,
    "LOC": 2
  }
  previous = {
    "tag": np.nan, # B, C, O
    "word": np.nan, # word or symbol
    "label": np.nan # PER, ORG, LOC
  }
  entities = []
  entity = []
  sentence = []

  for i, data in enumerate(df.itertuples()): 

    # very bad piece of code
    if (i + 1) < len(df):
      next = df.iloc[i + 1] 
      if pd.isna(next.label):
        next_tag = "stop"
      else:
        next_tag = next.label[0]

    # update sentence counter
    sentence_id = dataset_splits[dsplit]

    # condictions for blank line
    if pd.isna(data.word) and pd.isna(data.label):
      if previous["tag"] in ["B", "I"] and \
        (next_tag != "I"): # this is veeery specific :<:
        # save previous entity
        entity = update_entity(entities, entity, label=labels_map[previous["label"]], DEBUG=DEBUG)

        # reset values for previus sample
        previous["tag"] = np.nan
        previous["word"] = np.nan
        previous["label"] = np.nan

      # change sentence
      break_symbols = {',', ';', ':', '!', '?','<','(', '[', '{', '}', ']', ')', '>'}
      if (previous["word"] not in break_symbols) and \
        (next_tag != "I"): # also this is veeery specific :<
        # make json objects with entities
        if len(entities) > 0:
          sentence_text = join_strings_smartly(sentence)
          make_json(output_jsonl, sentence_id, sentence_text, entities, DEBUG=DEBUG)
          # update sentence counter (here?)
          dataset_splits[dsplit] += 1

        if DEBUG:
          print("\nSentence:")
          print(sentence_text)
          print("\nEntities:")
          print(entities)
          print("\n" + "-"*100 + "\n")

        sentence = [] # delete old sentence
        entities = [] # delete old entities

        # reset values for previus sample
        previous["tag"] = np.nan
        previous["word"] = np.nan
        previous["label"] = np.nan
      
      # same sentence
      else:
        ... # do nothing, somethimes is important to do nothing and just relax  

    else:
      tag = data.label[0]
      word = data.word
      label = data.label[2:]

      # condictions for non-blank lines
      if (tag == "B" and previous["tag"] in ["B", "I"]):
        # save previous entity
        entity = update_entity(entities, entity, label=labels_map[previous["label"]], DEBUG=DEBUG)
        # go on 
        entity.append(data.word)
      
      elif (tag == "O"  and previous["tag"] in ["B", "I"]):
        # save previous
        entity = update_entity(entities, entity, label=labels_map[previous["label"]], DEBUG=DEBUG)

      elif (tag == "B" and previous["tag"] not in ["B", "I"]) or \
          (tag == "I" and previous["tag"] in ["B", "I"]) :
        # go on
        entity.append(data.word) 

      else:
        ... # do nothing
  
      # update values of previous sample
      previous["tag"] = tag
      previous["word"] = word
      previous["label"] = label

      # and add words/symbols in the sentence
      sentence.append(data.word)

    if DEBUG:
      print(data.Index, end=" ")
      print(data.word, end=" ") 
      print(data.label)
      print(f"next label --> {next.label}")


# MAIN
if __name__ == '__main__' : 

  # set up command line args
  parser = argparse.ArgumentParser(description='Dataset Manipulation')
  parser.add_argument('--debug', '-d', action='store_true')
  parser.add_argument('--multiple', '-m', action='store_true')
  args = parser.parse_args()
  DEBUG = args.debug 
  MULTIPLE = args.multiple
  mode = "w" if MULTIPLE else "a"

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
        print(f"Dataset: {dataset} already present")
        ...

  # clear previous results just to be sure
  try:
    shutil.rmtree(results_dir)
  except FileNotFoundError:
    pass

  # make json files
  print("Working...")
  for dtype in dataset_types:
    for dsplit in  dataset_splits.keys():
      dataset = dtype + "_" + dsplit +".tsv"
      # save multiple jsonl files for each dataset 
      if MULTIPLE:
        output_json = "NERMuD_" + dtype + "_" + dsplit + ".jsonl"
      # or save just one file for each split
      else:
        output_json = "NERMuD_" + dsplit + ".jsonl"
      print(f"Dataset --> {dataset}")
      df = make_dataframe(data_dir + dataset, dtype)
      print(f"Dataset len: {len(df)}")
      add_to_json(output_json, df, dataset_splits, dsplit, DEBUG=DEBUG)
      jsonl_files.add(output_json)
      print(f"JSONL output --> {output_json}")


  print(jsonl_files)
  move_data(list(jsonl_files), results_dir)