from river import datasets, stream
from river import linear_model
from river import metrics, compose, preprocessing

metric = metrics.ROCAUC()
roclist =[]
for x, y in dataset:
    # y_pred = model.predict_proba_one(x)
    model.learn_one(x,y)
    y_pred = model.predict_one(x)
    metric.update(y, y_pred)
    print(metric.get())
    roclist.append(metric.get())
plt.plot(roclist)
plt.show()