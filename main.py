import os
import functools
from PyPDF2 import *
from tkinter import *
from tkinter import ttk
from lib.filtros import *
import lib.filtrarPdf as filtrarPdf

fp = functools.partial
osName = os.name

listaNomes = [""]
infoPesquisa = ["informática", "2023", ""]
infoPesquisa[2] = os.listdir("./pdf/" + infoPesquisa[1] + "/")[0]

def main():
    window = Tk()
    window.geometry("1300x750+20+20")
    window.title("Teste => Leitura vagas cti")

    #Gambiarra pra adicionar um scrollbar

    mainFrame = Frame(window)
    mainFrame.pack(fill="both", expand=1)

    mainCanvas = Canvas(mainFrame,highlightthickness=0)
    mainCanvas.pack(side="left", fill="both", expand=1)
    
    scrollbar = ttk.Scrollbar(mainFrame , orient="vertical", command=mainCanvas.yview)
    scrollbar.pack(side="right", fill="y")

    #Configuração do scroll/canvas 

    mainCanvas.configure(yscrollcommand=scrollbar.set)
    mainCanvas.bind("<Configure>", lambda e: mainCanvas.configure(scrollregion=mainCanvas.bbox("all")))

    #Verificação do sistema operacional

    if osName == "nt":
        #Funções de scroll pelo mouse #windows

        def onScroll(event):
            mainCanvas.yview_scroll(int(-1*(event.delta/120)),"units")

        def bindToMouseWheel(event):
            mainCanvas.bind_all("<MouseWheel>", onScroll)

        def unbindToMouseWheel(event):
            mainCanvas.unbind_all("<MouseWheel>") 
    else:
        #Funções de scroll pelo mouse #linux

        def onScroll(event, scroll):
            mainCanvas.yview_scroll(int(scroll),"units")

        def bindToMouseWheel(event):
            mainCanvas.bind_all("<Button-4>", fp(onScroll, scroll=-1))
            mainCanvas.bind_all("<Button-5>", fp(onScroll, scroll=1))

        def unbindToMouseWheel(event):
            mainCanvas.unbind_all("<Button-4>") 
            mainCanvas.unbind_all("<Button-5>") 

    #Reset do yview do canvas
    
    mainCanvas.yview_moveto(0)

    #Gamibiarra dois: o inimigo agora é outro, aparentemente temos que colocar outro frame aqui pra dar bom :)

    secondFrame = Frame(mainCanvas)
    mainCanvas.create_window((0,0), window=secondFrame, anchor="nw")

    #configurações do scroll

    mainFrame.bind("<Enter>", bindToMouseWheel)
    mainFrame.bind("<Leave>", unbindToMouseWheel)

    #Frame pros filitrinhos poggers

    frFiltro = Frame(secondFrame)
    frFiltro.pack(side="top", expand=1, fill="both", padx=20, pady=20)

    #Obtem o nome do curso

    frCurso = Frame(frFiltro)
    frCurso.pack(side="top",fill="both")

    lbCurso = Label(frCurso, text="Curso:", width=7, anchor="w", font=("arial", 14), fg="black")
    lbCurso.pack(side="left")

    enCurso = Entry(frCurso)
    enCurso.pack(side="left")

    btCurso = Button(frCurso, text="Ok",  width=3, height=1, command= lambda: getEntry(0,0,enCurso, infoPesquisa))
    btCurso.pack(side="left")

    #Obtem o nome da pasta raiz

    frAno = Frame(frFiltro)
    frAno.pack(side="top",fill="both")

    lbAno = Label(frAno, text="Ano:", width=7,  anchor="w", font=("arial", 14), fg="black")
    lbAno.pack(side="left")

    enAno = Entry(frAno)
    enAno.pack(side="left")

    btAno = Button(frAno, text="Ok",  width=3, height=1, command= lambda: getEntry(enArquivo,1,enAno, infoPesquisa))
    btAno.pack(side="left")

    #Obtem o nome do arquivo

    frArquivo = Frame(frFiltro, width=30)
    frArquivo.pack(side="top", fill="both")

    lbArquivo = Label(frArquivo, text="Arquivo:", width=7,  anchor="w", font=("arial", 14), fg="black")
    lbArquivo.pack(side="left")

    enArquivo = Entry(frArquivo)
    enArquivo.pack(side="left")

    btArquivo = Button(frArquivo, text="Ok",  width=3, height=1, command= lambda: getEntry(0,2, enArquivo, infoPesquisa))
    btArquivo.pack(side="left")
    
    #Definir itens padrões 

    enCurso.insert(0,infoPesquisa[0])
    enAno.insert(0,infoPesquisa[1])
    enArquivo.insert(0,infoPesquisa[2])

    #Pesquisa 👍

    frPesquisa = Frame(secondFrame)
    frPesquisa.pack(side="top", fill="both", expand=1, padx=20)

    btPesquisar = Button(frPesquisa, text="Mostrar Pdf", width=10, height=1, font=("arial", 12), command= lambda: filtrarPdf.filtrarCandidatos(window,lbMostrar,infoPesquisa[0], infoPesquisa[1], infoPesquisa[2]))
    btPesquisar.pack(side="left")

    #Mostrar valores

    frMostrar = Frame(secondFrame)
    frMostrar.pack(side="top", fill="both", expand=1, padx=20)

    lbMostrar = Label(frMostrar, text=" ", justify="left", anchor="nw")
    lbMostrar.pack(side="top", fill="both", expand= 1)


    window.mainloop()
main()