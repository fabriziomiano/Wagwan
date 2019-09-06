# Wagwan Fam?

This tool serves those who have, or work for someone who owns, a facebook 
page, and essentially want to know what the people are talking about in their post.


## What is it?

A simple front-end which can be used to run a basic, yet simple, 
keywords extraction on facebook posts. In addition, it employs
[spaCy](https://github.com/explosion/spaCy) default models 
to extract named-entities from comments. Visit spaCy page to know more
about named entities.
This tool is pretty much a word counter that employs 
standard NLP pre-processing, plus the NER part performed by spaCy. 


#### How does it do it?

It brings up a webapp supported by a python back-end 
which is a taylored version of [whats-the-topic](https://github.com/fabriziomiano/whats-the-topic/)
It requires an access token to get people's comments on a selected post. 
Additional info on how to get a token can be found at this [link](https://developers.facebook.com/docs/facebook-login/access-tokens/)
In short, once a facebook developers account has been created, the access token can be generated through
the [Facebook GraphAPI](https://developers.facebook.com/tools/explorer/). 

The tool performs text preprocessing (tokenization, stopwords filtering, stemming) 
to make plots of the keyword-count plus a word cloud image - using the awesome 
[`word_Cloud`](https://github.com/amueller/word_cloud) library.

## For devs

This tool has been developed on Ubuntu 18.04 and macOS High Sierra, but 
has never been seriously tested. 
It requires Python3+ and all the packages listed in `requirements.txt`.


## Results 

Here there are two images of the keyword-count bar plot, and the wordcloud, that are produced
by running the tool on [this](https://www.facebook.com/GiveToTheNext/posts/477277113022512) post:



#### Top 20 keywords

![alt_text](https://github.com/fabriziomiano/Wagwan/blob/master/Wagwan/static/plots/single_posts/477277113022512/barplot_477277113022512.png)


#### Word cloud with no stemming 
![alt text](https://github.com/fabriziomiano/Wagwan/blob/master/Wagwan/static/plots/single_posts/477277113022512/wordcloud_477277113022512.png
)


#### Top 12 entities

This is a bar plot of the top N entities extracted from
[this](https://www.facebook.com/GiveToTheNext/posts/477277113022512) post

![alt_text](https://github.com/fabriziomiano/Wagwan/blob/master/Wagwan/static/plots/barplot_476807096402847_ner.png)


## Acknowledgements

Thanks to the people at [spaCy](https://github.com/explosion/spaCy)
for the NE part,to the people who produced 
[facebook-sdk](https://github.com/mobolic/facebook-sdk)
for the ease of access to the data, and finally to the guys who made 
[word_cloud](https://amueller.github.io/word_cloud) for the awesome word-cloud images
that can be produced.
