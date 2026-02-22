# Controlador de Cursor por Gestos
**Stack:** Python · OpenCV · MediaPipe · PyAutoGUI

---

## O que esse projeto faz

Usa a webcam para rastrear a mão em tempo real. Cada gesto reconhecido dispara uma ação no computador — mover o cursor, clicar, rolar a página — sem tocar no mouse.

---

## Instalação

```bash
# 1. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
python main.py
```

---

## Gestos Mapeados

| Gesto        | Como fazer                     | Ação no computador   |
|--------------|--------------------------------|----------------------|
| `APONTAR`    | Só o indicador levantado       | Move o cursor        |
| `CLICAR`     | Indicador + médio levantados   | Clique esquerdo      |
| `PUNHO`      | Mão fechada                    | Para o cursor        |
| `MAO_ABERTA` | Todos os dedos abertos         | Scroll para cima     |

---

## Como funciona — Conceitos para o TCC

### 1. Landmarks
O MediaPipe detecta **21 pontos** na mão, numerados de 0 a 20.
Cada ponto tem coordenadas `(x, y, z)` normalizadas entre 0 e 1.

```
        8   12  16  20
        |   |   |   |
        7   11  15  19
        |   |   |   |
        6   10  14  18
         \  |   |  /
          5  9  13
           \ | /
            \|/
             0 (pulso)
```

### 2. Lógica de classificação
Um dedo está **levantado** quando a ponta (ex: ponto 8) tem coordenada Y
**menor** que o nó (ponto 6). Y menor = mais alto na imagem, pois o eixo
cresce de cima para baixo.

```python
dedo_levantado = landmarks[8].y < landmarks[6].y
```

### 3. Suavização do cursor
Sem suavização, o cursor treme seguindo cada microvibração da mão.
A fórmula abaixo faz o cursor "perseguir" a mão gradualmente:

```python
cursor_x = cursor_x + (alvo_x - cursor_x) // SUAVIZACAO
```
Quanto maior `SUAVIZACAO`, mais lento e suave o movimento.

---

## Referências

- [MediaPipe Hands — Google](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Docs](https://docs.opencv.org/)
- [PyAutoGUI Docs](https://pyautogui.readthedocs.io/)
