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
ax = df["Score"].value_counts().sort_index().plot(kind="bar", title="Count of Reviews by score", figsize=(10, 5))
ax.set_xlabel("Review score")
#plt.show()

# Basic nltk
# Getting an example and tokenizing
example = df["Text"][50]
tokenized = nltk.word_tokenize(example)
#print(tokenized)
# Getting part of speech
# Downloading averaged perceptron tagger due to error
nltk.download("averaged_perceptron_tagger")

# POS TAG List
# https://www.educba.com/nltk-pos-tag/
tagged = nltk.pos_tag(tokenized)
#print(tagged)

# Putting tags into entities
# Grouping tags into chunks
# Downloading maxent ne chunker, words due to error
nltk.download("maxent_ne_chunker")
nltk.download("words")

entities = nltk.chunk.ne_chunk(tagged)
entities.pprint()

