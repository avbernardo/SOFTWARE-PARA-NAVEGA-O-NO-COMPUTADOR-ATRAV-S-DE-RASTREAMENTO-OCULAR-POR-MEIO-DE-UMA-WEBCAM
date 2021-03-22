import cv2
import numpy as np
import dlib 
from math import hypot
import time
import ctypes
import winsound
import os
import json
import sys


with open ('config.json') as arquivo:
    config = json.load(arquivo)
    
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second
olho_direito = list(range(36, 42))
olho_esquerdo = list(range(42, 48))
sobrancelha_esquerda = list(range(18,22))
sobrancelha_direita = list(range(23,27))
cap = cv2.VideoCapture(int(config['webcam']))
seleciona = False
quadro_texto = np.zeros((220,1080),np.uint8)
quadro_texto[:] = 255
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

detector = dlib.get_frontal_face_detector() #função da biblioteca dlib para detectar o rosto
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
teclado = np.zeros((500,750,3),np.uint8)
tela_menu = np.zeros((800,800),np.uint8)
k = 0
direcao = 0
opcao = 0
texto_geral = ""


letras = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 6: "U", 7: "I", 8: "O", 9: "P",
          10: "A", 11: "S", 12: "D", 13: "F", 14: "G", 15: "H", 16: "J", 17: "K", 18: "L", 19: "C",
          20: "Z", 21: "X", 22: "C", 23: "V", 24: "B", 25: "N", 26: "M" , 28 : " ", 29 : "<" , 27 : "<-"}

frases = {0: "OLA", 1: "SIM", 2: "NAO", 3:"ESTOU BEM", 4: "ESTOU MAL", 5: "BANHEIRO", 6: "DESCONFORTO", 7: "FOME", 8: "SEDE",
          9: "FRIO" , 10: "CALOR" , 11 : "<"}

def criaTeclado(index,letra,selector):
    
    if index == 0:
       x = 0
       y = 0
    elif index == 1:
        x = 70
        y = 0
    elif index == 2:
        x = 140
        y = 0
    elif index == 3:
        x = 210
        y = 0
    elif index == 4:
        x = 280
        y = 0
    elif index == 5:
        x = 350
        y = 0
    elif index == 6:
        x = 420
        y = 0
    elif index == 7:
        x = 490
        y = 0
        
    elif index == 8:
        x = 560
        y = 0
    
    elif index == 9:
        x = 630
        y = 0

    elif index == 10:
        x = 0
        y = 70
    
    elif index == 11:
        x = 70
        y = 70
    
    elif index == 12:
        x = 140
        y = 70
    
    elif index == 13:
        x = 210
        y = 70
    
    elif index == 14:
        x = 280
        y = 70
    
    elif index == 15:
        x = 350
        y = 70
    
    elif index == 16:
        x = 420
        y = 70
    
    elif index == 17:
        x = 490
        y = 70
        
    elif index == 18:
        x = 560
        y = 70
    
    elif index == 19:
        x = 630
        y = 70
    
    elif index == 20:
        x = 0
        y = 140
    
    elif index == 21:
        x = 70
        y = 140
    
    elif index == 22:
        x = 140
        y = 140
    
    elif index == 23:
        x = 210
        y = 140
        
    elif index == 24:
        x = 280
        y = 140
        
    elif index == 25:
        x = 350
        y = 140
        
    elif index == 26:
        x = 420
        y = 140
    
    elif index == 27:
        x = 490
        y = 140
        
    elif index == 28:
        x = 140
        y = 210
        
    elif index == 29:
        x = 490
        y = 210
    
    
        
    # Teclas

    width = 70
    height = 70
    th = 2
    if (index == 28):
        width = 350
        
    if (index == 27):
        width = 140
            
    if selector is True:
        cv2.rectangle(teclado, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(teclado, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)
    
    # Texto 
    font_scale = 5
    text_size = cv2.getTextSize(letra, cv2.FONT_HERSHEY_PLAIN, font_scale, 2)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(teclado, letra, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 0, 0), 2)
    
