# -*- coding: utf-8 -*-
"""
@author: Nicolas Barragan
"""

import cv2
import mediapipe as mp
import pyautogui


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#captura
cap = cv2.VideoCapture(0) #acceso a la camara integrada del computador

#Guardara en que estado se encuentra actualmente el programa
# 0: Defecto, 1: Start, 2: Update, 3: Error
estado = 0

#Tamaño de la pantalla
width, height = pyautogui.size()


#Mover el puntero del mouse
def moverRaton(xm,ym):
    #Mover el mouse
    pyautogui.FAILSAFE=False #evitar errores cuando se esta en los bordes del screen
    pyautogui.moveTo(xm,ym) #el cursor del mouse se mueve a la direccion indicada

#Click mouse
def clickRaton(y1,y2):
    if(y1>y2):
        #liberar el mouse
        print("Release Mouse")
        pyautogui.mouseUp()
    else:
        #oprimir el mouse
        print("Click Mouse")
        cv2.putText(fotograma,'Click',(xp+10,yp), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 1, cv2.LINE_AA)
        pyautogui.mouseDown()
        

with mp_hands.Hands(static_image_mode=False,max_num_hands=2, min_detection_confidence=0.8) as hands:
    
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
            print("Screen size: (" + str(width) + "," + str(height) + ")")
            
            estado = 2
            
        elif(estado == 2): #Update
            #print("Update")
            
            #Camara
            h,w,_ = fotograma.shape #Tamaño
            fotograma = cv2.flip(fotograma,1) #Efecto espejo
            fotograma = cv2.cvtColor(fotograma,cv2.COLOR_BGR2RGB)
            
            #calcular puntos clave
            fotograma.flags.writeable = False
            resultado = hands.process(fotograma)
            
            #devolver la configuracion de color a la normalidad
            fotograma.flags.writeable = True
            fotograma = cv2.cvtColor(fotograma, cv2.COLOR_RGB2BGR)
            
            if resultado.multi_hand_landmarks is not None:
                #Accediendo a los puntos clave
                for hand_landmarks in resultado.multi_hand_landmarks:
                    #Dibujar puntos clave
                    #print(hand_landmarks)
                    #mp_drawing.draw_landmarks(fotograma, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    #Dibujar puntero (punta dedo indice)
                    xp = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * w)
                    yp = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h)
                    cv2.circle(fotograma,(xp,yp),5,(255,0,255),-1)
                    #cv2.putText(fotograma,'{},{}'.format(xp,yp),(xp+10,yp), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 1, cv2.LINE_AA)
                    #llama a la funcion de mapeo
                    xm = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                    ym = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                    #llama a la función para mover el mouse
                    moverRaton(xm, ym)
                    #llama a la funcion de clickear mouse
                    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h)
                    y2 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * h)
                    clickRaton(y1, y2)
                    
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