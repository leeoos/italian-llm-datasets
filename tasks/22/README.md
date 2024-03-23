# TASK 22 - GxG
- Homepage: https://sites.google.com/view/gxg2018
- GitHub: https://github.com/malvinanissim/gxg/tree/master/Data/Training


## Data
Given a collection of texts, the gender of the author has to be predicted. 
The task is cast as a binary classification task, with gender represented as female or male.
The distribution of genders will be controlled for (50/50).

The dataset is already splitted into training and test data (labels of test data are present in the `gold` folder).
For further details on the data, please refer to the website. 

## Expected output

The expected output is two (2) datasets per tasks + one (1) prompt file per tasks.

Files to submit: 
- `GxG-task1-train-data.jsonl`
- `GxG-task1-test-data.jsonl`
- `GxG-task1-prompt.jsonl`


Each line in the data files should be a JSON object following this format:
```JSON
{
    "id":           int,
    "text":         str,
    "choices":      list[str],
    "label":        int
}
```

In the prompt file you have to report the prompts you designed for the task.
Each line in the prompt files should be a JSON object following this format (max 5 lines):
```JSON
{
    "prompt": str
}
```