def criaFrases(index,letra,selector):
    
    if index == 0:
       x = 0
       y = 0
    elif index == 1:
        x = 110
        y = 0
    elif index == 2:
        x = 220
        y = 0
    elif index == 3:
        x = 0
        y = 80     
    elif index == 4:
       x = 350
       y = 80
    elif index == 5:
        x = 0
        y = 160
    elif index == 6:
        x = 350
        y = 160
    elif index == 7:
        x = 0
        y = 240
    elif index == 8:
       x = 150
       y = 240
    elif index == 9:
        x = 300
        y = 240
    elif index == 10:
        x = 450
        y = 240   
    elif index == 11:
       x = 150
       y = 320

    # Teclas

    width = 110
    height = 80
    th = 2
    if (index == 3 or index == 4 or index == 5 or index == 6):
        width = 350
        
    if (index == 7 or index == 8 or index == 9 or index == 10):
        width = 150
        
    if selector is True:
        cv2.rectangle(teclado, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:
        cv2.rectangle(teclado, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)
    
    # Texto 
    font_scale = 3
    text_size = cv2.getTextSize(letra, cv2.FONT_HERSHEY_PLAIN, font_scale, 2)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(teclado, letra, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, font_scale, (255, 0, 0), 2)
    
def menu():
    rows, cols, _ = teclado.shape
    th_lines = 4 
    cv2.line(teclado, (int(cols/2) - int(th_lines/2), 0),(int(cols/2) - int(th_lines/2), rows),
             (51, 51, 51), th_lines)
    cv2.putText(teclado, "TECLADO", (30, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
    cv2.putText(teclado, "FRASES", (30 + int(cols/2), 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)



def getPiscada(pontos,landmarks):
    p1,p2,p3,p4 = getPontosOlho(landmarks,pontos)
    linhaH = cv2.line(quadro,p1,p2,(0,255,0),1)
    linhaV = cv2.line(quadro,p3,p4,(0,255,0),1) #desenhada uma 'cruz' no olho
        
    tamanhoV,tamanhoH = getTamanhoLinhasOlho(p1,p2,p3,p4)

    razao = (tamanhoH/tamanhoV)
    
    return razao
        
def getTamanhoLinhasOlho(p1,p2,p3,p4):
    tamanhoLinhaV = hypot((p3[0] - p4[0]),(p3[1] - p4[1]))
    tamanhoLinhaH = hypot((p1[0] - p2[0]),(p1[1] - p2[1]))
    
    return tamanhoLinhaV,tamanhoLinhaH

def getRazaoOlho(pontos,landmarks):
        olho_esquerdo_contorno = np.array([(landmarks.part(pontos[0]).x,landmarks.part(pontos[0]).y),
                                  (landmarks.part(pontos[1]).x,landmarks.part(pontos[1]).y),
                                  (landmarks.part(pontos[2]).x,landmarks.part(pontos[2]).y),
                                  (landmarks.part(pontos[3]).x,landmarks.part(pontos[3]).y),
                                  (landmarks.part(pontos[4]).x,landmarks.part(pontos[4]).y),
                                  (landmarks.part(pontos[5]).x,landmarks.part(pontos[5]).y)],np.int32)
        #cv2.polylines(quadro,[olho_esquerdo_contorno],True,(0,0,255),2) #desenhado um contorno no olho
        
        altura,largura,_ = quadro.shape
        mascara = np.zeros((altura,largura),np.uint8)
        cv2.polylines(mascara,[olho_esquerdo_contorno],True,255,2)
        cv2.fillPoly(mascara,[olho_esquerdo_contorno],255)
        olho = cv2.bitwise_and(quadro_cinza,quadro_cinza,mask=mascara)
        min_x = np.min(olho_esquerdo_contorno[:,0])
        max_x = np.max(olho_esquerdo_contorno[:,0])
        min_y = np.min(olho_esquerdo_contorno[:,1])
        max_y = np.max(olho_esquerdo_contorno[:,1])
        
        olho_cinza = olho[min_y:max_y,min_x:max_x]
        #olho_gray = cv2.cvtColor(olho,cv2.COLOR_BGR2GRAY) #imagem do olho convertida para escala de cinza para melhor precisão
        olho = cv2.resize(olho_cinza,None,fx=5,fy=5)
        
        _,threshold_olho = cv2.threshold(olho_cinza,int(config['tsholding']),255,cv2.THRESH_BINARY) #feito threshold na imagem cinza para detectar mais precisamente a direção do olho
        
        height, width = threshold_olho.shape
        esquerdo_t = threshold_olho[0:height,0:int(width/2)]
        esquerdo_branco = cv2.countNonZero(esquerdo_t)
        direito_t = threshold_olho[0:height,int (width/2):width]
        direito_branco = cv2.countNonZero(direito_t)
        
        if esquerdo_branco == 0:
            razao_olho = 1
        elif direito_branco == 0:
            razao_olho = 1
        else:
            razao_olho = esquerdo_branco/direito_branco
        
        return razao_olho

def getPontosOlho(landmarks,pontos):
    p1 = (landmarks.part(pontos[0]).x,landmarks.part(pontos[0]).y)
    p2 = (landmarks.part(pontos[3]).x,landmarks.part(pontos[3]).y)
    p3 = int(((landmarks.part(pontos[1]).x)+(landmarks.part(pontos[2]).x))/2),int(((landmarks.part(pontos[1]).y)+(landmarks.part(pontos[2]).y))/2) 
    p4 = int(((landmarks.part(pontos[5]).x)+(landmarks.part(pontos[4]).x))/2),int(((landmarks.part(pontos[5]).y)+(landmarks.part(pontos[4]).y))/2)
    
    return p1,p2,p3,p4

quadros = 0
indice_letra = 0
quadros_piscada = 0
texto = ""
menu_ = True
linha = 1
ultima_letra = ""
tamanho_fonte = 2

    
while True:
    _, quadro = cap.read()
    quadros += 1
    teclado[:] = (0,0,0)
    quadro_cinza = cv2.cvtColor(quadro,cv2.COLOR_BGR2GRAY)
    
    if opcao == 2:
        escrever = letras[indice_letra]
        
    if opcao == 1:
        escrever = frases[indice_letra]
    
    if menu_ is True:
        menu()
    
    rostos = detector(quadro)
    for rosto in rostos:
        bx,by = rosto.left(),rosto.top()
        x1,y1 = rosto.right(),rosto.bottom()
        cv2.rectangle(quadro,(bx,by),(x1,y1),(255,0,0),1) #desenha um retângulo onde é detectado o rosto #primeiro passo de detecção do rosto foi concluído
        landmarks = predictor(quadro, rosto)

        piscadaEsquerdo = getPiscada([36,37,38,39,40,41],landmarks)
        piscadaDireito = getPiscada([42,43,44,45,46,47],landmarks)
        if (piscadaEsquerdo+piscadaDireito)/2 > float(config['tamanho_piscada']):   
            cv2.putText(quadro,"PISCOU",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA,False) 
            quadros_piscada += 1
            quadros -= 1
            
            if(quadros_piscada == 7):
                if opcao == 1:
                    quadro_texto[:] = 255
                    if (escrever == "<"):
                        menu_ = True
                        indice_letra = 0
                        texto = ""
                        linha = 1
                    else:
                        texto = escrever
                    winsound.Beep(frequency, duration)
                elif opcao == 2:
                    if (escrever == "<-"):
                        linha_aux = 1
                        texto_aux = ""
                        texto = texto[:-1]
                        print(texto)
                        quadro_texto[:] = 255
                        for caracter in texto_geral:
                            
                            texto_aux += caracter
                            #print(texto_aux)
                            if len(texto_aux) > 30:
                                linha_aux += 1
                                texto_aux = ""
                            cv2.putText(quadro_texto,texto_aux,(5,linha_aux*50),cv2.FONT_HERSHEY_SIMPLEX,1,0,3)
                    elif(escrever == "<"):
                        menu_ = True
                        indice_letra = 0
                        texto = ""
                        texto_geral = ""
                        quadro_texto[:] = 255
                        linha = 1
                    else:
                        ultima_letra = escrever
                        texto += escrever
                    winsound.Beep(frequency, duration)
        else:
            quadros_piscada = 0
                     
        razao_olhoEsquerdo = getRazaoOlho([36,37,38,39,40,41],landmarks)
        razao_olhoDireito = getRazaoOlho([42,43,44,45,46,47],landmarks)
        
        razao_olhos = (razao_olhoEsquerdo + razao_olhoDireito)/2
        if razao_olhos <= float(config['direita_abaixo_de']):
            cv2.putText(quadro,"direita",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
            #k += 1
            direcao = 1
            if menu_ is True:
                opcao = 1
                menu_ = False
                winsound.Beep(frequency, duration)
            
        elif float(config['direita_abaixo_de'])<razao_olhos<float(config['esquerda_acima_de']):
            cv2.putText(quadro,"centro",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
        else:
            cv2.putText(quadro,"esquerda",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
            #k -= 1
            direcao = 0
            if menu_ is True:
                opcao = 2
                menu_ = False
                linha = 1
                winsound.Beep(frequency, duration)
        
        cv2.putText(quadro,str(razao_olhos),(50,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
    
    if quadros == 7:
        if direcao == 1:
            if menu_ is False:
                indice_letra += 1
        else:
            if menu_ is False:
                indice_letra -= 1
        quadros = 0
        
        if opcao == 2:
        
            if indice_letra == 30:
                indice_letra = 0
            if indice_letra == -1:
                indice_letra = 29
                
        if opcao == 1:
            
            if indice_letra == 12:
                indice_letra = 0
            if indice_letra == -1:
                indice_letra = 11
            
        
    if opcao == 2:
        for i in range(30):
            
            if i == indice_letra:
                seleciona = True
              
                        
            else:
                seleciona = False
             
            if menu_ is False:
                criaTeclado(i,letras[i],seleciona)
    
    if opcao == 1:
            
        for i in range(12):
            
            if i == indice_letra:
                seleciona = True
              
                        
            else:
                seleciona = False
             
            if menu_ is False:
                criaFrases(i,frases[i],seleciona)
    
    
    if (len(texto) > 30 and opcao == 2):
        texto_geral += texto
        linha += 1
        texto = ""
        texto += ultima_letra
    
    if (linha == 5 and opcao == 2):
        linha = 1
        quadro_texto[:] = 255
        texto = ""
        texto += ultima_letra
    
    if opcao == 1:
        tamanho_fonte = 4
        linha = 2
    else:
        tamanho_fonte = 1
        
             
           
    cv2.putText(quadro_texto,texto,(5,linha*50),cv2.FONT_HERSHEY_SIMPLEX,tamanho_fonte,0,3)
        
   # if menu_ is True:
    #    cv2.imshow("menu",tela_menu)
    cv2.resize(quadro, (10,10))
    cv2.moveWindow("quadro", 0,0)
    
    cv2.imshow("quadro",quadro)
    cv2.moveWindow("teclado",int(screensize[0]/2.5),0)
    cv2.imshow("teclado", teclado)
    cv2.moveWindow("texto",int(screensize[0]/8.5),int(screensize[1]/1.6))
    cv2.imshow("texto", quadro_texto)
    #cv2.imshow("cinza",quadro_cinza)
    

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()
cv2.destroyAllWindows()



































