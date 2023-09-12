import pandas as pd
import classify_tweets as classify
import pickle as pp
import csv

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def clean_data(data):
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

    return data


def filter_data(data):
    countries = []
    with open("../../data/countries.csv", "r") as countriesfile:
        reader = csv.reader(countriesfile)
        next(reader)
        for row in reader:
            countries.append(row)
    countries.remove(["KE", "Kenya"])

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

    print(f"Number of tweets found is: {len(target_tweets)}")
    target_dataset = pd.DataFrame(target_tweets, columns=["Date", "Text"])

    return target_dataset

raw_pres_tweets = pd.read_csv("../../data/raw_tweets/raw_president_tweets.csv")
clean_pres_tweets = clean_data(raw_pres_tweets)
filtered_tweets = filter_data(clean_pres_tweets)

# Uncomment next 2 lines to save as separate csv files
#clean_pres_tweets.to_csv("data/raw_tweets/clean_president_tweets.csv")
#filtered_tweets.to_csv("data/raw_tweets/filtered_president_tweets.csv")

# Load vectorizer and classifier
loaded_vec = pp.load(open("../../data/model_training/200_samples/TfidfVectorizer().pickle", 'rb'))
loaded_classifier = pp.load(open("../../data/model_training/200_samples/CalibratedClassifierCV().pickle", 'rb'))

preds_arr = []
for msg in filtered_tweets.Text:
    res = classify.predict(msg, loaded_vec, loaded_classifier)
    preds_arr.append([msg, res])

prediction_df = pd.DataFrame(preds_arr, columns=["Text", "Category"])
prediction_df.to_csv("data/predictions/presidential_tweets.csv", index=False)
