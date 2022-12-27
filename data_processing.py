import pandas as pd
import csv
import random as r


# Configure format settings for pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
#%%

# Read in tweets and look at first 5 rows
# Step 1 - clean raw data
data = pd.read_csv("data/leader_tweets_kenya.csv")
data.head()

# Remove any tweets that are retweets
to_drop = data.loc[(data["Text"].str.contains("RT @"))]
data.drop(list(to_drop.index), inplace = True)

# Clean up the date format (must be in YYYY-MM-DD format)
cleaned_dates = []
for date in data.loc[:, "Date"]:
    cleaned_dates.append(date.split("T")[0])
data.loc[:, "Date"] = cleaned_dates

# Remove any links in tweets
no_links = []
for tweet in data.loc[:, "Text"]:
    no_links.append(tweet.split(" http")[0])
data.loc[:, "Text"] = no_links

# Save cleaned data to new csv file
data.to_csv("data/leader_tweets_kenya_clean.csv", index=False)
new_data = pd.read_csv("data/leader_tweets_kenya_clean.csv")

print(f"STEP 1 : Successfully cleaned raw data and exported to new csv file.\n")
print(f"--- STEP 2 beginning ---")

# Step 2 - find only tweets that mention a country
# Read in a file of all countries
countries = []
with open("data/countries.csv", "r") as countriesfile:
    reader = csv.reader(countriesfile)
    next(reader)
    for row in reader:
        countries.append(row)
countries.remove(["KE", "Kenya"]) # Remove Kenya, only need to find other countries
#%%
# Dataset to be used for processing
# data = pd.read_csv("data\leader_tweets_kenya_clean.csv")
# data.head()
#%%

# Find target data (and frequency of countries being mentioned)
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

print(f"Number of tweets found is: {len(target_tweets)}") # Should be 3328

# Frequency for countries
sorted_frequency_map = sorted(frequency_map.items(), key = lambda kv: kv[1])
sorted_frequency_map.reverse()
sorted_frequency_map = dict(sorted_frequency_map)
print(f"Frequency of countries: \n {sorted_frequency_map}")
target_dataset = pd.DataFrame(target_tweets, columns=["Date", "Text"])
#%%

# Uncomment to save as .csv
#target_dataset.to_csv("data\target_data.csv", index=False)
#%%

# Uncomment to reload data
data = pd.read_csv("data/target_data.csv")
data = data.reset_index()

#%%

# Function to obtain a n-random sample of the tweets
def sample_data(n):
    sample = []

    for date, tweet in zip(data["Date"], data["Text"]):
        seed = r.random()
        if seed >= 0.80 and len(sample) <= n:
            sample.append([date, tweet])

    sample = pd.DataFrame(sample).to_csv(f"data/sampled_tweets{n}.csv", index=False)
    return f"Successfully sampled {n} tweets"


sample_data(200)
print(f"STEP 2 : Found tweets mentioning countries and took a random sample")