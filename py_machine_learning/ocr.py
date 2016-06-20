import matplotlib.pyplot as plt
import sklearn.datasets as datasets
from sklearn import cross_validation, svm

digits = datasets.load_digits();

X_train,X_test,y_train,y_test = cross_validation.train_test_split(digits.data,digits.target,test_size=0.4)
clf = svm.SVC(gamma=0.0001, C=100);
clf.fit(X_train,y_train);

print 'Accuracy : ', clf.score(X_test,y_test);

plt.imshow(digits.images[-5], cmap = plt.cm.binary, interpolation='nearest');
plt.title('Predicted : ' + str( clf.predict(digits.data[-5])));
plt.show();




