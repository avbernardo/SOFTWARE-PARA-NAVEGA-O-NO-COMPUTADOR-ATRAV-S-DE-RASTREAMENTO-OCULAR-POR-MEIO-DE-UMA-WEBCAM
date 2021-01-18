# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:14:25 2020

@author: avber
"""


import cv2
import numpy as np

teclado = np.zeros((1000,1500,3),np.uint8)

letras = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T", 5: "Y", 6: "Y", 7: "I", 8: "O", 9: "P",
          10: "A", 11: "S", 12: "D", 13: "F", 14: "G", 15: "H", 16: "J", 17: "K", 18: "L", 19: "C",
          20: "Z", 21: "X", 22: "C", 23: "V", 24: "B", 25: "N", 26: "M"}
              

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
    
    
        
    # Teclas

    width = 70
    height = 70
    th = 2
    
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
    
for i in range(27):
    criaTeclado(i,letras[i],False)
    






cv2.imshow("teclado", teclado)
cv2.waitKey(0)
cv2.destroyAllWindows()