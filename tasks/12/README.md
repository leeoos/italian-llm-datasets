# TAG-it

Homepage: https://sites.google.com/view/tag-it-2020/task

Download Link: https://live.european-language-grid.eu/catalogue/corpus/8112/download/

This can be seen as a follow-up of the GxG task organised in the context of EVALITA 2018  though with some differences. GxG was concerned with gender prediction, and had two distinctive traits: (i) models were trained and tested cross-genre, and (ii) evidence per author was for some genres (Twitter and YouTube) extremely limited (one tweet or one comment). The combination of these two aspects yielded scores that were comparatively lower than those observed in other campaigns, and for other languages. One of the core reasons for training the models cross-genre was to remove as much as possible genre-specific traits, but also topic-related features. The two would basically coincide in most n-gram-based models, which are standard for this task. 

## Data

The data come in several `.txt` files. You have to use as training the file *training.txt* and for test *test_task1.txt*. The files contains xml objects where there is a list of \<users\> where each of them contains a list of \<post\>.

## Expected output

You don't have to follow the tasks definition given in the EVALITA site. 

For each user you have to create different samples, for each sample you have to take 5 different posts and predict separatelly **Topic**, **Age**, and **Genre**, so split each user diving by 5 the total number of posts.

### Task A TAG-it-topic

Consider only the **Topic** label.

Create ```TAG-it-topic-train.jsonl```, ```TAG-it-topic-test.jsonl```.

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "post1": str,
    "post2": str,
    "post3": str,
    "post4": str,
    "post5": str,
    "choices": list[str],
    "label": int
}
```

### Task B TAG-it-age

Consider only the **Age** label.

Create ```TAG-it-age-train.jsonl```, ```TAG-it-age-test.jsonl```.

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "post1": str,
    "post2": str,
    "post3": str,
    "post4": str,
    "post5": str,
    "choices": list[str],
    "label": int
}
```

### Task C TAG-it-genre

Consider only the **Genre** label.

Create ```TAG-it-genre-train.jsonl```, ```TAG-it-genre-test.jsonl```.

Each line in your output file must be a JSON object like the one below:

```JSON
{
    "post1": str,
    "post2": str,
    "post3": str,
    "post4": str,
    "post5": str,
    "choices": list[str],
    "label": int
}
```

### Prompts

Create ```prompts-genre.jsonl```, ```prompts-topic.jsonl```, and ```prompts-age.jsonl```.

In this file you have to report the prompts you designed for the task. 
Each line in your output file (1 line per prompt) must be a JSON object like the one below (max 5 lines in this file):

```JSON
{
    "prompt": str
}
```

## Deliver format

You have to format your data using JSON Lines standard.

## License

Creative Commons Attribution Non Commercial Share Alike 4.0 International