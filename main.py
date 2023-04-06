#ESTE CÓDIGO ESTÁ APENAS FUNCIONANDO PARA A MÃO DIREITA, SE TENTAR COM A ESQUERDA DISPARARÁ CLIQUES ATÉ QUE A MÃO SAIA
#DA ARÉA DE CAPTURA DA CÂMERA.

#A ARÉA DE MOVIMENTAÇÃO DO CURSOR É RESTRITA ÀS DIMENSÕES DA TELA DE CAPTURA, FORAM ADICIONADOS ALGUNS MUTIPLICADORES
# PARA AUMETAR A ÁREA DE ALCANCE DO CURSOR.

#A CÂMERA CAPTURA A IMAGEM INVERTIDA, LOGO AS COORDENADAS NO EIXO Y TAMBÉM ESTÃO INVERTIDAS, ADICIONEI UMA FUNÇÃO PARA
# INVERTER O EIXO Y.

import cv2
import mediapipe as mp
import pyautogui

#Inicializa a captura de vídeo
cam = cv2.VideoCapture(0)

hand = mp.solutions.hands
#Define o número máximo de mãos que serão detectadas
Hand = hand.Hands(max_num_hands= 1)
#cria um objeto para desenhar os pontos e linhas
Sketch = mp.solutions.drawing_utils

while True:
    #"check" retorna um booleano se a captura foi feita com sucesso, caso verdadeiro, "img" recebe a imagem capturada
    check,img= cam.read()
    #Converte a imagem capturada para RGB
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #Processa a imagem capturada
    results = Hand.process(imgRGB)
    handsPoints = results.multi_hand_landmarks
    points = []
    #Captura as dimensões da imagem capturada
    h , w, _ = img.shape
    #Parâmetros para ajuste de área (pode variar de acordo com o tamanho do seu monitor)
    mutiplyW = 1920
    mutiplyH = 3000

    if handsPoints:
        for auxPoints in handsPoints:
            #Desenha as linhas que ligam os pontos da mão
            Sketch.draw_landmarks(img, auxPoints,hand.HAND_CONNECTIONS)
            #adiciona os numeros dos pontos presentes na mão
            for id, coord in enumerate( auxPoints.landmark):
                #Captura as coordenadas da imagem capturada
                ncX,ncY = int(coord.x *w), int(coord.y*h )
                #mutiplicando as coordenadas para ajustar a área de movimentação do cursor
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
                #Imprime na imagem os numeros dos pontos, econfigura a posição do texto e caracteristicas
                cv2.putText(img, str(id),(ncX,ncY+10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)

                print(cX,cY)
                #Adiciona as coordenadas a um array
                points.append((cX, cY))

        #Colocando o ponto 8 no array
        pointer= [8]
        if auxPoints:
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