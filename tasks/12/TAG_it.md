# TAG-it

Homepage: https://sites.google.com/view/tag-it-2020/task

Download Link: https://live.european-language-grid.eu/catalogue/corpus/8112/download/

This can be seen as a follow-up of the GxG task organised in the context of EVALITA 2018  though with some differences. GxG was concerned with gender prediction, and had two distinctive traits: (i) models were trained and tested cross-genre, and (ii) evidence per author was for some genres (Twitter and YouTube) extremely limited (one tweet or one comment). The combination of these two aspects yielded scores that were comparatively lower than those observed in other campaigns, and for other languages. One of the core reasons for training the models cross-genre was to remove as much as possible genre-specific traits, but also topic-related features. The two would basically coincide in most n-gram-based models, which are standard for this task. 

## Data

The data come in several `.txt` files. You have to use as training the file *training.txt* and for test *test_task1.txt*. The files contains xml objects where there is a list of \<users\> where each of them contains a list of \<post\>.

## Expected output

Don't follow the tasks definition given in the EVALITA site. 

For each user you have to create a single sample.
You should group the posts of a single user (use up to 5 posts) and use them to predict the Topic of the grouped posts. 


### Task TAG-it-topic

Consider only the **Topic** label.

Create ```TAG-it-train.jsonl```, ```TAG-it-test.jsonl```.

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

#### Distractors

We expect from you to design a strategy to include distractors among the possible topics, so you select three different wrong topics beside the correct one. These three labels must be challenging for the selected posts.

### Prompts

Create```prompts.jsonl```.

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


## Prompts

1) dati i seguenti post {{post1}},{{post2}},{{post3}},{{post4}},{{post5}} qual'è l'argomento comune?
1a) dati i seguenti post {{post1}},{{post2}},{{post3}},{{post4}},{{post5}} qual'è l'argomento comune tra {{choices[]}}?
2) {{post1}},{{post2}},{{post3}},{{post4}},{{post5}}\n
qual'è l'argmento di questa conversazione? 
2a) {{post1}},{{post2}},{{post3}},{{post4}},{{post5}}\n
qual'è l'argmento di questa conversazione tra {{choices[]}}? 
3) 