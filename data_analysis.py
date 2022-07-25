import pandas as pd
import csv
import pprint as pp
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# Configure format settings for pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
#%%

# Read in any necessary files:
countries = []
with open("data\countries.csv", "r") as countriesfile:
    reader = csv.reader(countriesfile)
    next(reader)
    for row in reader:
        countries.append(row)
countries.remove(["KE", "Kenya"])
#%%
# Dataset
# data = pd.read_csv("data\leader_tweets_kenya_clean.csv")
# data.head()
#%%

# Targeted data
target_tweets = []
other_tweets = []
frequency_map = {}
for date, tweet in zip(data["Date"], data["Text"]):
    for country in countries:
        if country[1] in tweet:
            if [date, tweet] not in target_tweets:
                target_tweets.append([date, tweet])
            if country[1] in frequency_map.keys():
                frequency_map[country[1]] += 1
            else:
                frequency_map[country[1]] = 1

len(target_tweets) #3328

# Frequency for countries
sorted_frequency_map = sorted(frequency_map.items(), key = lambda kv: kv[1])
sorted_frequency_map.reverse()
sorted_frequency_map = dict(sorted_frequency_map)
sorted_frequency_map

target_dataset = pd.DataFrame(target_tweets, columns=["Date", "Text"])
#%%

# Uncomment to save as .csv
#target_dataset.to_csv("data\target_data.csv", index=False)
#%%

# Uncomment to reload data
data = pd.read_csv("data/target_data.csv")
data = data.reset_index()
#%%

outbound_terms = [
    "meeting in",
    "met with",
    "visit to",
    "is visiting",
    "visited",
    "held a press briefing"
]

inbound_terms = [
    "courtesy call",
    "held a meeting",
    "held meeting",
    "bilateral talks",
    "bilateral meeting",
    "official talks",
    "received",
    "is hosting",
    "is receiving",
    "receives",
    "host",
    "was hosted"
]
#%%

def searcher(search_terms, data):
    info = []
    copy_of_data = data.copy()
    for index, row in data.iterrows():
        current_data = [ row["Date"], row["Text"] ]
        for term in search_terms:
            if term in row["Text"] and current_data not in info:
                info.append(current_data)
                copy_of_data.drop(index, inplace=True)
    return [info, copy_of_data]
#%%

in_data = searcher(inbound_terms, data)[0]
len(in_data)
for idx in range(len(in_data)):
    pp.pprint(f"Index is: {idx}. Text: {in_data[idx]}")
#%%

indices_to_remove = [5, 8, 29, 33, 51, 52, 53, 54, 56, 57, 65, 70, 82, 85, 96, 97 ]
indices_to_switch = [7, 9, 10, 11, 12, 13, 14, 17, 18, 19, 21, 23, 31, 49, 55, 58, 60, 83, 89]

del in_data[5, 8]

out_data = searcher(outbound_terms, data)[0]
len(out_data)
remainder = []
copy_of_data = data.copy()

all_terms = outbound_terms + inbound_terms

expected = searcher(all_terms, data)[0]
len(expected)
len(data)

#%%
