import theano
import theano.tensor as T


X = T.dmatrix('X')
y = T.dcol('y')

def Layer(X, n_in, n_out):

    w = theano.shared(np.random.randn(n_out,n_in), name='w')
    b = theano.shared(np.random.randn(1,n_out), name='b', broadcastable=(True,False))

    Xw = T.dot(X,T.transpose(w)) + b;
    sigmoid = 1/(1 + T.exp(-Xw));
    return sigmoid, w,b


hid1, w_h, b_h = Layer(X, 2,2)
out, w_o, b_o = Layer(hid1, 2,1)

cost = T.sum((y - out) ** 2)

updates = []
updates.append((w_o, w_o - 0.1 * T.grad(cost,w_o) ))
updates.append((b_o, b_o - 0.1 * T.grad(cost,b_o) ))
updates.append((w_h, w_h - 0.1 * T.grad(cost,w_h) ))
updates.append((b_h, b_h - 0.1 * T.grad(cost,b_h) ))

train = theano.function([X,y], [cost], updates= updates, allow_input_downcast=True)

pred = theano.function([X], [out], allow_input_downcast=True)

X_train = np.array([ [0,0], [0,1], [1,0], [1,1] ])
y_train = np.asarray([0,1,1,0]).reshape(-1,1)

for i in range(10000):
    train(X_train,y_train)

pred(X_train)
