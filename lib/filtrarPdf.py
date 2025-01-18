from PyPDF2 import *

#Função que define o body do pdf

def filtroPdf(data , palavra):
    inicio = data.find(palavra)
    return data[inicio+len(palavra):]

#Função para obtenção de dados do pdf

def filtrarCandidatos(Tk, root , curso, ano ,nomePdf):

    bodyPdf = " "

    if ano== " ":
        ano = "2025"

    #Tenta acessar e ler a quantidade de paginas do arquivo

    try:  
        pdf = open("./pdf/" + ano + "/" + nomePdf, "rb")
        pdfReader = PdfReader(pdf)
        paginas = len(pdfReader.pages)
        print(paginas)

    except:
        root.config(text="Não foi possivel acessar o arquivo! Verifique o nome colocado e a pasta raiz declarada.", fg = "red", font=("arial", 16))
    
    else:
        try:
            #verifica se o arquivo só tem uma pagina

            if(paginas == 1):
                body = pdfReader.pages[0]
                texto = body.extract_text()
                bodyPdf = "############ Dados agrupados pois existe apenas uma pagina! ############ \n " + texto

            else:
                #Acessa os alunos com base no curso escolhido

                for i in range(paginas-1):
                    pagina = pdfReader.pages[i]
                    paginaText = pagina.extract_text().lower()

                    if paginaText.find(curso.lower()) > 0:
                        texto = pagina.extract_text()
                        bodyPdf = bodyPdf + "\n" + filtroPdf(texto, "Nome")

                        pagina = pdfReader.pages[i+1]
                        paginaText = pagina.extract_text().lower()

                        #Verifica se tem continuação na pagina abaixo e caso tenha, adiciona ela à variavel global

                        if paginaText.find("bauru") < 0:
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
            
            
            Tk.geometry("1300x760")
            return root.config(text = bodyPdf , fg = "black", font=("arial", 12))