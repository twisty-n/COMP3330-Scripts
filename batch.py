import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


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
    
class TrainingInstance(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.Entry1 = Entry(self)
        self.Entry1.pack(side=LEFT)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(width=11)

        self.Entry2 = Entry(self)
        self.Entry2.pack(side=LEFT)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(width=11)

        self.Entry3 = Entry(self)
        self.Entry3.pack(side=LEFT)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(width=11)

        self.Entry4 = Entry(self)
        self.Entry4.pack(side=LEFT)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(width=11)

        self.Entry5 = Entry(self)
        self.Entry5.pack(side=LEFT)
        self.Entry5.configure(background="white")
        self.Entry5.configure(font="TkFixedFont")
        self.Entry5.configure(width=12)

        self.Entry6 = Entry(self)
        self.Entry6.pack(side=LEFT)
        self.Entry6.configure(background="white")
        self.Entry6.configure(font="TkFixedFont")
        self.Entry6.configure(width=11)

        self.Entry7 = Entry(self)
        self.Entry7.pack(side=LEFT)
        self.Entry7.configure(background="white")
        self.Entry7.configure(font="TkFixedFont")
        self.Entry7.configure(width=11)

        self.Label8 = Label(self)
        self.Label8.pack(side=LEFT)
        self.Label8.configure(text='''Label''')
        self.Label8.configure(width=5)

        self.Label11 = Label(self)
        self.Label11.pack(side=LEFT)
        self.Label11.configure(text='''Label''')
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


class TTrainer():
    def __init__(self, master=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        
        self.created_trainers = 0


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
        self.Label7.configure(text='''L-Class''')
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
        self.Button3.configure(text='''New Run''')
        self.Button3.configure(width=87)
        self.Button3.configure(command=self.dispatch_new_run)

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
        self.available_instance = TrainingInstance(self.Frame2)
        self.available_instance.pack()
        self.training_instances[self.created_trainers] = self.available_instance

    def dispatch_new_run(self):
        # Make a call to training instance . run or something like that
        # Do this for the currently pointed to training instance
        self._place_new_instance()
        pass
    
    def delete_training_run(self, instance):
        self.training_instances[instance].destroy()
        del training_instances[instance]



if __name__ == '__main__':
    vp_start_gui()