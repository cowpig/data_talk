import pandas as pd
import re
import csv
from matplotlib import pyplot as plt
import random

# first call head and tail on the file, wc -l

# grab the headers using sublimetext
headers = [
    "beer_name", 
    "beer_beerId", 
    "beer_brewerId", 
    "beer_ABV", 
    "beer_style", 
    "review_appearance", 
    "review_aroma", 
    "review_palate", 
    "review_taste", 
    "review_overall", 
    "review_time", 
    "review_profileName", 
    "review_text"
]

# regexpal.com is useful for working out regular expressions
p = re.compile("(?:beer|review)/.*: (.*)\n?")

# open a subset of the file first to work this expression out
with open("beeradvocate.txt", "rb") as f:
    beers = [p.findall(line.replace("\t", "  ")) for line in f.read().strip().split("\n\n")]
# check that wc -l beeradvocate.txt / 14 == len(beers)

# take a first glance at the contents of each column
for i in xrange(len(beers[0])):
    s = set([review[i] for review in beers])
    print headers[i], len(s)
    if len(s) <= 15:
        print sorted(list(s))
    elif i < len(beers)-1:
        print sorted(list(s))[:5], sorted(list(s))[-5:]

# save the data as tab-separated values
with open("beeradvocate.tsv", "wb") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(headers)
    w.writerows(beers)

# import the tsv file as a pandas dataframe
df = pd.read_csv("beeradvocate.tsv", sep="\t")
df.columns.values

# cast the numerical columns to numbers (useful for vectorization later)
def cast(df, headers, cast_to):
    for header in headers:
        df[header] = df[header].astype(cast_to)
cast(df, ["beer_ABV", "review_appearance", "review_aroma", "review_palate", "review_taste", "review_overall", "review_time"], float)

# plot some things
df.plot(x="beer_ABV", y="review_overall"); plt.show()
# too many to plot! take a random sample instead
random_subsample = random.sample(df.index, 5000)
df.ix[random_subsample].plot(x="review_overall", y="beer_ABV", ls="", marker="."); plt.show()

# get the counts of reviews of each beer
counts = df.groupby("beer_name").size()
counts.median()
counts.mean()

# filter out the useless ones
# this takes a while, take some questions
df = df.groupby('beer_beerId').filter(lambda x: len(x) >= 5)
len(df)

# next step would be to vectorize the data, using one-hot vectors for categorical strings
