import pickle
from numpy import arange
from numpy import meshgrid
from numpy import zeros
import matplotlib.pyplot as plt
import sys

import Tkinter
import tkFileDialog


def load_dump(file_path, action=plt.show):
    X = arange(-6., 6., 0.2)
    Y = arange(-6., 6., 0.2)
    X, Y = meshgrid(X, Y)
    Z = zeros(X.shape)

    model = pickle.load(open(file_path))

    for i in range(len(X)):
        for j in range(len(Y)):
            result = model.activate([X[i][j], Y[i][j]])
            if result[0] > result[1]:
                Z[i][j] = 0  # lower limit
            else:
                Z[i][j] = 100  # higher limit
    plt.imshow(Z)
    plt.gcf()
    plt.clim()
    plt.title("Neural Network Activation")

    action()
    plt.close()

if __name__ == '__main__':
    # The first argument is always the script
    if len(sys.argv) == 1:
    
        # This is the stand alone version
    
        root = Tkinter.Tk()
        root.withdraw()
    
        file_path = tkFileDialog.askopenfilename()
        s_filepath = file_path.split('/')
        print "Opening dump: " + s_filepath[-1]
        load_dump(file_path)
    
    else:
        # We are being called with a specific filename
    
        # we will need to parse the arguments and see if we also want to save a
        # pic
        # We will need to accept a location in which to do the pic save as well
        # savefig('foo.png', bbox_inches='tight')    this will need to be passed to
        # load
        # dump as the action
        print "Opening dump: " + sys.argv[1]
        load_dump(sys.argv[1])
