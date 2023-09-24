from tkinter import DISABLED, END, Menu, Tk, FALSE, Button, Entry, ttk, Frame, Menu
from application.calc import Calc
from application.historico import *
from json import load

class WidgetList:
    """Responsavel por posicionar os Widgets em forma de tabela"""
    def __init__(self, rows:int, cols:int, relwidth:float, relheight:float, relx:float, rely:float):
        #Variaveis
        self._rows = rows
        self._cols = cols
        self.rw = relwidth
        self.rh = relheight
        self.rx = relx
        self.ry = rely
        #self._widgets guarda os widgets adicionados na classe que posteriormente serao posicionados na tela
        self._widgets = []
    def add(self, tkinter_widget, text:str, cnf:dict) -> Button:
        """Adiciona um novo Widget a classe"""
        tkinter_widget.configure(text=text, cnf=cnf)
        wlist = [tkinter_widget]
        self._widgets.append(wlist)
        return tkinter_widget
    def posicionar_objetos(self):
        """Adiciona os Widgets a Tela em forma de Tabela"""
        index = 0
        for row in range(0, self._rows, 1):
            for col in range(0, self._cols, 1):
                if index >= len(self._widgets):
                    break
                else:
                    wlist = self._widgets[index]
                    widget = wlist[0]
                    widget.place(relx=self.rx+((self.rw/self._cols)*col), rely=self.ry+((self.rh/self._rows)*row), relwidth=self.rw/self._cols, relheight=self.rh/self._rows)
                index+=1

