import cv2
import numpy as np

# ----------- CAMERA EXTERNA -----------
camera_id = 1   # se não abrir, troque para 0, 2 ou 3
video = cv2.VideoCapture(camera_id)

# Deixar a câmera mais aberta (resolução maior)
video.set(3, 1920)  # largura
video.set(4, 1080)  # altura

# ----------- ZOOM DIGITAL (ABRIR IMAGEM) -----------
ZOOM = 0.75   # 0.75 = imagem mais aberta | 1.0 = normal

# ----------- VAGAS SEPARADAS -----------
# Ajustado para ficar igual a sua placa, 3 em cima e 3 em baixo

vaga1 = [205, 130, 260, 100]
vaga2 = [550, 125, 260, 105]
vaga3 = [930, 115, 260, 110]

vaga4 = [65, 550, 290, 160]
vaga5 = [475, 550, 350, 160]
vaga6 = [970, 550, 360, 160]

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6]

# ----------- TELA CHEIA -----------
cv2.namedWindow("Estacionamento", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Estacionamento", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:

    check, img = video.read()
    if not check:
        print("Erro ao acessar a webcam externa.")
        break

    # Zoom digital para abrir mais a imagem
    h, w = img.shape[:2]
    img = cv2.resize(img, (int(w * ZOOM), int(h * ZOOM)))

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgGray, 255,
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 25, 10)
    imgBlur = cv2.medianBlur(imgTh, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDil = cv2.dilate(imgBlur, kernel)

    vagasLivres = 0

    # ----------- LOOP DAS 6 VAGAS -----------
    for x, y, w, h in vagas:
        recorte = imgDil[y:y+h, x:x+w]
        branco = cv2.countNonZero(recorte)

        # Mostra valor para depuração
        cv2.putText(img, str(branco), (x, y+h-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # Se muitos pixels brancos = carro
        if branco > 3000:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
        else:
            vagasLivres += 1
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # Caixa superior
    cv2.rectangle(img, (10, 10), (400, 70), (255, 0, 0), -1)
    cv2.putText(img, f"LIVRE: {vagasLivres}/6", (25, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 4)

    # Mostrar imagem final
    cv2.imshow("Estacionamento", img)

    # Pressionar "q" para sair
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
