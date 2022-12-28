import csv
from sklearn import naive_bayes, dummy, ensemble, neighbors, tree, feature_extraction, calibration, linear_model, multiclass, svm
import pandas as pd
import pickle as pp

learn_data = pd.read_csv("data/sampled_tweets/sampled_tweets200_categorized.csv")
test_data = pd.read_csv("data/sampled_tweets/sampled_tweets_categorized.csv")
complete_data = pd.read_csv("data/raw_tweets/target_data.csv")

def test_performance(classifiers, vectorizers, train, test):
    ratings = {}
    for classifier in classifiers:
        for vec in vectorizers:
            vectorize_text = vec.fit_transform(train["Text"])
            classifier.fit(vectorize_text, train["Category"])

            vectorize_text = vec.transform(test["Text"])
            score = classifier.score(vectorize_text, test["Category"])

            ratings[f"{classifier.__class__.__name__} with {vec.__class__.__name__}"] = score
    return ratings

classifiers = [
    naive_bayes.BernoulliNB(), ensemble.RandomForestClassifier(n_estimators= 10, n_jobs= -1), ensemble.AdaBoostClassifier(),
    ensemble.BaggingClassifier(), ensemble.ExtraTreesClassifier(), ensemble.GradientBoostingClassifier(), tree.DecisionTreeClassifier(),
    calibration.CalibratedClassifierCV(), dummy.DummyClassifier(), linear_model.PassiveAggressiveClassifier(),
    linear_model.RidgeClassifier(), linear_model.RidgeClassifierCV(), linear_model.SGDClassifier(), neighbors.KNeighborsClassifier(),
    multiclass.OneVsRestClassifier(svm.SVC(C=10, gamma=1, kernel = "linear")), multiclass.OneVsRestClassifier(linear_model.LogisticRegression())
]

vectorizers = [
    feature_extraction.text.CountVectorizer(),
    feature_extraction.text.TfidfVectorizer(),
    feature_extraction.text.HashingVectorizer()
]

#test_performance(classifiers, vectorizers, learn_data, test_data)

classifiers_to_test = [ensemble.BaggingClassifier(), calibration.CalibratedClassifierCV(), linear_model.PassiveAggressiveClassifier()]
vecs_to_test = [feature_extraction.text.CountVectorizer(), feature_extraction.text.TfidfVectorizer(),
                feature_extraction.text.HashingVectorizer()]

for k in range(len(classifiers_to_test)):
    current_classifier = classifiers_to_test[k]
    current_vectorizer = vecs_to_test[k]

    vectorize_text = current_vectorizer.fit_transform(learn_data.Text)
    current_classifier.fit(vectorize_text, learn_data.Category)

    vectorize_text = current_vectorizer.transform(test_data.Text)
    score = current_classifier.score(vectorize_text, test_data.Category)
    print(score)

    csv_arr = []
    for index, row in test_data.iterrows():
        text = row[0]
        answer = row[1]
        vectorize_text = current_vectorizer.transform([text])
        predict = current_classifier.predict(vectorize_text)[0]

        if predict == answer:
            result = "correct"
        else:
            result = "incorrect"
        csv_arr.append([len(csv_arr), text, answer, predict, result])

        with open(f"data/model_training/200_samples/test_score_{k}.csv", "w", newline = "", encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(["#", "Text", "Answer", "Prediction", "Result"])

            for row in csv_arr:
                writer.writerow(row)
    pp.dump(current_classifier, open(f"data/model_training/200_samples/{current_classifier}.pickle", "wb"))
    pp.dump(vectorize_text, open(f"data/model_training/200_samples/{current_vectorizer}.pickle", "wb"))
    print(f"Finished scoring {current_classifier} and {current_vectorizer}")

"""
Function to categorize a tweet using a vectorizer and classifier
def predict(message, vectorizer, classifier):
    vectorize_message = vectorizer.transform([message])
    predict = classifier.predict(vectorize_message)[0]
    return predict
"""

"""Categorize all tweets of the data set
preds_arr = []
for msg in complete_data.Text:
    res = predict(msg, current_vectorizer, current_classifier)
    preds_arr.append([msg, res])
"""