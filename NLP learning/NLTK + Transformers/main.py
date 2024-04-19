import nltk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("ggplot")

# Reading data
df = pd.read_csv("CSV/Reviews.csv")

# Shortening dataset
df = df.head(51)

# Quick EDA
# https://www.ibm.com/topics/exploratory-data-analysis
##ax = df["Score"].value_counts().sort_index().plot(kind="bar", title="Count of Reviews by score", figsize=(10, 5))
##ax.set_xlabel("Review score")
##plt.show()

# /// USING NLTK ///
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

# /// USING VADER ///
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


# /// USING TRANSFORMERS  ///
# From hugging face, using transformer pretrained model Roberta
# https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest
# These transformer models can detect words relations
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Getting model
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# /// Comparing VADER X Roberta

# /// Comparing VADER result on example with the model ///
print(sia.polarity_scores(example))

# tokenizing the text
encoded_text = tokenizer(example, return_tensors="pt")

# Running model on encoded text -> returns a pytorch tensor
output = model(**encoded_text)
# Converting tensor to numpy
scores = output[0][0].detach().numpy()
# Applying softmax
scores = softmax(scores)

# Converting scores to a dictionary
scores = {
    "roberta_neg": scores[0],
    "roberta_neu": scores[1],
    "roberta_pos": scores[2],
}
print(scores)

# /// Comparing dataset results with VADER and Roberta ///
# The Roberta model runs faster using GPU instead of CPU
# Creating function to generate polarity scores using Roberta
def polarity_scores_roberta(example):
    # tokenizing the text
    encoded_text = tokenizer(example, return_tensors="pt")

    # Running model on encoded text -> returns a pytorch tensor
    output = model(**encoded_text)
    # Converting tensor to numpy
    scores = output[0][0].detach().numpy()
    # Applying softmax
    scores = softmax(scores)

    # Converting scores to a dictionary
    scores = {
        "roberta_neg": scores[0],
        "roberta_neu": scores[1],
        "roberta_pos": scores[2],
    }
    return scores

# Generating scores using dataset
# There's an error with tensor size:
# RuntimeError: The expanded size of the tensor (571) must match the existing size (514) at non-singleton dimension 1.  Target sizes: [1, 571].  Tensor sizes: [1, 514]
# So, they'll be skipped (try.. except)
res = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    try:
        text = row["Text"]
        myid = row["Id"]

        vader_results = sia.polarity_scores(text)
        roberta_result = polarity_scores_roberta(text)

        # Renaming vader results
        vader_results_rename = {}
        for key, value in vader_results.items():
            vader_results_rename[f"vader_{key}"] = value

        # Merging results
        both = {**vader_results_rename, **roberta_result}
        res[myid] = both
    except RuntimeError:
        print(f"Broke for id{myid}")

##print(res)
# Creating dataframe with both results
results_df = pd.DataFrame(res).T
results_df = results_df.reset_index().rename(columns={"index": "Id"})
results_df = results_df.merge(df, how="left")

# Compare scores between models using seaborn pairplot
axs[0] = sns.pairplot(data=results_df, 
             vars=["vader_neg", "roberta_neg"],
             hue="Score",
             palette="tab10"
            )
axs[1] = sns.pairplot(data=results_df, 
             vars=["vader_neu", "roberta_neu"],
             hue="Score",
             palette="tab10"
            )
axs[2] = sns.pairplot(data=results_df, 
             vars=["vader_pos", "roberta_pos"],
             hue="Score",
             palette="tab10"
            )
plt.show()

# Showing first text where there are a positive 1-star review
print(results_df.query("Score == 1").sort_values("roberta_pos", ascending=False)["Text"].values[0])
# Now using VADER
print(results_df.query("Score == 1").sort_values("vader_pos", ascending=False)["Text"].values[0])

# Showing first text where there are a negative 5-star review
print(results_df.query("Score == 5").sort_values("roberta_neg", ascending=False)["Text"].values[0])
# Now using VADER
print(results_df.query("Score == 5").sort_values("vader_neg", ascending=False)["Text"].values[0])