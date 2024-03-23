# TASK 22 - AcCompl-it
- Homepage: https://sites.google.com/view/accompl-it/home-page
- GitHub: https://live.european-language-grid.eu/catalogue/corpus/8113/download/

## Data 
AcCompl-It is a task aimed at developing and evaluating methods to classify Italian sentences according to Acceptability and Complexity.
- **Acceptability** is the native speakers’ judgment of the well-formedness of a sentence. This is the core dimension for the evaluation of both formal and psycho-linguistic theories as well as for generation, summarization and machine translation tasks;
- **Complexity**, namely a measure of the native speakers’ effort in processing a sentence, is required both for comparing neurolinguistic and psycholinguistic theories and for rating the accessibility of a text. Unlike more conventional studies on human sentence processing carried out in experimental settings, in this task this measure is intended as a judgment of perceived complexity given by humans to a sentence. This measure is also relevant for developing text generation systems addressing a specific target user in terms of linguistic competence.

**NOTE**: you shall perform only task 1 and 2, ignore task 3. Ignore also the requirements for the estimation of the standard error.

**NOTE**: the Acceptability and Complexity metrics were originally declined as a score given to a sentence on a 7-points Likert scale (1 = lowest, 7 = highest).
However, you are required to verbalise these scores using the common Likert-scale verbalisation (e.g., "Eccellente" in place of "7"). 
Furthermore, the actual data may have scores ranging over the previously mentioned Likert-scale. 
What you can do is simply to use the new range and verbalise the scores based off the Likert scale intuition.

The dataset is already splitted into training and test data (labels of test data are present in the `gold` folder).
For further details on the data, please refer to the website. 

## Expected output

The expected output is two (2) datasets per tasks + one (1) prompt file per tasks.

### Task 1 - ACCEPT Subtask
Files to submit: 
- `ACCOMPLIT-task1-train-data.jsonl`
- `ACCOMPLIT-task1-test-data.jsonl`
- `ACCOMPLIT-task1-prompt.jsonl`

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

### Task 2 - COMPL Subtask
Files to submit: 
- `ACCOMPLIT-task2-train-data.jsonl`
- `ACCOMPLIT-task2-test-data.jsonl`
- `ACCOMPLIT-task2-prompt.jsonl`

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
