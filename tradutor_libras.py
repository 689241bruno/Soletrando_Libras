import cv2
import mediapipe as mp
import pickle
import numpy as np

# Carrega o Modelo de IA
try:
    with open('modelo_libras.pkl', 'rb') as f:
        modelo = pickle.load(f) 
except FileNotFoundError:
    print("Arquivo 'modelo_libras.pkl' não encontrado.")
    exit()


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
contador = 0
contadorLetra = 0
pontos = 0
corTexto = (255, 255, 255)

palavra = []

l = 0
palavra_escolhida = str(input("Digite uma palavra: ")).upper()



sinal_previsto = "Aguardando Gesto..."


with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: # se ret(variavel de checagem) for diferente de falso o codigo continua
            continue

        #frame = cv2.flip(frame, 1) vira a imagem
        frame = cv2.flip(frame, 1) 

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        frame = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                contador += 1
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                keypoints = []
                for landmark in hand_landmarks.landmark:
                    keypoints.extend([landmark.x, landmark.y, landmark.z])
                print(contador)
                
                # Converte para array numpy e ajusta o formato para a IA
                dados_entrada = np.array([keypoints]) 

                # retorna o sinal
                sinal_previsto = modelo.predict(dados_entrada)[0] # 0 pq ele retornar um array, ai ele pega o primeiro elemento
                if contador >= 80:
                    palavra.append(sinal_previsto)
                    if contadorLetra <= len(palavra_escolhida):
                        print(len(palavra_escolhida))
                        if sinal_previsto == palavra_escolhida[contadorLetra]:
                            print(sinal_previsto, palavra_escolhida[contadorLetra])
                            print("acertou")
                            corTexto = (0, 255, 0)
                            pontos += 1
                        else: 
                            print("errou")
                            corTexto = (0, 0, 255)
                            print(sinal_previsto, palavra_escolhida[contadorLetra])
                            print(len(palavra_escolhida))
                    else:
                        print(len(palavra_escolhida))
                        break
                    contador = 0
                    contadorLetra += 1
        else:
            sinal_previsto = "Aguardando Gesto..." 
        cv2.putText(frame, f"SINAL: {sinal_previsto}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.putText(frame, f" {palavra}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, corTexto, 3)
        cv2.putText(frame, f"pontuacao: {pontos}", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))
        cv2.imshow('Tradutor Libras ', frame)
        if cv2.waitKey(1) & 0xFF == ord('1'):
            print("fechou")
            break
        
cap.release()
cv2.destroyAllWindows()
print(palavra)