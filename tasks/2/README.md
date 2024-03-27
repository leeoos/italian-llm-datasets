**NERMuD**

LINK: https://nermud.fbk.eu/

Named-Entities Recognition on Multi-Domain Documents (NERMuD) is a task presented at EVALITA 2023 consisting in the extraction and classification of named-entities in a document, such as persons, organizations, and locations.

1. Download the data from : https://github.com/dhfbk/KIND/tree/main/evalita-2023

### Reformat data:
You will find three datasets: "ADG", "FIC", and "WN", already split in train, dev and test.

For ADG, and FIC datasets, first, obtain the sentences (consider using SpaCy in this process). For more details check: https://stackoverflow.com/questions/46290313/how-to-break-up-document-by-sentences-with-spacy

Here you have to reason at the entity-level. Given the words of a named entity, i.e., the ones tagged with B-xxx, I-xxx, , the model must be prompted to predict the correct label. Create a sample for each named entity in the input

```JSON
{
    "sentence_id": int, # an incremental integer (starting from zero)
    "text": str, # the input sentence,
    "target_entity": str, # can be a multi-word
    "choices": List[str],
    "label": int, # the correct answer
}
```
Do the same for the WN dataset. Note that, in this case, the provided text is already split in sentences.

write the resulting jsons in ```NERMuD_{split}.jsonl```, replace {split} with [train, dev, test] according to the data you are processing.


### Prompts

Create ```prompt.jsonl```.
In this file you have to report the prompts you designed for the task. 
Each line in your output file (1 line per prompt) must be a JSON object like the one below:

```JSON
{
    "prompt": "..."
}
```


## Deliver format

You have to format your data using JSON Lines standard.
