import numpy as np
import theano
import theano.tensor as T
import sklearn
import sklearn.datasets as datasets
from sklearn import cross_validation as cv
import matplotlib.pyplot as plt
import sys

digits = datasets.load_digits();

data = (digits.data.astype(float))/256
target = (np.arange(10) == digits.target[:,None]).astype(theano.config.floatX)

X_train, X_test, y_train, y_test = cv.train_test_split(data,target,test_size=0.2)


def HiddenLayer(X, n_in, n_out):

    w = theano.shared(np.random.randn(n_in,n_out), name='w')
    b = theano.shared(np.random.randn(1,n_out), name='b', broadcastable=(True,False))

    Xw = T.dot(X,w) + b;
    return T.nnet.relu(Xw, alpha=0.01), w,b

def SoftMaxLayer(X, n_in, n_out):
    w = theano.shared(np.random.randn(n_in, n_out), name='w')
    b = theano.shared(np.random.randn(1,n_out), name='b', broadcastable=(True,False))
    Xw = T.dot(X,w) + b;
    return T.nnet.softmax(Xw), w,b

def sgd(cost,params, learning_rate=0.05):
    grads = T.grad(cost,params)

    updates = []
    for param,grad in zip(params,grads):
        updates.append((param, param - learning_rate * grad ))
    return updates

def model(lr=0.05, L2_Reg=0.001):

    X = T.dmatrix('X')
    y = T.dmatrix('y')

    hid1, w_h, b_h = HiddenLayer(X, 64,80)
    hid2, w_h2, b_h2 = HiddenLayer(hid1, 80,80)
    out, w_o, b_o = SoftMaxLayer(hid2, 80,10)
    cost = T.mean(T.nnet.categorical_crossentropy(out, y)) + (L2_Reg * ( T.sum(T.sqr(w_h)) +T.sum(T.sqr(w_h2)) + T.sum(T.sqr(w_o)) ))
    params = [w_h, b_h, w_h2, b_h2, w_o, b_o]
    updates = sgd(cost, params)
    pred = T.argmax(out,axis=1)

    train = theano.function([X,y], cost, updates= updates, allow_input_downcast=True)

    pred = theano.function([X], pred, allow_input_downcast=True)

    return train, pred, params

train, pred, params = model()


costs = []
for i in range(1000):
    for start, end in zip(range(0, len(X_train), 128), range(128, len(X_train), 128)):
        cost = train(X_train[start:end], y_train[start:end])
    print 'Cost: {0} , Accuracy: {1}'.format(cost, sklearn.metrics.accuracy_score(np.argmax(y_test, axis=1),pred(X_test)))
    sys.stdout.flush()
    costs.append(cost)