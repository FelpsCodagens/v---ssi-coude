from PyPDF2 import *
import tkinter as tk

listaNomes = [""]
infoPesquisa = ["informática", "./", "convocacao-bauru"]

#Função que define o body do pdf

def filtroPdf(data , palavra):
    inicio = data.find(palavra)
    return data[inicio+len(palavra):]


def filtrarCandidatos(root, curso, rootUrl ,nomePdf):

    bodyPdf = " "

    if rootUrl== " ":
        rootUrl = "./"

    #Tenta acessar e ler a quantidade de paginas do arquivo

    try:  
        pdf = open(rootUrl + nomePdf + ".pdf", "rb")
        pdfReader = PdfReader(pdf)
        paginas = len(pdfReader.pages)

    except:
        root.config(text="Não foi possivel acessar o arquivo! Verifique o nome colocado e a pasta raiz declarada.", fg = "red", font=("arial", 16))
    
    else:
        try:

            #Acessa os alunos com base no curso escolhido

            for i in range(paginas):
                pagina = pdfReader.pages[i]
                gugu = pagina.extract_text().lower()

                if gugu.find(curso.lower()) > 0:
                    texto = pagina.extract_text()
                    bodyPdf = bodyPdf + "\n" + filtroPdf(texto, "Documento")

                    pagina = pdfReader.pages[i+1]
                    gugu = pagina.extract_text().lower()

                    #Verifica se tem continuação na pagina abaixo e caso tenha, adiciona ela à variavel geral

                    if gugu.find("bauru") < 0:
                        texto = pagina.extract_text()
                        bodyPdf = bodyPdf + "\n" + filtroPdf(texto, "Vagas")

        except:
            
            return root.config(text = "Filtro inválido!", fg = "red", font=("arial", 16))

        else:

            #Separa os nomes e os rgs em uma lista

            listaNomes = bodyPdf.split("\n")

            #Retira os espaços da lista

            p = 0
            for i in listaNomes:
                if listaNomes[p] == ' ' or listaNomes[p] == '' or listaNomes[p] == '  ':
                    listaNomes.pop(p)
                else:
                    listaNomes[p] = listaNomes[p].strip()
                p = p + 1
            p = 0

            #Transforma a lista de nomes em uma string para apresenta-la no label

            bodyPdf = ""
            for i in listaNomes:
                bodyPdf = bodyPdf + "\n" + i
            
            return root.config(text = bodyPdf , fg = "black", font=("arial", 12))


def getEntry(p, info):
    infoPesquisa[p] = info.get()
    print(infoPesquisa)


def main():
    window = tk.Tk()
    window.geometry("1300x760+200+200")
    window.title("Teste => Leitura vagas cti")

    #Gambiarra pra adicionar um scrollbar

    mainFrame = tk.Frame(window)
    mainFrame.pack(fill="both", expand=1)

    mainCanvas = tk.Canvas(mainFrame)
    mainCanvas.pack(side="left", fill="both", expand=1)
    
    scrollbar = tk.Scrollbar(mainFrame , orient="vertical", command=mainCanvas.yview)
    scrollbar.pack(side="right", fill="y")

    #Configuração do scroll/canvas 
    #Corrigir o scroll que não ta descendouj!!!!!!!!!!!!!

    mainCanvas.configure(yscrollcommand=scrollbar)
    mainCanvas.bind("<Configure>", lambda e: mainCanvas.configure(scrollregion=mainCanvas.bbox("all")))

    #Gamibiarra dois: o inimigo agora é outro, aparentemente temos que colocar outro frame aqui pra dar bom :)

    secondFrame = tk.Frame(mainCanvas)

    mainCanvas.create_window((0,0), window=secondFrame, anchor="nw")

    #Frame pros filitrinhos poggers

    frFiltro = tk.Frame(secondFrame)
    frFiltro.pack(side="top", expand=1, fill="both", padx=20, pady=20)

    #Obtem o nome do curso

    frCurso = tk.Frame(frFiltro)
    frCurso.pack(side="top",fill="both")

    lbCurso = tk.Label(frCurso, text="Curso:", width=7, anchor="w", font=("arial", 14), fg="black")
    lbCurso.pack(side="left")

    enCurso = tk.Entry(frCurso)
    enCurso.pack(side="left")

    btCurso = tk.Button(frCurso, text="Ok",  width=3, height=1, command= lambda: getEntry(0,enCurso))
    btCurso.pack(side="left")

    #Obtem o nome da pasta raiz

    frRoot = tk.Frame(frFiltro)
    frRoot.pack(side="top",fill="both")

    lbRoot = tk.Label(frRoot, text="Raiz:", width=7,  anchor="w", font=("arial", 14), fg="black")
    lbRoot.pack(side="left")

    enRoot = tk.Entry(frRoot)
    enRoot.pack(side="left")

    btRoot = tk.Button(frRoot, text="Ok",  width=3, height=1, command= lambda: getEntry(1,enRoot))
    btRoot.pack(side="left")

    #Obtem o nome do arquivo

    frArquivo = tk.Frame(frFiltro, width=30)
    frArquivo.pack(side="top", fill="both")

    lbArquivo = tk.Label(frArquivo, text="Arquivo:", width=7,  anchor="w", font=("arial", 14), fg="black")
    lbArquivo.pack(side="left")

    enArquivo = tk.Entry(frArquivo)
    enArquivo.pack(side="left")

    btArquivo = tk.Button(frArquivo, text="Ok",  width=3, height=1, command= lambda: getEntry(2, enArquivo))
    btArquivo.pack(side="left")

    #Pesquisa 👍

    frPesquisa = tk.Frame(secondFrame)
    frPesquisa.pack(side="top", fill="both", expand=1, padx=20)

    btPesquisar = tk.Button(frPesquisa, text="Mostrar Pdf", width=10, height=1, font=("arial", 12), command= lambda: filtrarCandidatos(lbMostrar,infoPesquisa[0], infoPesquisa[1], infoPesquisa[2]))
    btPesquisar.pack(side="left")

    #Mostrar valores

    frMostrar = tk.Frame(secondFrame)
    frMostrar.pack(side="top", fill="both", expand=1, padx=20)

    lbMostrar = tk.Label(frMostrar,justify="left", anchor="nw")
    lbMostrar.pack(side="top", fill="both", expand= 1)


    window.mainloop()
main()