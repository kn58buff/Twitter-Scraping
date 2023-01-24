import pandas as pd
from sklearn import svm
import spacy
import pickle
import os

# Configure format settings for pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Load complete data
data = pd.read_csv("data/raw_tweets/target_data.csv")
data = data.reset_index()

# load training data and split
train = pd.read_csv("data/sampled_tweets/sampled_tweets200_categorized.csv")
train_x = train["Text"]
train_y = train["Category"]

# load test data
test = pd.read_csv("data/sampled_tweets/sampled_tweets100_categorized.csv")
test_x = test["Text"]
test_y = test["Category"]

check = os.path.isfile("data/model_training/clf_svm/clf_svm.pickle")

# load nlp model from spacy
nlp = spacy.load("en_core_web_lg")

if not check:
    # vectorize train data

    train_x_vecs = [nlp(text).vector for text in train_x]

    # fit model to train data
    clf_svm = svm.SVC(kernel = "linear")
    clf_svm.fit(train_x_vecs, train_y)

    # uncomment to save model
    pickle.dump(clf_svm, open("data/model_training/clf_svm/clf_svm.pickle", "wb"))

# load model
model = pickle.load(open("data/model_training/clf_svm/clf_svm.pickle", "rb"))

# vectorize test data
test_x_vecs = [nlp(text).vector for text in test_x]
result = model.score(test_x_vecs, test_y) #0.82
print(result)

check_preds = os.path.isfile("data/predictions/preds_with_clfsvm.csv")
if not check_preds:
    full_x_vecs = [nlp(text).vector for text in data["Text"]]
    full_preds = model.predict(full_x_vecs)

    full_preds_df = pd.DataFrame(full_preds, columns=["Category"])

    compl_data = pd.concat([data, full_preds_df], axis=1)
    compl_data.to_csv("data/predictions/preds_with_clfsvm.csv", index=False)