import pandas as pd
import csv
import pprint as pp
import random as r


# Read in tweets and look at first 5 rows
data = pd.read_csv("leader_tweets_kenya.csv")

data.head()
to_drop = data.loc[(data["Text"].str.contains("RT @"))]
data.drop(list(to_drop.index), inplace = True)

cleaned_dates = []
for date in data.loc[:, "Date"]:
    cleaned_dates.append(date.split("T")[0])

data.loc[:, "Date"] = cleaned_dates

no_links = []
for tweet in data.loc[:, "Text"]:
    no_links.append(tweet.split(" http")[0])

data.loc[:, "Text"] = no_links

data.to_csv("leader_tweets_kenya_clean.csv", index=False)

new_data = pd.read_csv("leader_tweets_kenya_clean.csv")

sample = []

for date, tweet in zip(new_data["Date"], new_data["Text"]):
    seed = r.random()
    if seed >= 0.80:
        sample.append([date, tweet])

sample = pd.DataFrame(sample).to_csv("sampled_tweets.csv", index=False)
