# include/import the libraries we need for loading CSV files
from pybrain.datasets import SupervisedDataSet
from pybrain.utilities import one_to_n
from pybrain.structure.modules import *
import pickle
import datetime
import threading
import subprocess
import os
import Tkinter
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
import matplotlib.pyplot as plt

# This must point to a python installed with all of the various required libs
PYTHON_EXE = '/home/tnewmann/anaconda/bin/python2.7'
RUN_MASTER_DIR = 'dumps/run:'
IMG_SUBDIR = '/img'
DUMP_SUBDIR = '/nn'


def now():
    """
    Returns the current date and time as a string
    """
    return str(datetime.datetime.now())


def loadCSV(filename, multiclass=True, outputs=1, separator=','):
    # read in all the lines
    f = open(filename).readlines()

    # start our datasets
    in_data = []
    out_data = []

    # process the file
    for line in f:
        # remove whitespace and split according to separator character
        samples = line.strip(' \r\n').split(separator)

        # save input data
        in_data.append([float(i) for i in samples[:-outputs]])

        # save output data
        if multiclass:
            out_data.append(samples[-1])
        else:
            out_data.append([float(i) for i in samples[-outputs:]])

    processed_out_data = out_data

    # process multiclass encoding
    if multiclass:
        processed_out_data = []
        # get all the unique values for classes
        keys = []
        for d in out_data:
            if d not in keys:
                keys.append(d)
        keys.sort()
        # encode all data
        for d in out_data:
            processed_out_data.append(one_to_n(keys.index(d), len(keys)))

    # create the dataset
    dataset = SupervisedDataSet(len(in_data[0]), len(processed_out_data[0]))
    for i in xrange(len(out_data)):
        dataset.addSample(in_data[i], processed_out_data[i])

    # return the keys if we have
    if multiclass:
        return dataset, keys  # a multiclass classifier
    else:
        return dataset


# train the neural network

def error_plot(error_list):
    import matplotlib.pyplot as plot
    plot.plot(error_list, 'r')
    plot.ylabel("Training Error")
    plot.xlabel("Training Steps")
    plot.show()


def dump(neural_net, files_made, dump_dir, print_params=False, params=None):
    """
    Dumps the neural network using pickle
    @neural_net: The pyBrain neuralnet to dump
    @files_made: A list which will hold the filenames of the dump files
    @print_params: Print the paramaters related to the dump
    @params: A hash of the params that will be used for the dump
    """
    dt = now()
    pk_d = dump_dir + '/NN' + dt + '.pkl'
    files_made.append(pk_d)
    pickle.dump(neural_net, open(pk_d, 'wb'))
    # Also allow paramater printout
    if print_params:
        param_file = open(dump_dir + '/params/PARAM_DUMP_'+dt+'.txt', "w")
        for key, value in params.iteritems():
            param_file.write(key+value+'\n')
        param_file.close()


def print_activation(file_name):
    """
    Prints the activation graph of the neural network
    """
    if file_name == 'herp':  # Hax cause im a lazy bastard
        return
    print "Printing activation of file: " + file_name
    subprocess.Popen(PYTHON_EXE+' graphNN2D.py \'' + file_name + '\'',
                                shell=True)


# Set up an action window thread
def create_window(nn, error, files_list, dump_dir):
    """
    Create a window to launch our commands
    """
    
    win = Tkinter.Tk()
    printButton = Tkinter.Button(win, text="Perform Dump",\
                                 command=lambda: dump(nn, files_list, dump_dir))
    printButton.pack()
    errorButton = Tkinter.Button(win, text="View most recent dump",\
                                 command=lambda: print_activation(files_list[-1]))
    errorButton.pack()
    print "Creating options pane!"
    win.mainloop()


def save_activation(files_made, img_path, dumper, defer=False):
    # TODO: Fix this up !
    """
    Saves a neural network activation plot as a picture
    """
    from graphNN2D import load_dump as loader
    if dumper is None:
        print "Error no Dumper specified!"
        return
    dumper()
    img_name = img_path + '/AP-'+now()+'.png'
    if not defer:
        loader(files_made[-1], lambda: plt.savefig(img_name, 
                                      bbox_inches='tight'))
    else:
        shell_string = PYTHON_EXE + ' graphNN2D.py \'' + files_made[-1] + '\''
        shell_string += ' -s '
        shell_string += '\''+img_name+'\''
        subprocess.Popen(shell_string, shell=True)
                                       
    
