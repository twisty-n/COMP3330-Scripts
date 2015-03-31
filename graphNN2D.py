import pickle
from numpy import arange,meshgrid,zeros
import matplotlib.pyplot as plt
import sys

import Tkinter, tkFileDialog



def open_dump(file_path):
    X = arange(-6.,6.,0.2)
    Y = arange(-6.,6.,0.2)
    X,Y = meshgrid(X,Y)
    Z = zeros(X.shape)
    
    model = pickle.load(open(file_path))
    
    for i in range(len(X)):
        for j in range(len(Y)):
            result = model.activate([X[i][j],Y[i][j]])
            if result[0] > result[1]:
                Z[i][j] = 0 #lower limit
            else:
                Z[i][j] = 100 #higher limit
    plt.imshow(Z)
    plt.gcf()
    plt.clim()
    plt.title("Neural Network Activation")
    
    plt.show()

# The first argument is always the script
if len(sys.argv) == 1:

    root = Tkinter.Tk()
    root.withdraw()
    
    file_path = tkFileDialog.askopenfilename()
    s_filepath = file_path.split('/')
    print "Opening dump: " + s_filepath[-1]
    open_dump(file_path)
    
else:
    #We are being called with a specific filename
    print "Opening dump: " + sys.argv[1]
    open_dump(sys.argv[1])



