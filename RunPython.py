import os, json, sys
import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog

class GuiError:
    def __init__(self, text):
        self.gui = tk.Tk()
        self.gui.title('Internal Error')
        self.gui.columnconfigure(0, weight=1)
        self.gui.rowconfigure(0, weight=1)
        self.frame = ttk.Frame(self.gui)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
        self.text = ttk.Label(self.frame, text=text)
        self.text.grid(row=0, column=0, padx=5, pady=5)
        self.gui.mainloop()

class Main:
    def __init__(self):
        self.myGUI=tk.Tk()
        self.myGUI.title('Run File Python')
        self.myGUI.minsize(width=400, height=50)
        self.myGUI.resizable(False, False)
        self.myGUI.columnconfigure(0, weight=1)
        self.myGUI.rowconfigure(0, weight=1)
        self.myGUI.iconphoto(False, PhotoImage(file='logo.png'))

        #Frame
        self.GUI=ttk.Frame(self.myGUI)
        self.GUI.grid(column=0, row=0, padx=5, pady=5)

        #label
        self.Label=[None, None]
        self.Label[0]=tk.Label(self.GUI, text="Lokasi :")
        self.Label[0].grid(column=0, row=0, sticky=tk.E)
        self.Label[1]=tk.Label(self.GUI, text="File   :")
        self.Label[1].grid(column=0, row=1, sticky=tk.E)

        #Entry / input
        self.Lokasi, self.Nama= [tk.StringVar() for a in range(2)]

        ##input lokasi
        Var_Lokasi=tk.Entry(self.GUI, textvariable=self.Lokasi, width=80)
        Var_Lokasi.grid(column=1, row=0, columnspan=6, sticky=tk.W)
        self.readDefault(Var_Lokasi)

        ##input nama
        Var_Nama=tk.Entry(self.GUI, textvariable=self.Nama, width=60)
        Var_Nama.grid(column=1, row=1, columnspan=4, sticky=tk.W)
        
        #Start
        ## Browse
        openFolder=tk.Button(self.GUI, text="Browse", command=self.openFolder, width=14)
        openFolder.grid(column=5, row=1, columnspan=1, sticky=tk.E)

        ## buka CMD
        openCMD=tk.Button(self.GUI, text="Open Python", command=self.openCMD, width=18)
        openCMD.grid(column=0, row=2, columnspan=2, sticky=tk.W)

        ## tanpa CMD
        start=tk.Button(self.GUI, text="Start", command=self.START, width=18)
        start.grid(column=2, row=2, columnspan=2)
        
        ## dengan CMD
        startCmd=tk.Button(self.GUI, text="Start dgn Debug", command=self.STARTcmd, width=26)
        startCmd.grid(column=4, row=2, columnspan=2, sticky=tk.E)

        #Var_Nama.bind("<Return>", self.START)
        Var_Nama.bind("<Return>", self.STARTcmd)
        Var_Nama.focus()
        #Var_Lokasi.focus()
        self.Input=[Var_Lokasi, Var_Nama]
        
        self.myGUI.protocol('WM_DELETE_WINDOW', self.Quit)
        self.myGUI.bind('<Control-q>', self.Quit)
        self.myGUI.mainloop()
       
    def Quit(self, *arg):
        self.myGUI.destroy()
 
    def readDefault(self, data):
        file={"lokasi" : ""}
        file['lokasi']=os.getcwd()
        try:
            with open("RunPython.json") as Run:
                file=json.load(Run)
                Run.close()
        except Exception:
            with open("RunPython.json", "w") as Run:
                json.dump(file, Run)
                Run.close()
        nama=file['lokasi']
        data.insert(0, nama)

    def writeDefault(self, data):
        file, name=[None for a in range(2)]

        name=os.getcwd()
        if data != name:
            name=data
        try:
            with open("RunPython.json") as Run:
                file=json.load(Run)
                file["lokasi"]=data
                Run.close()
            with open("RunPython.json", "w") as Run:
                json.dump(file, Run)
                Run.close()
        except Exception:
            pass

    def openFolder(self):
        nama=filedialog.askopenfilename(filetypes=(("Python (*.py)", "*.py"),
                                                     ("All files", "*.*")))
        
        if nama == "":
            return
        a=nama.find("/")
        b=0
        while True:
            if a < 0:
                a=b
                break
            b=a
            a=nama.find("/", a+1)
        lokasi=nama[:a+1]
        nama=nama[a+1:]
        self.Input[0].delete(0, tk.END)
        self.Input[0].insert(0, lokasi)
        self.Input[1].delete(0, tk.END)
        self.Input[1].insert(0, nama)

    def checkData(self, lokasi, nama):
        Error=False
        if lokasi == "":
            self.Label[0].configure(foreground="red")
            Error=True
        else:
            self.Label[0].configure(foreground="black")
            
        if nama == "":
            self.Label[1].configure(foreground="red")
            Error=True
        else:
            self.Label[1].configure(foreground="black")

        return Error

    def openCMD(self):
        os.system("start python")

    def START(self, event=None):
        Lokasi=self.Lokasi.get()
        Nama=self.Nama.get()
        self.writeDefault(Lokasi)

        if self.checkData(Lokasi, Nama):
            return
        else:
            if Nama[-3:] not in ".py":
                Nama += ".py"

            Nama=Lokasi+Nama
            os.system('start pythonw ' + Nama)

    def STARTcmd(self, event=None):
        Lokasi=self.Lokasi.get()
        Nama=self.Nama.get()
        self.writeDefault(Lokasi)
        
        if self.checkData(Lokasi, Nama):
            return
        else:
            if Nama[-3:] not in ".py":
                Nama += ".py"

            Nama=Lokasi+Nama
            os.system('start cmd /k python ' + Nama)

def main():
    try:
        Main()
    except Exception as e:
        GuiError(e)

if __name__ == '__main__':
    main()