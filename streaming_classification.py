from river import datasets, stream
from river import linear_model
from river import metrics, compose, preprocessing
from river import optim,evaluate
from river import tree

X_y = datasets.Bikes()

model = compose.Select('clouds', 'humidity', 'pressure', 'temperature', 'wind')
model |= preprocessing.StandardScaler()
model |= tree.BaseHoeffdingTree()

metric = metrics.MAE()

evaluate.progressive_val_score(X_y, model, metric, print_every=20_000)

