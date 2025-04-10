import cv2
from ultralytics import YOLO
import pyautogui as pa




p1 = (0,300)
p2 = (1280,0)



# Carrega o modelo pré-treinado (YOLOv8n = nano, bem leve)
model = YOLO("yolov8s.pt")  # ou yolov8s.pt para versão small

# Fonte do vídeo: 0 = webcam, ou pode usar RTSP/HTTP/arquivo
video = cv2.VideoCapture("rtsp://admin:admin@172.16.0.180/media/video1")

# Força resolução da webcam (HD)
line_y = 300
offset = 20  # margem de erro

# Lista de IDs que já cruzaram
crossed_ids = set()

while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (1280,720))
    if not ret:
        break

    results = model.track(frame, persist=True, classes=[0])  # habilita rastreamento por ID
    annotated_frame = results[0].plot()

    count = 0
    if results[0].boxes.id is not None:
        for box, cls, track_id in zip(results[0].boxes.xyxy,
                                      results[0].boxes.cls,
                                      results[0].boxes.id):
            if int(cls) != 0:  # só pessoa
                continue

            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # centro do bounding box

            if (line_y - offset) < cy < (line_y + offset):
                if int(track_id) not in crossed_ids:
                    crossed_ids.add(int(track_id))
                    count += 1  # incrementa só uma vez por ID

            # desenha o centro
            cv2.circle(annotated_frame, (cx, cy), 5, (255, 0, 0), -1)

    # desenha linha virtual
    cv2.line(annotated_frame, (0, line_y), (annotated_frame.shape[1], line_y), (0, 255, 255), 2)

    # total de pessoas que cruzaram
    cv2.putText(annotated_frame, f'Cruzaram: {len(crossed_ids)}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Contagem de Pessoas na Linha", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()