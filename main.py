from tkinter import *
from application.calculadora import Calculadora
from json import load
json = {}

# CARREGA O ARQUIVO JSON
with open("cfg.json", mode="r", encoding="utf-8") as doc:
    json = load(doc)
    doc.close()

# INICIA O PROGRAMA
if __name__ == "__main__":
    tela = Tk()
    tela.geometry("-500+100")
    tela.maxsize(400,600)
    tela.minsize(400,600)
    tela.title("Calculadora")
    Calculadora(tela, json)