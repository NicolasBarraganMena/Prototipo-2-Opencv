# -*- coding: utf-8 -*-
"""
@author: Nicolas Barragan
"""

import cv2
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#captura
cap = cv2.VideoCapture(0) #acceso a la camara integrada del computador

#Guardara en que estado se encuentra actualmente el programa
# 0: Defecto, 1: Start, 2: Update, 3: Error
estado = 0

with mp_hands.Hands(static_image_mode=False,max_num_hands=2, min_detection_confidence=0.5) as hands:
    
    #ciclo infinito "update"
    while True:
        
        #verificar si la captura esta funcionando
        disponible, fotograma = cap.read()
        
        #Maquina de estados
        if(disponible == True and estado==0):
            estado = 1 #Empieza el programa
        elif(disponible == False and estado==0):
            estado = 3 #Error(camara no disponible o camara dañada)
        
        #Estados
        if(estado == 1): #Start
            #print("Start")
            
            estado = 2
            
        elif(estado == 2): #Update
            #print("Update")
            
            #Mostrar la captura
            cv2.imshow("Camara", fotograma)
            
            #Comandos de teclado
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                #Liberar camara y destruir ventanas
                print("Finalizando")
                break
        elif(estado == 3): #Error
            print("Error, camara no disponible")
            break
    
    #libera camara y destruye ventanas
    cap.release()
    cv2.destroyAllWindows()