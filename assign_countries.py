import tkinter as tk
import tkinter.ttk as ttk
import queue
import pandas as pd
import os
pwd = "D:/Dev/ForeignLeadersProject"

if os.path.isfile(pwd + "/data/labeled_tweets/updated_labeled_data.csv"):
    data = pd.read_csv(pwd + "/data/labeled_tweets/updated_labeled_data.csv")
else:
    data = pd.read_csv(pwd + "/data/labeled_tweets/related_data.csv")

tweets = queue.Queue()
for t in data.loc[data["Country"].isnull()]["Text"]:
    tweets.put(t)

data = data.where(pd.notnull(data), None)


def num_completed():
    k = len(data)
    for i in range(len(data)):
        if pd.isna(data.at[i, "Country"]):
            k -= 1
    return k

completed = num_completed()

responses = queue.Queue()

window = tk.Tk()
window.geometry("900x500")
counter_frame = tk.Frame(master=window, width=150, height=100)
tweet_frame = tk.Frame(master=window, width=600, height=500)
input_frame = tk.Frame(master = window, width=300, height=100)
buttons_frame = tk.Frame(master=window, width=200, height=150)
save_frame = tk.Frame(master=window, width=200, height=120)

counter_frame.place(x=0, y=0)
tweet_frame.place(x=150, y=50)
input_frame.place(x=300, y=260)
buttons_frame.place(x=500, y=260)
save_frame.place(x=750, y=400)

txt_counter = ttk.Label(master=counter_frame, text="Completed:")
txt_counter.place(x=0, y=0)

txt_dynamic_counter = ttk.Label(master=counter_frame, text=f"{completed}")
txt_dynamic_counter.place(x=4, y=20)

size = len(data)
static_max = ttk.Label(master=counter_frame, text=f"/ {size}")
static_max.place(x=30, y=20)

txt_tweet = tk.Label(master=tweet_frame, text=f"{tweets.get()}", wraplength=500, justify="left", font=16)
txt_tweet.place(x=75, y=0)


def increase_counter():
    curr_value = int(txt_dynamic_counter["text"])
    txt_dynamic_counter["text"] = f"{curr_value + 1}"


def update_tweet():
    curr_tweet = txt_tweet["text"]
    curr_value = int(txt_dynamic_counter["text"])
    if (curr_value) != size:
        txt_tweet["text"] = str(tweets.get())
    elif (curr_value) == size:
        txt_tweet["text"] = "All done, saving data"
        save_data()


def handle_input():
    country = T.get("1.0", "end")
    responses.put(country)
    T.delete("1.0","end")
    increase_counter()
    update_tweet()


def save_data():
    k = num_completed()
    for i in range(k,len(data)):
        if pd.isna(data.at[i, "Country"]) and responses.empty() == False:
            print(data.at[k, "Country"])
            data.at[k, "Country"] = str(responses.get())
        k += 1
    data.to_csv(pwd + "/data/labeled_tweets/updated_labeled_data.csv", index=False)

T = tk.Text(master=input_frame, width=100, height=50)
btn_submit = ttk.Button(master=buttons_frame, text="Add", command=handle_input)
T.place(x = 0, y = 0)
btn_submit.place(x=100, y=100)
window.bind("<Return>", lambda event:handle_input())
btn_save_data = ttk.Button(master=save_frame, text="Save Data", command=save_data)
btn_save_data.pack()

window.mainloop()
