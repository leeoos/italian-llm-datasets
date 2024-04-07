# Resources

## General resources  
- Homework presentation -> [link](https://docs.google.com/presentation/d/1DxKuGBhC78XzUlKZzIAPg6xxOJxUykCYpyClMDqzUik/edit#slide=id.g2c523027c45_1_158)

- Standard JSONL format rules -> [link](https://jsonlines.org/)

- Official python JSON library -> [link](https://docs.python.org/3/library/json.html) 

- OverLeaf template [link](https://www.overleaf.com/read/crtcwgxzjskr#7213b2)

## How to Submit (and What)
- You have to create a file for each split present in the EVALITA dataset.
- If only train and test are provided, deliver only train and test splits.
- Then a prompt file in jsonl format, called prompts.jsonl, one for each task.
- Important!!! you have to submit all the code (for each task)

For the folder structure:
```code 
HM1_A-<student_id>/
  <group-id>_<distractor_task_name>/	
    - train.jsonl
    - val.jsonl
    - test.jsonl
    - Report.pdf  # this identical for all the members of a specific group. All students must deliver a copy
    - scripts.py
  <task_name-1>/
    - scripts.py
    - <subtask_name>-train.jsonl
    - <subtask_name>-valid.jsonl
    - <subtask_name>-test.jsonl
    - <task_name-1>_prompts[_subtask_name].jsonl
    - <task_name-1>_Report.pdf # this instead is specific of a student.
…

```