def create_interface(nn, error, files_made, dump_path):
    """
    Create a window that allows the printing and viewing of dumps
    during traing execution
    """
    worker = threading.Thread(target=create_window, kwargs={'nn': nn,
                              'error': error,
                              'files_list': files_made,
                              'dump_dir': dump_path})
    worker.setDaemon(True)
    worker.start()


def train(activation_stream=False, print_iters=0, path=None):
    """
    Trains a neural network
    """
    # training parameters for neural networks:
    learning_rate = 0.1                 # set in [0,1]
    learning_decay = 1                  # try 0.999, set in [0.9,1]
    momentum = 0.05                     # set in [0,0.5]
    batch_learning = False              # set to learn in batches
    validation_proportion = 0           # set in [0,0.5]
    hidden_layers = [30, 10, 5]         # no of neurons in each hidden layer
    iterations = 800                     # used only if vproportion is 0
    hidden_class = SigmoidLayer
    out_class = LinearLayer

    stream = activation_stream
    print_val = print_iters
    
    if path is None:
        run_path = RUN_MASTER_DIR + now()
    else:
        run_path = path
    
    img_path = run_path + IMG_SUBDIR
    dump_path = run_path + DUMP_SUBDIR
    os.mkdir(run_path)
    os.mkdir(img_path)
    os.mkdir(dump_path)
    os.mkdir(dump_path+'/params')

    params = {
        'Learning Rate: ':          str(learning_rate),
        'Learning Decay:':          str(learning_decay),
        'Momentum: ':                 str(momentum),
        'Batch Learning':           str(batch_learning),
        'Validation Proportion: ':  str(validation_proportion),
        'Hidden Layers ':           str(hidden_layers),
        'Iterations: ':             str(iterations),
        'Hidden Class: ':           str(hidden_class).split('.')[-1],
        'Out Class: ':              str(out_class).split('.')[-1]
    }

    data, keys = loadCSV("smile.csv")
    nn = buildNetwork(*([data.indim]+hidden_layers+[data.outdim]),
                      outclass=out_class, hiddenclass=hidden_class)

    trainer = BackpropTrainer(nn, data, learningrate=learning_rate,
                              momentum=momentum,
                              lrdecay=learning_decay,
                              batchlearning=batch_learning)

    error = []
    validation_error = []
    files_made = ['herp']

    # Create this training runs run directory


    #create_interface(nn, error, files_made, dump_path)
    

    print "Beginning Training run..."

    try:
        if validation_proportion == 0. or validation_proportion == 0:

            for i in xrange(iterations):
                error_val = trainer.train()
                print "Iteration " + str(i) + "\tError: " + str(error_val)
                error.append(error_val)

                # check which iteration we're up to, dump the network
                if stream and (i % print_val == 0):
                    save_activation(files_made, 
                                    img_path,
                                    lambda: dump(nn, files_made, dump_path),
                                    True)
        else:
            error, validation_error = trainer.trainUntilConvergence(
                                validationProportion=validation_proportion)

        print "Training Complete.... Printing Error Plot"
    except:
        print "Exception occured, performing emergency Dump!"
        # print "Error Information: " + str(e)
    finally:
        dump(nn, files_made, dump_path, True, params)
        error_plot(error)

# Treat this as a stand alone program
if __name__ == "__main__":
    """
    ARGUMENT FORMAT:
            Blank: Run as a standalone script
      ELSE
      
          ARG 1: The directory that this training one will take place in
          ARG 2: Learning Rate
          ARG 3: Learning Decay
          ARG 4: Momentum
          ARG 5: Batch Learning
          ARG 6: Hiddden Layers
          ARG 7: Hidden Class
          ARG 8: Output Class
    """
    if len(sys.argv) == 1:
        train(True, 50)
    else:
        # Being called as part of a batch routine, so we need to process the
        # args
        pass