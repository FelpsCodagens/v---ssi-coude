#Função de alterar filtros
import os
from tkinter import *

def getEntry(root, p, info, data):
    data[p] = info.get()
    if p == 1:
        try:
            data[2] = os.listdir("./pdf/" + data[1] + "/")[0]
        except: 
            print("Pasta Vazia")
        else:
            root.delete(0,END)
            root.insert(0,data[2])
    print(data)