from svmutil import svm_load_model,svm_predict
from svm import *
from numpy import arange,meshgrid,zeros
import matplotlib.pyplot as plt
from numpy import array

X = arange(-6.,6.,0.2)
Y = arange(-6.,6.,0.2)
X,Y = meshgrid(X,Y)
Z = zeros(X.shape)

model = svm_load_model('mysvm')


for i in range(len(X)):
    for j in range(len(Y)):
        #print svm_predict([0.],[[X[i][j],Y[i][j]]],model)[0][0]
        result = int(svm_predict([0.],[[X[i][j],Y[i][j]]],model,'-q')[0][0])
        if result == 0:
            Z[i][j] = 0 #lower limit
        else:
            Z[i][j] = 100 #higher limit
plt.imshow(Z)
plt.gcf()
plt.clim()
plt.title("SVM Activation")


plt.show()

