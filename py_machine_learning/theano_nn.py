import theano
import theano.tensor as T
import numpy as np
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt

features = 2

X_features, y_label = make_classification(n_samples=1000,n_features=features, n_redundant=0, n_informative=2,
                           random_state=31,n_clusters_per_class=1)




X = T.dmatrix('X')
y = T.dvector('y')

W = theano.shared(np.random.randn(features), name='W');
b = theano.shared(0.,  name = 'b')

s = 1 / (1 + T.exp(-T.dot(X,W) - b));

xent = -y * T.log(s) - (1-y)*T.log(1-s);
cost= xent.mean() + 0.01 * (W ** 2).sum()

gw,gb = T.grad(cost,[W,b])

train = theano.function(inputs=[X,y], outputs=[cost], updates=[(W,W - 0.1*gw),(b,b - 0.1*gb)]);

predict = theano.function([X], [s])

# Declare Theano symbolic variables
#X = T.dmatrix("X")
#y = T.dvector("y")
#W = theano.shared(np.random.randn(features), name="w")
#b = theano.shared(0., name="b")

## Construct Theano expression graph
#s= 1 / (1 + T.exp(-T.dot(X, W) - b))   # Probability that target = 1
#prediction = s > 0.5                    # The prediction thresholded
#xent = -y * T.log(s) - (1-y) * T.log(1-s) # Cross-entropy loss function
#cost = xent.mean() + 0.01 * (W ** 2).sum()# The cost to minimize
#gw, gb = T.grad(cost, [W, b])             # Compute the gradient of the cost
#                                          # w.r.t weight vector w and
#                                          # bias term b
#                                          # (we shall return to this in a
#                                          # following section of this tutorial)
## Compile
#train = theano.function(
#          inputs=[X,y],
#          outputs=[cost],
#          updates=[(W, W - 0.1 * gw), (b, b - 0.1 * gb)])
#predict = theano.function(inputs=[X], outputs=prediction)

costs = []
for i in range(10000):
    costs.append( train(X_features,y_label))

plt.plot(np.arange(1,10001), costs)
plt.xlim((0,500))
plt.ylim((0,1))
plt.show()









