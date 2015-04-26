#training parameters for support vector machines:
from svm import *

c = 10.65
#svm cost - if no c, over train because of the impact of the noise

gamma = 8.0
#inverse size of circle

kernel = RBF

#RBF = circle
#poly = polynomial, need to set degree instead of gamma


#include/import the libraries we need for loading CSV files -------------------------------------------------------------------------------------------------------------------


def loadCSV(filename,multiclass=True,outputs=1,separator=','):
    #read in all the lines
    f = open(filename).readlines()
    
    #start our datasets
    in_data = []
    out_data =[]
    
    #process the file
    for line in f:
        #remove whitespace and split according to separator character
        samples = line.strip(' \r\n').split(separator)
        
        #save input data
        in_data.append([float(i) for i in samples[:-outputs]])
        
        #save output data
        if multiclass:
            out_data.append(samples[-1])
        else:
            out_data.append([float(i) for i in samples[-outputs:]])
        
    #process multiclass encoding
    keys = []
    if multiclass:
        processed_out_data = []
        #get all the unique values for classes
        keys = []
        for d in out_data:
            if d not in keys:
                keys.append(d)
        keys.sort()
    
    #use libsvm's data container:
    return svm_problem([keys.index(i) for i in out_data],in_data),in_data,[keys.index(i) for i in out_data],keys
    


#train the SVM ---------------------------------------------------------------------------------------------------------------------------------------------------
#include the current path for library importing so that we can find the svm files
import sys
import os
path = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(path)

#set up more svm library stuff
from svmutil import svm_train,svm_predict
svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]

#load data
dataset,data,outputs,keys = loadCSV("smile.csv")

#set parameters
parameters = svm_parameter()
parameters.kernel_type = kernel
parameters.C = c
parameters.gamma = gamma

print "Training..."

#train
solver = svm_train(dataset,parameters)




#Save trained SVM 
#--------------------------------------------------------------------------------------------------------------------------------------------
from svmutil import svm_save_model
svm_save_model('mysvm',solver)
print "Complete."