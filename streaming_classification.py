from river import datasets, stream, synth
from river import metrics, compose, preprocessing
from river import optim,evaluate
from river import tree
from sklearn.datasets import load_iris
import utils
gen = synth.Agrawal(classification_function=0, seed=42)
model = tree.HoeffdingTreeClassifier()

dataset = iter(gen.take(1000))
metric = metrics.Accuracy()
for x in range(1000):
    x,y = next(dataset)
    y_pred = model.predict_one(x)
    model.learn_one(x,y)
    metric.update(y,y_pred)
    print(metric)
    
model_dot = model.draw()
# print(type(model_dot))
# model_dot = pydot.graph_from_dot_data(str(model_dot))[0]
# print(model_dot['node'])

utils.save_graph_as_png(model_dot,'./img/sample_model.png')