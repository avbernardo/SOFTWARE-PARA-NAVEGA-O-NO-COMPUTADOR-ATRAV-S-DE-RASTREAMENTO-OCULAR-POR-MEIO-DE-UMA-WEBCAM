import cv2
import numpy as np
import dlib 
from math import hypot
olho_direito = list(range(36, 42))
olho_esquerdo = list(range(42, 48))
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

def getPontosOlho(landmarks,pontos):
    p1 = (landmarks.part(pontos[0]).x,landmarks.part(pontos[0]).y)
    p2 = (landmarks.part(pontos[3]).x,landmarks.part(pontos[3]).y)
    p3 = int(((landmarks.part(pontos[1]).x)+(landmarks.part(pontos[2]).x))/2),int(((landmarks.part(pontos[1]).y)+(landmarks.part(pontos[2]).y))/2) 
    p4 = int(((landmarks.part(pontos[5]).x)+(landmarks.part(pontos[4]).x))/2),int(((landmarks.part(pontos[5]).y)+(landmarks.part(pontos[4]).y))/2)
    
    return p1,p2,p3,p4
    
while True:
    _, quadro = cap.read()

    rostos = detector(quadro)
    for rosto in rostos:
        bx,by = rosto.left(),rosto.top()
        x1,y1 = rosto.right(),rosto.bottom()
        cv2.rectangle(quadro,(bx,by),(x1,y1),(255,0,0),1) #desenha um retângulo onde é detectado o rosto #primeiro passo de detecção do rosto foi concluído
        landmarks = predictor(quadro, rosto)

        piscadaEsquerdo = getPiscada([36,37,38,39,40,41],landmarks)
        piscadaDireito = getPiscada([42,43,44,45,46,47],landmarks)
        
        

        
        if (piscadaEsquerdo+piscadaDireito)/2 > 4:
            cv2.putText(quadro,"PISCASTE",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2,cv2.LINE_AA,False) 
        
    cv2.imshow("quadro",quadro)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

