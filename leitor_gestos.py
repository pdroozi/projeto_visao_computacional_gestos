"""
tutorial_gestos.py
------------------
Tutorial de Visão Computacional com MediaPipe (API nova — v0.10+)

Pré-requisitos:
    pip install opencv-python mediapipe requests
    py -3.11 -c "import requests; open('hand_landmarker.task','wb').write(requests.get('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task').content)"

Como rodar:
    py -3.11 tutorial_gestos.py

Pressione Q para sair.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarkerResult

# PASSO 1 — Carregue as imagens que serão exibidas

# Coloque as imagens na mesma pasta que este script. Troque os nomes de arquivo pelos seus.

IMAGENS = {
    "APONTAR":    cv2.imread("imagens/imagem_apontar.jpg"),
    "PAZ":        cv2.imread("imagens/imagem_paz.jpg"),
    "PUNHO":      cv2.imread("imagens/imagem_punho.webp"),
    "MAO_ABERTA": cv2.imread("imagens/imagem_aberta.webp"),
}

TAMANHO_IMAGEM = (300, 300)

# PASSO 2 — Configure o detector de mãos

ARQUIVO_MODELO = "hand_landmarker.task"

# Variável global que guarda o resultado mais recente
resultado_atual = None

def callback_resultado(result: HandLandmarkerResult, output_image, timestamp_ms):

    global resultado_atual
    resultado_atual = result


# Configurações do detector
opcoes = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=ARQUIVO_MODELO),
    running_mode=vision.RunningMode.LIVE_STREAM,  
    num_hands=1,                                  
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    result_callback=callback_resultado       
)

detector = vision.HandLandmarker.create_from_options(opcoes)

# FUNÇÕES DE RECONHECIMENTO DE GESTO

def dedo_levantado(lm, ponta, no):
    """
    Retorna True se o dedo estiver levantado.

    Mapa dos pontos:
        Indicador: ponta=8,  nó=6
        Médio:     ponta=12, nó=10
        Anelar:    ponta=16, nó=14
        Mindinho:  ponta=20, nó=18
    """
    return lm[ponta].y < lm[no].y


def reconhecer_gesto(landmarks):
 
    indicador = dedo_levantado(landmarks, 8, 6)
    medio     = dedo_levantado(landmarks, 12, 10)
    anelar    = dedo_levantado(landmarks, 16, 14)
    mindinho  = dedo_levantado(landmarks, 20, 18)

    if indicador and not medio and not anelar and not mindinho:
        return "APONTAR"

    if indicador and medio and not anelar and not mindinho:
        return "PAZ"

    if not indicador and not medio and not anelar and not mindinho:
        return "PUNHO"

    if indicador and medio and anelar and mindinho:
        return "MAO_ABERTA"

    return None


CORES_PLACEHOLDER = {
    "APONTAR":    (0, 200, 0),
    "PAZ":        (0, 165, 255),
    "PUNHO":      (0, 0, 220),
    "MAO_ABERTA": (200, 0, 200),
}

def mostrar_imagem_reacao(frame, gesto):

    fh, fw = frame.shape[:2]
    w, h = TAMANHO_IMAGEM
    x1, y1 = fw - w - 10, 10

    imagem = IMAGENS.get(gesto)

    if imagem is None:
        return  # sem imagem, não mostra nada

    imagem_redim = cv2.resize(imagem, TAMANHO_IMAGEM)
    frame[y1:y1+h, x1:x1+w] = imagem_redim


def desenhar_landmarks(frame, landmarks):
   
    h, w = frame.shape[:2]

    pontos = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    # Conexões entre os pontos (pares de índices que formam os ossos da mão)
    conexoes = [
        (0,1),(1,2),(2,3),(3,4),         # polegar
        (0,5),(5,6),(6,7),(7,8),         # indicador
        (0,9),(9,10),(10,11),(11,12),    # médio
        (0,13),(13,14),(14,15),(15,16),  # anelar
        (0,17),(17,18),(18,19),(19,20),  # mindinho
        (5,9),(9,13),(13,17)             # palma
    ]

    for inicio, fim in conexoes:
        cv2.line(frame, pontos[inicio], pontos[fim], (0, 200, 255), 2)

    for ponto in pontos:
        cv2.circle(frame, ponto, 5, (255, 255, 255), -1)


# PASSO 3 — Abra a webcam e inicie o loop

cam = cv2.VideoCapture(0)
timestamp = 0

print("Iniciando... Pressione Q para sair.")

while True:

    sucesso, frame = cam.read()
    if not sucesso:
        continue

    frame = cv2.flip(frame, 1)
    timestamp += 1

    # Converte para o formato do MediaPipe
    imagem_mp = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    detector.detect_async(imagem_mp, timestamp)

    gesto = None

    if resultado_atual and resultado_atual.hand_landmarks:

        landmarks = resultado_atual.hand_landmarks[0]

        desenhar_landmarks(frame, landmarks)

        gesto = reconhecer_gesto(landmarks)

        if gesto:
            mostrar_imagem_reacao(frame, gesto)

    texto = gesto if gesto else "nenhum gesto"
    cv2.putText(frame, f"Gesto: {texto}",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("Tutorial de Gestos", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('q') or tecla == 27:  # Q ou ESC
        break

# PASSO 4 — Limpeza

cam.release()
cv2.destroyAllWindows()
detector.close()
