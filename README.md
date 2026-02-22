# 👋 Reconhecimento de Gestos com Visão Computacional

Projeto em Python que usa a webcam para detectar gestos da mão em tempo real utilizando o MediaPipe do Google, e exibe uma imagem correspondente a cada gesto reconhecido.

---

## Índice

- [Visão geral](#visão-geral)
- [Linguagens e bibliotecas](#linguagens-e-bibliotecas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como funciona — fluxo completo](#como-funciona--fluxo-completo)
- [Conceito de Landmarks](#conceito-de-landmarks)
- [Pré-requisitos](#pré-requisitos)
- [Instalação passo a passo](#instalação-passo-a-passo)
- [Como rodar](#como-rodar)
- [Gestos reconhecidos](#gestos-reconhecidos)
- [Funções do código](#funções-do-código)
- [Como adicionar um novo gesto](#como-adicionar-um-novo-gesto)
- [Erros comuns](#erros-comuns)

---

## Visão geral

O programa abre a câmera do computador e, frame a frame, analisa se existe uma mão visível. Quando encontra, mapeia 21 pontos anatômicos da mão (chamados landmarks) e usa a posição desses pontos para classificar o gesto que está sendo feito. Cada gesto mapeado exibe uma imagem diferente na janela.

---

## Linguagens e bibliotecas

### Python 3.11
Linguagem principal do projeto. Versão 3.11 é obrigatória — o MediaPipe não tem suporte para versões 3.12 ou superiores.

### OpenCV (`opencv-python`)
Biblioteca de visão computacional. É usada para:
- Acessar a webcam e capturar frames em tempo real
- Exibir a janela com o vídeo processado
- Desenhar linhas, pontos e textos sobre o frame
- Carregar e redimensionar as imagens de reação
- Converter o espaço de cor de BGR para RGB

### MediaPipe (`mediapipe`)
Framework de machine learning do Google para processamento de mídia em tempo real. É usado para:
- Detectar se há uma mão no frame
- Retornar os 21 landmarks (pontos) da mão com coordenadas x, y, z normalizadas
- Rastrear a mão continuamente entre frames

### Requests (`requests`)
Biblioteca HTTP do Python. Usada apenas uma vez, durante a configuração, para baixar o arquivo de modelo do MediaPipe diretamente da internet.

---

## Estrutura do projeto

```
projeto_gestos/
│
├── tutorial_gestos.py        # script principal — toda a lógica do programa
├── hand_landmarker.task      # modelo de ML do MediaPipe (baixado na instalação)
├── requirements.txt          # dependências do projeto
├── README.md                 # este arquivo
│
└── imagens/
    ├── imagem_apontar.jpg    # exibida quando: só o indicador está levantado
    ├── imagem_paz.jpg        # exibida quando: indicador + médio levantados
    ├── imagem_punho.jpg      # exibida quando: mão fechada
    └── imagem_aberta.jpg     # exibida quando: todos os dedos abertos
```

> As imagens são opcionais. Se não existirem na pasta, o programa funciona normalmente e simplesmente não exibe nada no canto.

---

## Como funciona — fluxo completo

```
Webcam captura frame
        ↓
OpenCV lê o frame e espelha horizontalmente
        ↓
Frame convertido de BGR para RGB
        ↓
MediaPipe recebe o frame e detecta a mão
        ↓
MediaPipe retorna 21 landmarks (pontos x, y, z)
        ↓
Código analisa os pontos e classifica o gesto
        ↓
Imagem correspondente ao gesto é colada no frame
        ↓
OpenCV exibe o frame final na janela
        ↓
(repete para o próximo frame)
```

Esse ciclo ocorre dezenas de vezes por segundo, criando a sensação de processamento em tempo real.

---

## Conceito de Landmarks

Landmarks são os 21 pontos que o MediaPipe mapeia sobre a mão detectada. Cada ponto representa uma articulação específica e possui coordenadas `x`, `y` e `z`, todas normalizadas entre `0.0` e `1.0` (proporcionais ao tamanho do frame).

```
        8   12  16  20
        |   |   |   |
        7   11  15  19
        |   |   |   |
        6   10  14  18
         \  |   |  /
          5  9  13
            \|/
             0  ← pulso
```

| Dedo      | Ponta | Nó do meio | Base |
|-----------|-------|------------|------|
| Polegar   | 4     | 3          | 2    |
| Indicador | 8     | 7          | 6    |
| Médio     | 12    | 11         | 10   |
| Anelar    | 16    | 15         | 14   |
| Mindinho  | 20    | 19         | 18   |

**Como saber se um dedo está levantado:**
O eixo Y da imagem cresce de cima para baixo. Se a ponta do dedo (ex: ponto `8`) tem Y *menor* que o nó (ponto `6`), o dedo está levantado — pois está mais alto na tela.

```python
dedo_levantado = landmarks[8].y < landmarks[6].y  # True = levantado
```

---

## Pré-requisitos

- Sistema operacional: Windows, macOS ou Linux
- Webcam conectada ou embutida
- [Python 3.11](https://www.python.org/downloads/release/python-3119/) instalado
  - Durante a instalação, marque **"Add Python 3.11 to PATH"**
  - Não é necessário desinstalar outras versões do Python

---

## Instalação passo a passo

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/projeto-gestos.git
cd projeto-gestos
```

Ou baixe o ZIP pelo GitHub e extraia na pasta desejada.

### 2. Instale as dependências com Python 3.11

```bash
py -3.11 -m pip install -r requirements.txt
```

> **Por que `py -3.11`?**
> Se você tiver múltiplas versões do Python instaladas, o comando `py -3.11` garante que está usando a versão correta. Usar apenas `python` pode chamar outra versão incompatível.

### 3. Baixe o modelo do MediaPipe

O MediaPipe 0.10+ não vem com o modelo embutido. É necessário baixar o arquivo `.task` separadamente. Execute o comando abaixo dentro da pasta do projeto — ele vai salvar o arquivo `hand_landmarker.task` no local correto:

```bash
py -3.11 -c "import requests; open('hand_landmarker.task','wb').write(requests.get('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task').content)"
```

### 4. Adicione as imagens (opcional)

Crie a pasta `imagens/` e coloque dentro dela os arquivos com os nomes exatos:

```
imagens/imagem_apontar.jpg
imagens/imagem_paz.jpg
imagens/imagem_punho.jpg
imagens/imagem_aberta.jpg
```

Pode usar qualquer imagem `.jpg` que quiser associar a cada gesto.

---

## Como rodar

```bash
py -3.11 tutorial_gestos.py
```

Uma janela será aberta com o vídeo da webcam. Para encerrar, clique na janela e pressione **Q** ou **ESC**.

---

## Gestos reconhecidos

| Gesto        | Como fazer                          | Arquivo de imagem             |
|--------------|-------------------------------------|-------------------------------|
| `APONTAR`    | Só o indicador levantado            | `imagens/imagem_apontar.jpg`  |
| `PAZ`        | Indicador + médio levantados        | `imagens/imagem_paz.jpg`      |
| `PUNHO`      | Mão fechada, nenhum dedo levantado  | `imagens/imagem_punho.jpg`    |
| `MAO_ABERTA` | Todos os quatro dedos levantados    | `imagens/imagem_aberta.jpg`   |

---

## Funções do código

### `callback_resultado(result, output_image, timestamp_ms)`
Função chamada automaticamente pelo MediaPipe toda vez que um frame é processado. Atualiza a variável global `resultado_atual` com os landmarks detectados no frame mais recente.

---

### `dedo_levantado(lm, ponta, no)`
Verifica se um dedo específico está levantado comparando a posição Y da ponta com a posição Y do nó.

| Parâmetro | Tipo   | Descrição                          |
|-----------|--------|------------------------------------|
| `lm`      | lista  | Lista dos 21 landmarks da mão      |
| `ponta`   | int    | Índice do landmark da ponta do dedo|
| `no`      | int    | Índice do landmark do nó do dedo   |

**Retorna:** `True` se o dedo estiver levantado, `False` caso contrário.

---

### `reconhecer_gesto(landmarks)`
Analisa o estado dos quatro dedos principais (indicador, médio, anelar, mindinho) e retorna o nome do gesto correspondente.

| Parâmetro   | Tipo  | Descrição                        |
|-------------|-------|----------------------------------|
| `landmarks` | lista | Lista dos 21 landmarks da mão    |

**Retorna:** `str` com o nome do gesto (`"APONTAR"`, `"PAZ"`, `"PUNHO"`, `"MAO_ABERTA"`) ou `None` se a combinação não estiver mapeada.

---

### `mostrar_imagem_reacao(frame, gesto)`
Carrega a imagem associada ao gesto, redimensiona para 300×300 pixels e cola no canto superior direito do frame atual.

| Parâmetro | Tipo   | Descrição                                        |
|-----------|--------|--------------------------------------------------|
| `frame`   | array  | Frame atual da webcam (array numpy do OpenCV)    |
| `gesto`   | str    | Nome do gesto reconhecido                        |

Se a imagem não existir na pasta, a função retorna sem fazer nada.

---

### `desenhar_landmarks(frame, landmarks)`
Desenha os 21 pontos e as conexões entre eles diretamente no frame usando OpenCV puro, sem depender das funções de desenho do MediaPipe.

| Parâmetro   | Tipo   | Descrição                                     |
|-------------|--------|-----------------------------------------------|
| `frame`     | array  | Frame atual da webcam                         |
| `landmarks` | lista  | Lista dos 21 landmarks com coordenadas x, y, z|

Converte as coordenadas normalizadas (0.0 a 1.0) para pixels multiplicando pelo tamanho do frame antes de desenhar.

---

## Como adicionar um novo gesto

**Passo 1 —** Coloque a imagem na pasta `imagens/`:
```
imagens/imagem_joinha.jpg
```

**Passo 2 —** Registre a imagem no dicionário `IMAGENS` no início do script:
```python
IMAGENS = {
    "APONTAR":    cv2.imread("imagens/imagem_apontar.jpg"),
    "PAZ":        cv2.imread("imagens/imagem_paz.jpg"),
    "PUNHO":      cv2.imread("imagens/imagem_punho.jpg"),
    "MAO_ABERTA": cv2.imread("imagens/imagem_aberta.jpg"),
    "JOINHA":     cv2.imread("imagens/imagem_joinha.jpg"),  # novo
}
```

**Passo 3 —** Adicione a condição na função `reconhecer_gesto()`:
```python
# Joinha: polegar para cima, demais dedos fechados
# O polegar usa eixo X: ponta (4) mais à esquerda que a base (3) = levantado
polegar = landmarks[4].x < landmarks[3].x
if polegar and not indicador and not medio and not anelar and not mindinho:
    return "JOINHA"
```

---

## Erros comuns

**`module 'mediapipe' has no attribute 'solutions'`**
Versão do MediaPipe incompatível com a versão do Python. Certifique-se de estar usando Python 3.11 com `py -3.11`.

**`No module named 'cv2'`**
OpenCV foi instalado em outra versão do Python. Reinstale com:
```bash
py -3.11 -m pip install opencv-python
```

**`Requirement already satisfied` mas o erro persiste**
O pip está instalando no Python errado. Sempre use `py -3.11 -m pip install` ao invés de apenas `pip install`.

**`can't open/read file: imagens/imagem_apontar.jpg`**
O arquivo não foi encontrado. Verifique se a pasta `imagens/` existe dentro da pasta do projeto e se os nomes dos arquivos estão corretos. O programa funciona normalmente sem as imagens.

**A janela não fecha com Q**
O Q só funciona quando a janela do OpenCV está em foco. Clique na janela do vídeo primeiro, depois pressione **Q** ou **ESC**.

---

## Referências

- [MediaPipe Hand Landmarker — Google](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Python 3.11 Downloads](https://www.python.org/downloads/release/python-3119/)
