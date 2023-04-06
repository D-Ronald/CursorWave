#ESTE CÓDIGO ESTÁ APENAS FUNCIONANDO PARA A MÃO DIREITA, SE TENTAR COM A ESQUERDA DISPARARÁ CLIQUES ATÉ QUE A MÃO SAIA
#DA ARÉA DE CAPTURA DA CÂMERA.

#A ARÉA DE MOVIMENTAÇÃO DO CURSOR É RESTRITA ÀS DIMENSÕES DA TELA DE CAPTURA, FORAM ADICIONADOS ALGUNS MUTIPLICADORES
# PARA AUMETAR A ÁREA DE ALCANCE DO CURSOR.

#A CÂMERA CAPTURA A IMAGEM INVERTIDA, LOGO AS COORDENADAS NO EIXO Y TAMBÉM ESTÃO INVERTIDAS, ADICIONEI UMA FUNÇÃO PARA
# INVERTER O EIXO Y.

import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
hand = mp.solutions.hands
Hand = hand.Hands(max_num_hands= 1)
desenho = mp.solutions.drawing_utils

while True:
    check,img= cam.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    h , w, _ = img.shape
    points = []

    #Parâmetros para ajuste de área (pode variar de acordo com o tamanho do seu monitor)
    mutiplyW = 1920
    mutiplyH = 3000

    if handsPoints:
        for i in handsPoints:
            desenho.draw_landmarks(img, i,hand.HAND_CONNECTIONS)
            for id, coord in enumerate( i.landmark):
                ncX,ncY = int(coord.x *w), int(coord.y*h )
                cX, cY= int(coord.x * mutiplyW), int(coord.y * mutiplyH)
                if cX!=0:
                    #FUNÇÃO DE INVERSÃO
                    cX=-1 * (cX-mutiplyW)
                elif cX>mutiplyW:
                    cX = mutiplyW
                if cY<=0:
                    cY=1
                elif cY > mutiplyH:
                    cY = mutiplyH

                cv2.putText(img, str(id),(ncX,ncY+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)

                print(cX,cY)
                points.append((cX, cY))

        #Colocando o ponto 8 no array
        pointer= [8]
        if i:
            #Capturando a posição do ponto
            for x in pointer:
                posX = points[x][0]
                posY = points[x][1]
                #Move o ponteiro do mouse de acordo com a posições capturadas
                pyautogui.moveTo(posX,posY)

                #Ponto 4 do polegar do ponto 5 do dedo indicador em direção ao ponto 9 do dedo médio
                if points[4][0]>points[5][0]:
                    #Click do mouse
                    pyautogui.leftClick()

                #Ponto 8 do indicador abaixo do ponto 6
                #Ao mesmo temo em que o ponto 12 do dedo médio está abaixo do ponto 10 do dedo médio
                if points[8][1]>points[6][1] and points[12][1]>points[10][1] :
                    #rolagem para baixo
                    pyautogui.scroll(-150)

                #Ponto 16 do dedo anelar abaixo do ponto 14 do dedo anelar
                #ponto 20 do dedo mindinho abaixo do ponto 18 do mindinho
                elif points[16][1]>points[14][1] and points[20][1]>points[18][1]:
                    #rolagem para cima
                    pyautogui.scroll(150)

    cv2.imshow("Imagem",img)
    cv2.waitKey(1)