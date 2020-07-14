import cv2
import numpy as np
import dlib 
from math import hypot
olho_direito = list(range(36, 42))
olho_esquerdo = list(range(42, 48))
sobrancelha_esquerda = list(range(18,22))
sobrancelha_direita = list(range(23,27))
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector() #função da biblioteca dlib para detectar o rosto
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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
        
        _,threshold_olho = cv2.threshold(olho_cinza,80,255,cv2.THRESH_BINARY) #feito threshold na imagem cinza para detectar mais precisamente a direção do olho
        height, width = threshold_olho.shape
        esquerdo_t = threshold_olho[0:height,0:int(width/2)]
        esquerdo_branco = cv2.countNonZero(esquerdo_t)
        direito_t = threshold_olho[0:height,int (width/2):width]
        direito_branco = cv2.countNonZero(direito_t)
        
        if esquerdo_branco == 0:
            razao_olho = 1
        elif direito_branco == 0:
            razao_olho = 5
        else:
            razao_olho = esquerdo_branco/direito_branco
        
        return razao_olho

def getPontosOlho(landmarks,pontos):
    p1 = (landmarks.part(pontos[0]).x,landmarks.part(pontos[0]).y)
    p2 = (landmarks.part(pontos[3]).x,landmarks.part(pontos[3]).y)
    p3 = int(((landmarks.part(pontos[1]).x)+(landmarks.part(pontos[2]).x))/2),int(((landmarks.part(pontos[1]).y)+(landmarks.part(pontos[2]).y))/2) 
    p4 = int(((landmarks.part(pontos[5]).x)+(landmarks.part(pontos[4]).x))/2),int(((landmarks.part(pontos[5]).y)+(landmarks.part(pontos[4]).y))/2)
    
    return p1,p2,p3,p4
    
while True:
    _, quadro = cap.read()
    quadro_cinza = cv2.cvtColor(quadro,cv2.COLOR_BGR2GRAY)

    rostos = detector(quadro)
    for rosto in rostos:
        bx,by = rosto.left(),rosto.top()
        x1,y1 = rosto.right(),rosto.bottom()
        cv2.rectangle(quadro,(bx,by),(x1,y1),(255,0,0),1) #desenha um retângulo onde é detectado o rosto #primeiro passo de detecção do rosto foi concluído
        landmarks = predictor(quadro, rosto)

        piscadaEsquerdo = getPiscada([36,37,38,39,40,41],landmarks)
        piscadaDireito = getPiscada([42,43,44,45,46,47],landmarks)
              
        if (piscadaEsquerdo+piscadaDireito)/2 > 5:
            cv2.putText(quadro,"PISCOU",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA,False) 
        
        razao_olhoEsquerdo = getRazaoOlho([36,37,38,39,40,41],landmarks)
        razao_olhoDireito = getRazaoOlho([42,43,44,45,46,47],landmarks)
        
        razao_olhos = (razao_olhoEsquerdo + razao_olhoDireito)/2
        
        if razao_olhos <= 0.7:
            cv2.putText(quadro,"direita",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
            
        elif 0.7<razao_olhos<1.5:
            cv2.putText(quadro,"centro",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
        else:
            cv2.putText(quadro,"esquerda",(50,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
        
        #cv2.putText(quadro,str(razao_olhos),(50,150),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),3)
        
    cv2.imshow("quadro",quadro)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

