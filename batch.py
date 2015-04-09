import sys
from Tkinter import Toplevel
import trainNN2D
import subprocess
import os
import threading
import signal
import atexit

try:
    from Tkinter import *
except ImportError:
    from tkinter import *


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.title('Tristans Trainer')
    geom = "704x464+508+323"
    root.geometry(geom)
    w = TTrainer (root)
    root.mainloop()

w = None
def create_New_Toplevel_1(root, param=None):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    w.title('Tristans Trainer')
    geom = "704x464+508+323"
    w.geometry(geom)
    w_win = TTrainer (w)
    test2_support.init(w, w_win, param)
    return w_win

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class InstanceStates:
    PENDING = 1
    RUNNING = 2
    STOPPED = 3
    
class Command:
    def __init__(self, script):
        self.args = []
        self.args.append(script)
    
    def add_arg(self, arg, wrap_quotes=False):
        arg=str(arg)
        if wrap_quotes:
            arg = "\'" + arg + "\'"
        self.args.append(arg)
    
    def add_args(self, args):
        """
        Add multiple arguments to a command
        Argument must be a list of tuples
        t[0] is the command,
        t[1] is a bool of whether it is to be wrapped in quotes or not
        """
        for arg in args:
            self.add_arg(arg[0], wrap_quotes=arg[1])
    
    def stringify(self):
        command_string = ""
        for arg in self.args:
            command_string += (arg + " ")
        return command_string
    
    def execute(self, pipeout=False):
        if pipeout:
            return subprocess.Popen(self.stringify(),
                                stdout=subprocess.PIPE,    
                                shell=True)
        return subprocess.Popen(self.stringify(),
                                shell=True)
       
def update(update, iter_u, error_u):
    print "update recieved"
    iter_u.delete(0, END)
    iter_u.insert(0, update[0])
    error_u.configure(text=update[1])

                         
def monitor(instance):
    # While the process isn't dead, update the boxes
    while instance._process.poll() is None:
        update = instance._process.stdout.readline()
        update = update.split(",")
        update[1][:-1]
        update = instance._process.stdout.readline().split(",")
        instance.iter_val = update[0]
        instance.error_val = update[1]

        # Instead of using event generation. Prepare a Q. And then update it using the after callback
        # in the main thread
        
        instance._owner._master.event_generate("<<"+str(instance._id)+"update>>", when="tail")
              
    
def dispatch_monitor(instance):
    worker = threading.Thread(target=monitor, 
                              kwargs={'instance': instance})
    worker.setDaemon(True)
    worker.start()
    
   
class Log:
    def __init__(self):
        self._log_text = ""
        top = Toplevel()
        top.withdraw()
        top.protocol("WM_DELETE_WINDOW", self.view_log)
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        top.title("Log")
        self._pane = top
        self._log_area = Text(top, borderwidth=2, relief="sunken")
        self._log_area.config(font=("consolas", 12), undo=True, wrap='word', state=DISABLED)
        self._log_area.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self._active = False
        
    def update(self, text):
        self._log_text += text +'\n';
        self._log_area.config(state=NORMAL)
        self._log_area.delete(1.0, END)
        self._log_area.insert(END, self._log_text)
        self._log_area.config(state=DISABLED)
        
    def view_log(self):
        """
        Toggle the logL window on or offs
        :return:
        """
        self._pane.withdraw() if self._active else self._pane.deiconify()
        self._active = not self._active
    
