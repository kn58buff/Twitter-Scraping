# Import necessary modules
import json
import time
import requests
import pandas as pd

# Function to create requests header
def create_headers():
    bearer_token = "REPLACE WITH OWN"
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# Function to create requests URL
# By default, the endpoint is the full archive search
def create_url(keywords, start, max_results):
    search_url = "https://api.twitter.com/2/tweets/search/all"

    query_params = {"query" : keywords,
                    "start_time" : start,
                    "max_results": max_results,
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    "pagination_token" : {}}

    return (search_url, query_params)

# Creates a connection to the endpoint and requests a response
def endpoint_connection(url, headers, params, pagination_token = None):
    params["pagination_token"] = pagination_token
    response = requests.request("GET", url, headers = headers, params = params)
    print("Successful connection! Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

# Wrapper function. Pulls entirety of tweets from a desired account.
def scrape(keywords, start, max_results):
    again = True
    pagination_token = None
    list_of_tweets = []
    while again:
        url = create_url(keywords, start, max_results)
        response = endpoint_connection(url[0], headers, url[1], pagination_token)
        for tweet in response["data"]:
            tweet_details = {"Date": tweet["created_at"],
                             "Text": tweet["text"]}
            list_of_tweets.append(tweet_details)

        if "next_token" in response["meta"]:
            pagination_token = response["meta"]["next_token"]
            time.sleep(5)
        else:
            again = False
            pagination_token = None
        time.sleep(5)
    print(len(list_of_tweets))
    return list_of_tweets

# Converts a list of tweet details to a pandas DataFrame. By default, exports as a .csv file
def tweets_to_df(tweets, to_csv = "True"):
    df = pd.DataFrame(tweets)

    if to_csv == "True":
        df.to_csv("data/state_dept.csv", index=False)
        return df
    elif to_csv == "False":
        return df

headers = create_headers()
keywords = "from: StateDept"
start = "2006-03-21T00:00:00.000Z"
max_results = 500

tweets = scrape(keywords, start, max_results)
#%%
tweets_to_df(tweets)
