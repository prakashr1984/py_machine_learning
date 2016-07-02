import numpy as np
import theano
import theano.tensor as T
import sklearn
import sklearn.datasets as datasets
from sklearn import cross_validation as cv
from sklearn.preprocessing import OneHotEncoder

digits = datasets.load_digits();

data = digits.data.astype(float) / 255
enc = OneHotEncoder();
target = enc.fit_transform(digits.target.reshape(-1,1)).toarray()

X_train, X_test, y_train, y_test = cv.train_test_split(data,target,test_size=0.2)


X = T.dmatrix('X')
y = T.dmatrix('y')

def HiddenLayer(X, n_in, n_out):

    w = theano.shared(np.random.randn(n_out,n_in), name='w')
    b = theano.shared(np.random.randn(1,n_out), name='b', broadcastable=(True,False))

    Xw = T.dot(X,T.transpose(w)) + b;
    return T.nnet.sigmoid(Xw), w,b

def SoftMaxLayer(X, n_in, n_out):
    w = theano.shared(np.random.randn(n_out,n_in), name='w')
    b = theano.shared(np.random.randn(1,n_out), name='b', broadcastable=(True,False))
    Xw = T.dot(X,T.transpose(w)) + b;
    return T.nnet.softmax(Xw), w,b

def sgd(cost,params, learning_rate=0.05):
    grads = T.grad(cost,params)

    updates = []
    for param,grad in zip(params,grads):
        updates.append((param, param - learning_rate * grad ))
    return updates

def model():
    hid1, w_h, b_h = HiddenLayer(X, 64,80)
    hid2, w_h2, b_h2 = HiddenLayer(hid1, 80,80)
    out, w_o, b_o = SoftMaxLayer(hid2, 80,10)
    cost = T.mean(T.nnet.categorical_crossentropy(out, y))
    updates = sgd(cost, [w_h, b_h, w_h2, b_h2, w_o, b_o])
    pred = T.argmax(out,axis=1)

    return cost, updates, pred

cost, updates, pred = model()

train = theano.function([X,y], cost, updates= updates, allow_input_downcast=True)

pred = theano.function([X], pred, allow_input_downcast=True)


cost =0
for i in range(10000):
    for start, end in zip(range(0, len(X_train), 128), range(128, len(X_train), 128)):
        cost = train(X_train[start:end], y_train[start:end])
    print cost
    print sklearn.metrics.accuracy_score(np.argmax(y_test, axis=1),pred(X_test))    
