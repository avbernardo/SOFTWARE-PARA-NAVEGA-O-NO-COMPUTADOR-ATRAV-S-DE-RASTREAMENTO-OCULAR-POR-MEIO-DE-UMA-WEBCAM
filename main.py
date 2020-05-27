import cv2
import numpy as np
import dlib 
olho_direito = list(range(36, 42))
olho_esquerdo = list(range(42, 48))
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector() #função da biblioteca dlib para detectar o rosto
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    _, quadro = cap.read()

    rostos = detector(quadro)
    for rosto in rostos:
        bx,by = rosto.left(),rosto.top()
        x1,y1 = rosto.right(),rosto.bottom()
        cv2.rectangle(quadro,(bx,by),(x1,y1),(255,0,0),1) #desenha um retângulo onde é detectado o rosto #primeiro passo de detecção do rosto foi concluído
        landmarks = predictor(quadro, rosto)
       # for n in range(0,68):
        #    x = landmarks.part(n).x
         #   y = landmarks.part(n).y
          #  cv2.circle(quadro,(x,y),2,(0,0,255),-1) #todos os 68 pontos foram detectados pela biblioteca dlib
          
        p1 = (landmarks.part(36).x,landmarks.part(36).y)
        p2 = (landmarks.part(39).x,landmarks.part(39).y)
        p3 = int(((landmarks.part(37).x)+(landmarks.part(38).x))/2),int(((landmarks.part(37).y)+(landmarks.part(38).y))/2) 
        p4 = int(((landmarks.part(41).x)+(landmarks.part(40).x))/2),int(((landmarks.part(41).y)+(landmarks.part(40).y))/2)

        linhaH = cv2.line(quadro,p1,p2,(0,255,0),1)
        linhaV = cv2.line(quadro,p3,p4,(0,255,0),1) #desenhada uma 'cruz' no olho

                                                
        
        
    cv2.imshow("quadro",quadro) 

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

