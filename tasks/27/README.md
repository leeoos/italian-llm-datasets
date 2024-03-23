# TASK 27 - HaSpeeDe 3
Homepage: http://www.di.unito.it/~tutreeb/haspeede-evalita23/data.html
GitHub: https://github.com/mirkolai/EVALITA2023-HaSpeeDe3

## Data
The dataset is already split into training (development folder) and test (gold folder) set.
The train set consist of 5,600 tweets belonging to **PolicyCorpusXL**.
The test set consists of 1,400 tweets belonging to **PolicyCorpusXL** and 3,000 tweets belonging to **ReligiousHate.**

- **Task 1 - Hate Speech Detection**: a binary classification task aimed at determining whether the message contains Hate Speech or not
  - Political Hate Speech Detection: development and test data from  PolicyCorpusXL

- **Task 2 - Contextual Hate Speech Detection**: a binary classification task aimed at determining whether the message contains Hate Speech or not, leveraging also the metadata of the tweets
  - Political Hate Speech Detection: development and test data from PolicyCorpusXL
  - Religious Hate Speech Detection: test data from XReligiousHate. Note that only the test set is available for this task, as it was adapted from the original cross-domain task.

**NOTE**: how to leverage the contextual metadata (e.g., number of replies, post date, etc.) is up to you, so remember to explain your reasoning in the report :)

## Expected output
The expected output is two (2) datasets per tasks (train and test splits) + one (1) prompt file per tasks.

Files to submit: 
- `haspeede3-task1-train-data.jsonl`
- `haspeede3-task1-test-data.jsonl`
- `haspeede3-task1-prompt.jsonl`
- `haspeede3-task2-train-data.jsonl`
- `haspeede3-task2-test-data.jsonl`
- `haspeede3-task2-prompt.jsonl`

Each line in the data files should be a JSON object following this format:
```JSON
{
    "id":       int,
    "text":     str,
    "choices":  list[str],
    "label":    int
}
```

In the prompt file you have to report the prompts you designed for the task.
Each line in the prompt files should be a JSON object following this format (max 5 lines):
```JSON
{
    "prompt": str
}
```