class Calculadora:
    """Classe principal da Calculadora"""
    def __init__(self, master:Tk, json:dict):
        self.settings = json # Guarda as configuracoes do arquivo cfg.json
        #Tela Master
        self.mainFrame = Frame(master)
        self.mainFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.mainFrame.configure(cnf=self.settings["cnf"]["mainFrame"])
        #Menu
        self.menu = Button(master)
        self.menu.configure(text=">", cnf=self.settings["cnf"]["menu"])
        self.menu.place(relx=0, rely=0, relwidth=0.1, relheight=0.06)
        #Historico
        self.historico = Historico(master, self.mainFrame, self.menu)
        self.historico.historicoFrame.configure(cnf=self.settings["cnf"]["historicoFrame"])
        self.historico.historicoText.configure(cnf=self.settings["cnf"]["historicoText"])
        #MainEntry
        self.mainEntry = Entry(self.mainFrame, justify="right")
        self.mainEntry.place(relwidth=1.98, relheight=0.14, relx=-1, rely=0)
        self.mainEntry.configure(cnf=self.settings["cnf"]["main_entry"])
        self.mainEntry.bind("<FocusIn>", lambda _, txt="main": self.aoClicarNoEntry(txt))
        self.mainEntry.insert(0, "0")
        #ENTRY 2
        self.secEntry = Entry(self.mainFrame, justify="right")
        self.secEntry.place(relwidth=1.94, relheight=0.05, relx=-1, rely=0)
        self.secEntry.configure(cnf=self.settings["cnf"]["sec_entry"])
        self.secEntry.bind("<FocusIn>", lambda _, txt="sec": self.aoClicarNoEntry(txt))
        #Botoes
        self._create_buttons()
        #Loop
        master.mainloop()

    @property
    def mainEntryText(self) -> str:
        return self.mainEntry.get()
    
    @property
    def secEntryText(self) -> str:
        return self.secEntry.get()

    def aoClicarNoEntry(self, txt):
        if txt == "main":
            txt = self.mainEntry.get()
        else:
            txt = self.secEntry.get()
        print("O texto ",txt," foi copiado para Area de Transferencia!")
        self.mainFrame.clipboard_clear()
        self.mainFrame.clipboard_append(txt)
        self.mainFrame.update()
        self.mainFrame.focus()

    def _replace_entry(self, text:str) -> bool:
        self.mainEntry.delete(0, END)
        self.mainEntry.insert(0, text)
        return True
    
    def _write_entry(self, text:str) -> bool:
        txt = self.mainEntryText
        if text not in (".", "+", "-", "*", "%", "/", "**") and txt == "0" or txt == 0:
            txt = ""
        self.mainEntry.delete(0, END)
        self.mainEntry.insert(0, f"{txt}{text}")
        return True

    def _replace_sec_entry(self, text:str) -> bool:
        self.secEntry.delete(0, END)
        self.secEntry.insert(0, text)
        return True

    def _bind(self, btn:str):
        if btn == "C":
            self._replace_entry("0")
            self._replace_sec_entry("")
        elif btn == "=":
            anterior = self.mainEntryText
            res = Calc.calcular(self.mainEntryText)
            if res:
                self._replace_entry(res)
                self._replace_sec_entry(anterior)
                Historico_Save.write("{}= {}".format(anterior, res))
        elif btn == "<":
            self._replace_sec_entry("")
            txt = self.mainEntryText
            txt = txt[:-1] != "" and txt[:-1] or "0"
            self._replace_entry(txt)
        elif btn == ".":
            txt = self.mainEntryText
            if txt[-1] in ("0","1","2","3","4","5","6","7","8","9"):
                self._write_entry(".")
            else:
                self._write_entry("0.")
        else:
            self._write_entry(btn)

    def _create_buttons(self):
        rows = self.settings["rows"]
        cols = self.settings["cols"]
        wlist = WidgetList(rows, cols, 1, 0.85, 0, 0.15)

        #WIDGETS
        btn_c = wlist.add(Button(self.mainFrame), "C", self.settings["cnf"]["btn"])
        btn_elev = wlist.add(Button(self.mainFrame), "^", self.settings["cnf"]["btn"])
        btn_excluir = wlist.add(Button(self.mainFrame), "<", self.settings["cnf"]["btn"])
        btn_por = wlist.add(Button(self.mainFrame), "%", self.settings["cnf"]["btn"])
        btn_1 = wlist.add(Button(self.mainFrame), 1, self.settings["cnf"]["0_9_btn"])
        btn_2 = wlist.add(Button(self.mainFrame), 2, self.settings["cnf"]["0_9_btn"])
        btn_3 = wlist.add(Button(self.mainFrame), 3, self.settings["cnf"]["0_9_btn"])
        btn_ma = wlist.add(Button(self.mainFrame), "+", self.settings["cnf"]["btn"])
        btn_4 = wlist.add(Button(self.mainFrame), 4, self.settings["cnf"]["0_9_btn"])
        btn_5 = wlist.add(Button(self.mainFrame), 5, self.settings["cnf"]["0_9_btn"])
        btn_6 = wlist.add(Button(self.mainFrame), 6, self.settings["cnf"]["0_9_btn"])
        btn_me = wlist.add(Button(self.mainFrame), "-", self.settings["cnf"]["btn"])
        btn_7 = wlist.add(Button(self.mainFrame), 7, self.settings["cnf"]["0_9_btn"])
        btn_8 = wlist.add(Button(self.mainFrame), 8, self.settings["cnf"]["0_9_btn"])
        btn_9 = wlist.add(Button(self.mainFrame), 9, self.settings["cnf"]["0_9_btn"])
        btn_ve = wlist.add(Button(self.mainFrame), "*", self.settings["cnf"]["btn"])
        btn_colchet1 = wlist.add(Button(self.mainFrame), "(", self.settings["cnf"]["btn"])
        btn_0 = wlist.add(Button(self.mainFrame), 0, self.settings["cnf"]["btn"])
        btn_colchet2 = wlist.add(Button(self.mainFrame), ")", self.settings["cnf"]["btn"])
        btn_di = wlist.add(Button(self.mainFrame), "/", self.settings["cnf"]["btn"])
        wlist.add(Button(self.mainFrame), " ", self.settings["cnf"]["btn"])
        btn_vi = wlist.add(Button(self.mainFrame), ".", self.settings["cnf"]["btn"])
        wlist.add(Button(self.mainFrame), " ", self.settings["cnf"]["btn"])
        btn_ig = wlist.add(Button(self.mainFrame), "=", self.settings["cnf"]["btn"])

        #EVENTOS
        btn_c.bind("<Button-1>", lambda _, btn="C": self._bind(btn))
        btn_por.bind("<Button-1>", lambda _, btn="%": self._bind(btn))
        btn_elev.bind("<Button-1>", lambda _, btn="**": self._bind(btn))
        btn_excluir.bind("<Button-1>", lambda _, btn="<": self._bind(btn))
        btn_1.bind("<Button-1>", lambda _, btn=1: self._bind(btn))
        btn_2.bind("<Button-1>", lambda _, btn=2: self._bind(btn))
        btn_3.bind("<Button-1>", lambda _, btn=3: self._bind(btn))
        btn_ma.bind("<Button-1>", lambda _, btn="+": self._bind(btn))
        btn_4.bind("<Button-1>", lambda _, btn=4: self._bind(btn))
        btn_5.bind("<Button-1>", lambda _, btn=5: self._bind(btn))
        btn_6.bind("<Button-1>", lambda _, btn=6: self._bind(btn))
        btn_me.bind("<Button-1>", lambda _, btn="-": self._bind(btn))
        btn_7.bind("<Button-1>", lambda _, btn=7: self._bind(btn))
        btn_8.bind("<Button-1>", lambda _, btn=8: self._bind(btn))
        btn_9.bind("<Button-1>", lambda _, btn=9: self._bind(btn))
        btn_ve.bind("<Button-1>", lambda _, btn="*": self._bind(btn))
        btn_colchet1.bind("<Button-1>", lambda _, btn="(": self._bind(btn))
        btn_0.bind("<Button-1>", lambda _, btn=0: self._bind(btn))
        btn_colchet2.bind("<Button-1>", lambda _, btn=")": self._bind(btn))
        btn_di.bind("<Button-1>", lambda _, btn="/": self._bind(btn))
        btn_vi.bind("<Button-1>", lambda _, btn=".": self._bind(btn))
        btn_ig.bind("<Button-1>", lambda _, btn="=": self._bind(btn))

        wlist.posicionar_objetos()