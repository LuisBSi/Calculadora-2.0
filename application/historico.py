from tkinter import *

class Historico_Save:
    def write(txt:str):
        """Escreve no historico"""
        hfile = open("h_", "a")
        hfile.write("{}\n".format(txt))
    
    def get() -> str:
        """Retorna o historico"""
        hfile = open("h_", "r")
        hread = hfile.readlines()
        hread.reverse()
        return "".join(hread)

class Historico(object):
    def __init__(self, master:Tk, mainFrame:Frame, openButton:Button):
        self._oppened = False
        self.master = master
        self.mainFrame = mainFrame
        self.historicoFrame = Frame(master)
        self.openButton = openButton
        self.historicoText = Text(self.historicoFrame)
        self.historicoText.place(relheight=.87, relwidth=1, relx=0, rely=0.07)
        openButton.bind("<Button-1>", lambda _: self._change_state())
        
    def show(self):
        self.historicoFrame.place(relwidth=0.4, relheight=1, relx=0, rely=0)
        self.mainFrame.place(relwidth=0.6, relx=0.4)
        self.openButton.lift()
        self.openButton.configure(text="<")
        
        self.historicoText.configure(state=NORMAL)
        self.historicoText.delete("1.0", END)
        self.historicoText.insert("1.0", Historico_Save.get())
        self.historicoText.configure(state=DISABLED)
        
    def hide(self):
        self.historicoFrame.place(relwidth=0, relheight=0, relx=0, rely=0)
        self.mainFrame.place(relwidth=1, relx=0)
        self.openButton.configure(text=">")
        
    def _change_state(self):
        if self._oppened == False:
            self.show()
            self._oppened = True
        else:
            self.hide()
            self._oppened = False