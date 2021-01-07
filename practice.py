from river import datasets
from river import linear_model

dataset = datasets.Phishing()
model = linear_model.LogisticRegression()

for x, y in dataset:
    # y_pred = model.predict_proba_one(x)
    model.learn_one(x,y)
    y_pred = model.predict_one(x)
    print(y_pred)