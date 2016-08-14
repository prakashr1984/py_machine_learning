import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import mean_squared_error
import os

y = pd.read_csv(os.getcwd() + "\\FacialKeyPoint\\data\\training.csv")
y.dropna(inplace=True)
X = y.Image.apply(lambda x : np.fromstring(x,sep=' '))
X = np.stack(X.values, axis=0)
y.drop(['Image'], axis=1, inplace=True)


def plot_image(n):
    t = y.values[:,:-1].reshape(-1,15,2)
    plt.imshow(X[n].reshape(96,96), cmap=plt.cm.gray)
    plt.scatter(t[n,:,0],t[n,:,1])


def plot_16images(X,y,offset=0):
    t = y.reshape(-1,15,2)

    fig = plt.figure(figsize=(32,32))
    for i in range(64):
            ax = fig.add_subplot(8,8,i+1,xticks=[],yticks=[])
            ax.imshow(X[i+offset].reshape(96,96), cmap=plt.cm.gray)
            ax.scatter(t[i+offset,:,0],t[i+offset,:,1])


X = X.astype(float)/255
y = (y - 48)/48

#X_train,X_test,y_train,y_test = train_test_split(X,y.values)

#clf = DecisionTreeRegressor(max_depth=30)
#clf.fit(X_train,y_train)
#clf.score(X_test,y_test)
#y_pred = clf.predict(X_test)
#plot_16images(X_test,(y_pred * 48) + 48)
#cross_val_score(DecisionTreeRegressor(max_depth=30),X_train,y_train,scoring='mean_squared_error',n_jobs=-1)


#clf = LinearRegression()
#clf.fit(X_train,y_train)
#clf.score(X_test,y_test)
#y_pred = clf.predict(X_test)
#plot_16images(X_test,(y_pred * 48) + 48)

#clf = Lasso()
#clf.fit(X_train,y_train)
#clf.score(X_test,y_test)
#y_pred = clf.predict(X_test)
#plot_16images(X_test,(y_pred * 48) + 48)




clf = Lasso()
clf.fit(X,y)

test_df = pd.read_csv(os.getcwd() + "\\FacialKeyPoint\\data\\test.csv")
test_X = test_df.Image.apply(lambda x : np.fromstring(x,sep=' '))
test_X = np.stack(test_X.values, axis=0).astype(float)/255
y_pred = clf.predict(test_X)
y_pred = (y_pred * 48) + 48

test_lookup = pd.read_csv(os.getcwd() + "\\FacialKeyPoint\\data\\IdLookupTable.csv")
test_lookup.FeatureLoc = test_lookup.FeatureName.apply(lambda x: y.columns.get_loc(x))
test_lookup.Location = y_pred[test_lookup.ImageId - 1, test_lookup.FeatureLoc]


test_lookup[['RowId','Location']].to_csv(os.getcwd() + "\\FacialKeyPoint\\data\\submit.csv", index=False)
plot_16images(test_X, y_pred)