class TrainingInstance(Frame):
    def __init__(self, parent, owner, _id_):
        Frame.__init__(self, parent)
        self._entries = []
        self.Entry1 = Entry(self)
        self.Entry1.pack(side=LEFT)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(width=11)
        self._entries.append(self.Entry1)

        self.Entry2 = Entry(self)
        self.Entry2.pack(side=LEFT)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(width=11)
        self._entries.append(self.Entry2)

        self.Entry3 = Entry(self)
        self.Entry3.pack(side=LEFT)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(width=11)
        self._entries.append(self.Entry3)

        self.Entry4 = Entry(self)
        self.Entry4.pack(side=LEFT)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(width=11)
        self._entries.append(self.Entry4)

        self.Entry5 = Entry(self)
        self.Entry5.pack(side=LEFT)
        self.Entry5.configure(background="white")
        self.Entry5.configure(font="TkFixedFont")
        self.Entry5.configure(width=12)
        self._entries.append(self.Entry4)

        self.Entry6 = Entry(self)
        self.Entry6.pack(side=LEFT)
        self.Entry6.configure(background="white")
        self.Entry6.configure(font="TkFixedFont")
        self.Entry6.configure(width=11)
        self.Entry6.insert(0, trainNN2D.DEFAULT_HIDDEN)
        self._entries.append(self.Entry6)

        self.Entry7 = Entry(self)
        self.Entry7.pack(side=LEFT)
        self.Entry7.configure(background="white")
        self.Entry7.configure(font="TkFixedFont")
        self.Entry7.configure(width=11)
        self.Entry7.insert(0, trainNN2D.DEFAULT_OUT)
        self._entries.append(self.Entry7)

        self.Entry8 = Entry(self)
        self.Entry8.pack(side=LEFT)
        self.Entry8.configure(background="white")
        self.Entry8.configure(font="TkFixedFont")
        self.Entry8.configure(width=5)
        self._entries.append(self.Entry8)

        self.Label11 = Label(self)
        self.Label11.pack(side=LEFT)
        self.Label11.configure(text='''0''')
        self.Label11.configure(width=10)

        self.Button1 = Button(self)
        self.Button1.pack(side=LEFT)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''View''')
        self.Button1.configure(width=5)

        self.Button2 = Button(self)
        self.Button2.pack(side=LEFT)
        self.Button2.configure(activebackground="#d9090c")
        self.Button2.configure(activeforeground="white")
        self.Button2.configure(text='''Kill''')
        self.Button2.configure(width=5)
        self.Button2.configure(command=self.kill_instance)
        
        # Actual instance vars
        self.state = InstanceStates.PENDING
        self._owner = owner
        self._id = _id_
        self._run_dir = None
        self._process = None
        
        self.iter_val = None
        self.error_val = None

    def valid_params(self):
        # Eww
        valid = True
        for entry in self._entries:
            entry.configure(bg="white")
        if self.Entry1.get() is "" or float(self.Entry1.get()) <= float(0) or float(self.Entry1.get()) > float(1):
            self.Entry1.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in Lrate: set in [0->1]")
        if self.Entry2.get() is "" or float(self.Entry2.get()) <= float(0.9) or float(self.Entry2.get()) > float(1):
            self.Entry2.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in Ldecayset in [0.9->1]")
        if self.Entry3.get() is ""or float(self.Entry3.get()) <= float(0) or float(self.Entry3.get()) >= float(0.5):
            self.Entry3.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in momentum set in [0,0.5]")
            
        if self.Entry4.get() is "": #or str(self.Entry4.get()) != str(True) or str(self.Entry4.get()) != str(False):
            self._owner.log.update("val is " + str(self.Entry4.get()))            
            self.Entry4.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in B-learn. Must be True or False")
        if self.Entry5.get() is "" or " " in self.Entry5.get():
            self.Entry5.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in Hlayers. Must not contain spaces")
        if self.Entry6.get() is "":
            self.Entry6.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in HClass")
        if self.Entry7.get() is "":
            self.Entry7.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in OClass")
        if self.Entry8.get() is "" or self.Entry8.get() < 1:
            self.Entry8.configure(bg="orange")
            valid = valid and False
            self._owner.log.update("Error in Iterations. must be in [1->~]")
        
        return valid
        
    def _dispatch_process_monitor():
        """
        Updates the error and the iterations count for this pane
        """
    
    def dispatch_instance(self):
        """
        ARGUMENT FORMAT:
                Blank: Run as a standalone script
          ELSE
          
              ARG 1: The directory that this training run will take place in
              ARG 2: Learning Rate
              ARG 3: Learning Decay
              ARG 4: Momentum
              ARG 5: Batch Learning
              ARG 6: Hiddden Layers
              ARG 7: Hidden Class
              ARG 8: Output Class
              ARG 9: Iterations
        """  
        # Make a call to psubprocess in here

        if not self.valid_params():
            return False
        
        self.configure(bg='green')
        self.state = InstanceStates.RUNNING
        
        command = Command(trainNN2D.PYTHON_EXE)
        command.add_arg(trainNN2D.SCRIPT_NAME)
        self._run_dir = trainNN2D.RUN_MASTER_DIR + trainNN2D.now()
        command.add_arg(self._run_dir, wrap_quotes=True)
        args = []
        args.append((self.Entry1.get(), False))
        args.append((self.Entry2.get(), False))
        args.append((self.Entry3.get(), False))
        args.append((self.Entry4.get(), False))
        args.append((self.Entry5.get(), False))
        args.append((self.Entry6.get(), False))
        args.append((self.Entry7.get(), False))
        args.append((self.Entry8.get(), False))
        command.add_args(args)
        
        self._owner.log.update("Preparing to execute command: "+command.stringify())
        self._process = command.execute(pipeout=True)

        # Set up our event bindings

        # Set up a global event queue instead
        self._owner._master.bind_all("<<"+str(self._id)+"update>>", lambda: update((self.iter_val, self.error_val),
                                                                        self.Entry8,
                                                                        self.Label11))        
        
        dispatch_monitor(self)
        return True
        
        
    def open_view_pane(self):
        # Will create a TopLevel window that monitors a folder
        # Updates the pane with the latest image that is put in the folder        
        pass
    
    def kill_instance(self):
        if not self.state == InstanceStates.PENDING:
            self.configure(bg='red')
            self.state = InstanceStates.STOPPED
            self.Button2.configure(text='Close')
            self.Button2.configure(command=lambda: self._owner.delete_training_run(self._id))
            # Kill the subprocess here
            os.kill(self._process.pid, signal.SIGINT)

class TTrainer():
    def __init__(self, master=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        
        atexit.register(self.kill_children)
        
        self.created_trainers = 0
        self._master = master
        self.log = Log()

        self.Frame1 = Frame(master)
        self.Frame1.pack(side=TOP)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(width=685)

        self.Label1 = Label(self.Frame1)
        self.Label1.pack(side=LEFT)
        self.Label1.configure(cursor="fleur")
        self.Label1.configure(text='''L-Rate''')
        self.Label1.configure(width=11)

        self.Label2 = Label(self.Frame1)
        self.Label2.pack(side=LEFT)
        self.Label2.configure(cursor="fleur")
        self.Label2.configure(text='''L-Decay''')
        self.Label2.configure(width=11)

        self.Label3 = Label(self.Frame1)
        self.Label3.pack(side=LEFT)
        self.Label3.configure(text='''Momentum''')
        self.Label3.configure(width=11)

        self.Label4 = Label(self.Frame1)
        self.Label4.pack(side=LEFT)
        self.Label4.configure(text='''B-Learn''')
        self.Label4.configure(width=11)

        self.Label5 = Label(self.Frame1)
        self.Label5.pack(side=LEFT)
        self.Label5.configure(text='''H-Layers''')
        self.Label5.configure(width=12)

        self.Label6 = Label(self.Frame1)
        self.Label6.pack(side=LEFT)
        self.Label6.configure(text='''H-Class''')
        self.Label6.configure(width=11)

        self.Label7 = Label(self.Frame1)
        self.Label7.pack(side=LEFT)
        self.Label7.configure(text='''O-Class''')
        self.Label7.configure(width=11)

        self.Label9 = Label(self.Frame1)
        self.Label9.pack(side=LEFT)
        self.Label9.configure(text='''It''')
        self.Label9.configure(width=5)

        self.Label10 = Label(self.Frame1)
        self.Label10.pack(side=LEFT)
        self.Label10.configure(text='''Error''')
        self.Label10.configure(width=10)

        self.Button3 = Button(self.Frame1)
        self.Button3.pack(side=LEFT)
        self.Button3.configure(activebackground="#14d954")
        self.Button3.configure(text='''Run''')
        self.Button3.configure(width=20)
        self.Button3.configure(command=self.dispatch_new_run)
        
        self.Button4 = Button(self.Frame1)
        self.Button4.pack(side=LEFT)
        self.Button4.configure(activebackground="#14d954")
        self.Button4.configure(text='''Log''')
        self.Button4.configure(width=20)
        self.Button4.configure(command=self.log.view_log)

        # The frame in which training instances sit
        self.Frame2 = Frame(master)
        self.Frame2.pack()
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(width=685)
        
        self.available_instance = None
        self.training_instances ={}
        
        self._place_new_instance()
        
        
        
    def _place_new_instance(self):
        self.created_trainers+=1
        self.available_instance = TrainingInstance(self.Frame2, self, self.created_trainers)
        self.available_instance.pack()
        self.training_instances[self.created_trainers] = self.available_instance
        self.log.update("Created new training instance " + str(self.created_trainers))

    def dispatch_new_run(self):
        # Make a call to training instance . run or something like that
        # Do this for the currently pointed to training instance
        running = self.available_instance.dispatch_instance()
        if not running:
            return
        self._place_new_instance()
        self.log.update("Dispatched new training instance " + str(self.created_trainers))
    
    def delete_training_run(self, instance_id):
        self.training_instances[instance_id].destroy()
        del self.training_instances[instance_id]
        self.log.update("Deleted training instance " + str(instance_id))
        
    def kill_children():
        for id, trainer in self.training_instances.iteritems():
            os.kill(trainer._process.pid, signal.SIGTERM)



if __name__ == '__main__':
    vp_start_gui()