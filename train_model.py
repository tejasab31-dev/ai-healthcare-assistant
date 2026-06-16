import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle


df = pd.read_csv("data/Training.csv")


X = df.drop("prognosis", axis=1)
y = df["prognosis"]
print(X.columns)


model = RandomForestClassifier()

pickle.dump(
    list(X.columns),
    open("model/symptom_list.pkl", "wb")
)

print("Total Symptoms:", len(X.columns))


print("Model trained successfully!")