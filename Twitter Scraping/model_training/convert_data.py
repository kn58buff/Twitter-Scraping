import pandas as pd
import pprint as pp
import regex as re
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

sample_tweets = pd.read_csv("data/sampled_tweets.csv")
all_text = ""
for text in tqdm(sample_tweets["1"]):
    all_text = all_text + " " + text

with open("model_training/sample_text.txt", "w", encoding = "utf-8") as f:
    for char in all_text:
        f.write(char)

#train_data = [("The Ambassador of Japan to Kenya H.E. Okaniwa Ken paid a courtesy call on PS @AmbMKamau.", {"entities": [(4, 13, "Position"), (18, 22, "Country"), (27, 31, "Country"), (78, 80, "Position"), (81, 86, "Person")]})]


pp.pprint(train_data)

nlp = spacy.blank("en")
db = DocBin()


for text, annot in tqdm(train_data):
    doc = nlp.make_doc(text)
    ents = []

    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label = label, alignment_mode = "contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents
    db.add(doc)

db.to_disk("./train.spacy")





nlp1 = spacy.load("model_training/output/model-best")
doc = nlp1(all_text)
spacy.displacy.render(doc, style = "ent", jupyter=True)
