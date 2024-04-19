import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")

# Reading data
df = pd.read_csv("CSV/Reviews.csv")

# Shortening dataset
df = df.head(500)

# Quick EDA
# https://www.ibm.com/topics/exploratory-data-analysis
##ax = df["Score"].value_counts().sort_index().plot(kind="bar", title="Count of Reviews by score", figsize=(10, 5))
##ax.set_xlabel("Review score")
##plt.show()

# Basic nltk
# Getting an example and tokenizing
example = df["Text"][50]
tokenized = nltk.word_tokenize(example)
##print(tokenized)
# Getting part of speech
# Downloading averaged perceptron tagger due to error
nltk.download("averaged_perceptron_tagger")

# POS TAG List
# https://www.educba.com/nltk-pos-tag/
tagged = nltk.pos_tag(tokenized)
##print(tagged)

# Putting tags into entities
# Grouping tags into chunks
# Downloading maxent ne chunker, words due to error
nltk.download("maxent_ne_chunker")
nltk.download("words")

entities = nltk.chunk.ne_chunk(tagged)
entities.pprint()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Using VADER (Valence Aware Dictionary and sEntiment Reasoner)
# Using bag of words approach
# Stop words are removed (and, the, ...)
# Gets words in a sentence and gives positive, neutral or negative sentiment values
# Does not account for words relations

# Importing sentiment intensity analyzer
from nltk.sentiment import SentimentIntensityAnalyzer
# Importing progress bar tracker
from tqdm import tqdm

# Downloading vader lexicon due to error
nltk.download("vader_lexicon")
# Creating sentiment analyzer object
sia = SentimentIntensityAnalyzer()
# Testing sia
##print(sia.polarity_scores("I am so happy!"))

# Testing sia 2
##print(sia.polarity_scores("This is the worst thing ever."))

# Testing sia 3 - using example
##print(sia.polarity_scores(example))

# Run the polarity score on the entire dataset
res = {}
# Iterate through rows, tqdm generates the progress tracker
for i, row in tqdm(df.iterrows()):
    # Get text and id then populates the dictionary with the polarity scores
    text = row["Text"]
    myid = row["Id"]
    res[myid] = sia.polarity_scores(text)

##print(res)

# Creating dataframe from res dictionary
# T -> flips the dataframe horizontally
vaders = pd.DataFrame(res).T
vaders = vaders.reset_index().rename(columns={'index': 'Id'})
vaders = vaders.merge(df, how="left", on="Id")
##print(vaders)

# Creating barplot using seaborn for neutral, negative and positive values
# Using matplotlib subplots
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
sns.barplot(data=vaders, x="Score", y="pos", ax=axs[0])
sns.barplot(data=vaders, x="Score", y="neu", ax=axs[1])
sns.barplot(data=vaders, x="Score", y="neg", ax=axs[2])
axs[0].set_title("Positive")
axs[1].set_title("Neutral")
axs[2].set_title("Negative")
plt.tight_layout()
plt.show()


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# From hugging face, using transformer pretrained model Roberta
#https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
# These transformer models can detect words relations
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Getting model
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)





