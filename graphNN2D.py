import pickle
from numpy import arange
from numpy import meshgrid
from numpy import zeros
import matplotlib.pyplot as plt
import sys

import Tkinter
import tkFileDialog


def load_dump(file_path, action=plt.show):
    X = arange(-9., 9., 0.2)
    Y = arange(-9., 9., 0.2)
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
    """
    
    Arg 1: The location of the NN to open
    Arg 2: A flag indicating whether to save the plot as a picture -s
    Arg 3: The filepath to save the plot
    
    """
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
        # Check arguments to find the control path
        SAVE        = '-s'
        nn_path     = sys.argv[1]   
        do_save     = sys.argv[2]
        img_path    = sys.argv[3]
        
        if do_save == SAVE:
            load_dump(nn_path, lambda: plt.savefig(img_path, bbox_inches='tight'))
        else:
            # Just display the image
            load_dump(nn_path)
        


