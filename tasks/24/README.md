# TASK 24 - SENTIPOLC
- Homepage: http://www.di.unito.it/~tutreeb/sentipolc-evalita16/index.html
- Train data: http://www.di.unito.it/~tutreeb/sentipolc-evalita16/training_set_sentipolc16.csv.zip
- Test data: http://www.di.unito.it/~tutreeb/sentipolc-evalita16/test_set_sentipolc16_gold2000.csv.zip
## Data
The main goal of SENTIPOLC is sentiment classification at message level on Italian tweets. 
The task is divided into three sub-tasks with an increasing level of complexity. 

1. **Subjectivity Classification**: Given a message, decide whether the message is subjective or objective.

2. **Polarity Classification**: Given a message, decide whether the message is of positive, negative, neutral or mixed sentiment (i.e. conveying both a positive and negative sentiment).

3. **Irony Detection**: Given a message, decide whether the message is ironic or not

Please, *do refer* to the task guidelines (the .pdf file) for further explanation on the data.

## Expected output
The expected output is two (2) datasets per tasks (train and test splits) + one (1) prompt file per tasks.

Files to submit: 
- `sentipolc-task1-train-data.jsonl`
- `sentipolc-task1-test-data.jsonl`
- `sentipolc-task1-prompt.jsonl`
- `sentipolc-task2-train-data.jsonl`
- `sentipolc-task2-test-data.jsonl`
- `sentipolc-task2-prompt.jsonl`
- `sentipolc-task3-train-data.jsonl`
- `sentipolc-task3-test-data.jsonl`
- `sentipolc-task3-prompt.jsonl`

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
