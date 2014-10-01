import pandas as pd
import numpy as np
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
    elif i < len(beers[0]) - 1:
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

# now let's load all the beers from the former experiment
with open("beernames.txt", "rb") as f:
    names = set([line[1] for line in csv.reader(f, delimiter="\t")])

df = df[df.beer_name.isin(names)]

# get the counts of reviews of each beer
counts = df.groupby("review_profileName").size()
counts.median()
counts.mean()

# filter out the useless ones
# this takes a while, take some questions
df = df.groupby('review_profileName').filter(lambda x: len(x) >= 5)
counts = df2.groupby("review_profileName").size()
counts.median()
counts.mean()

# plot some things
df.plot(x="review_overall", y="beer_ABV"); plt.show()
# obviously the connectedness is screwing things up
df.plot(x="review_overall", y="beer_ABV", ls="", marker="x"); plt.show()
# take a random sample instead
subsample = random.sample(df.index, 500)
df.ix[subsample].plot(x="review_overall", y="beer_ABV", ls="", marker="x"); plt.show()

# now we want to create the dataset we're actually going to use:
# profile_name beer_rating1 beer_rating2 ... beer_ratingN

# first get a list of all the profile names to iterate over
profile_names = sorted(set(df.review_profileName))
# get a list of all the beer names to iterate over
beer_names = np.array(sorted(names))

with open("dataset_extension.tsv", "wb") as f:
    w = csv.writer(f, delimiter="\t")
    # write the header
    w.writerow(["profile_name"] + list(beer_names))
    for profile_name in profile_names:
        # selct the reviews for this user
        reviews = df[df.review_profileName == profile_name][["beer_name", "review_overall"]]
        # put them into an array, to iterate over. This is just because pandas.DataFrame.iterrows
        #   is also inefficient (allocates a new Series in memory for each row), and more annoying
        reviews = np.array(reviews)
        # creates a matrix of ratings, sums them row-wise
        review_vector = sum([(beer_names == beer_name) * rating for beer_name, rating in reviews])
        # write the row to disk!
        w.writerow([profile_name] + list(review_vector))
