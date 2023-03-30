import pandas as pd

# Would like to compare the results of the two models
# CC_TFIDF is the classifier_vectorizer combination
CC_TFIDF = pd.read_csv("data/predictions/preds_with_best.csv")

# CLF_SVM is the SVM (support vector machine) results
CLF_SVM = pd.read_csv("data/predictions/preds_with_clfsvm.csv")
CLF_SVM.drop(columns=["index", "Date"], inplace=True)

# Check if both models have same size
if len(CC_TFIDF) == len(CLF_SVM):
    print(f"The results of the models both have a size of {len(CC_TFIDF)}")
else:
    print(f"The two models do not have the same size.\nCC_TFIDF has size {len(CC_TFIDF)}\nCLF_SVM has size {len(CLF_SVM)}")

# Extract tweets from both dataframes, where categories are either AWAY or RECEIVE
SUP = CC_TFIDF.loc[CC_TFIDF["Category"] != "UNRELATED"].reset_index(drop = True)
SUB = CLF_SVM.loc[CLF_SVM["Category"] != "UNRELATED"].reset_index(drop = True)
print(f"Size of bigger set (CC_TFIDF): {len(SUP)}\nSize of smaller set (CLF_SVM): {len(SUB)}")

# Check if tweets in SUB are part of SUP
comparison_df = (SUB.Text.isin(SUP.Text).astype(int)).to_frame(name="Matched")
matches = comparison_df.loc[comparison_df["Matched"] == 1]
print(len(matches))


merged_df = pd.merge(left=SUP, right=SUB, how="left")
merged_df.to_csv("data/validation/check.csv", index=False)
SUP.to_csv("data/validation/SUP.csv", index=False)
SUB.to_csv("data/validation/SUB.csv", index=False)
