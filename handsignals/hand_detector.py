# Script para detección de manos y porcentaje de apertura
# Usando OpenCV y MediaPipe

import cv2
import mediapipe as mp
import json

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Configuración del detector de manos
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Índices de los landmarks de las puntas de los dedos
# Pulgar: 4, Índice: 8, Medio: 12, Anular: 16, Meñique: 20
FINGER_TIPS = [4, 8, 12, 16, 20]
# Índices de los nudillos (para comparar si el dedo está extendido)
FINGER_PIPS = [2, 6, 10, 14, 18]


def count_extended_fingers(hand_landmarks, handedness):
    """
    Cuenta cuántos dedos están extendidos.
    Retorna un valor entre 0 y 5.
    """
    landmarks = hand_landmarks.landmark
    fingers_extended = 0

    # Verificar el pulgar (comparación en eje X, depende de la mano)
    # Para la mano derecha: pulgar extendido si TIP.x < IP.x
    # Para la mano izquierda: pulgar extendido si TIP.x > IP.x
    is_right_hand = handedness.classification[0].label == "Right"

    if is_right_hand:
        # En imagen espejada, mano derecha tiene pulgar a la izquierda
        if landmarks[4].x < landmarks[3].x:
            fingers_extended += 1
    else:
        # Mano izquierda tiene pulgar a la derecha
        if landmarks[4].x > landmarks[3].x:
            fingers_extended += 1

    # Verificar los otros 4 dedos (comparación en eje Y)
    # Un dedo está extendido si la punta (TIP) está más arriba que el nudillo (PIP)
    # En la imagen, Y menor = más arriba
    for tip_idx in [8, 12, 16, 20]:
        pip_idx = tip_idx - 2  # El PIP está 2 posiciones antes del TIP
        if landmarks[tip_idx].y < landmarks[pip_idx].y:
            fingers_extended += 1

    return fingers_extended


def calculate_hand_openness(fingers_extended):
    """
    Calcula el porcentaje de apertura de la mano.
    0 dedos = 0% (mano cerrada)
    5 dedos = 100% (mano completamente abierta)
    """
    return int((fingers_extended / 5) * 100)


def get_hand_bounding_box(hand_landmarks, frame_width, frame_height):
    """
    Calcula el bounding box (coordenadas) de la mano detectada.
    Retorna: (x_min, y_min, x_max, y_max) en píxeles
    """
    x_coords = []
    y_coords = []

    for landmark in hand_landmarks.landmark:
        x_coords.append(landmark.x)
        y_coords.append(landmark.y)

    # Convertir coordenadas normalizadas (0-1) a píxeles
    x_min = int(min(x_coords) * frame_width)
    x_max = int(max(x_coords) * frame_width)
    y_min = int(min(y_coords) * frame_height)
    y_max = int(max(y_coords) * frame_height)

    # Agregar un margen
    margin = 20
    x_min = max(0, x_min - margin)
    y_min = max(0, y_min - margin)
    x_max = min(frame_width, x_max + margin)
    y_max = min(frame_height, y_max + margin)

    return x_min, y_min, x_max, y_max


def get_hand_center(hand_landmarks, frame_width, frame_height):
    """
    Calcula el centro de la mano (usando el landmark de la muñeca como referencia).
    Retorna: (center_x, center_y) en píxeles
    """
    # Landmark 0 es la muñeca, landmark 9 es el centro de la palma
    wrist = hand_landmarks.landmark[0]
    middle_base = hand_landmarks.landmark[9]

    # Calcular el centro como promedio entre muñeca y base del dedo medio
    center_x = int(((wrist.x + middle_base.x) / 2) * frame_width)
    center_y = int(((wrist.y + middle_base.y) / 2) * frame_height)

    return center_x, center_y


def main():
    # Iniciar captura de video
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return

    print("Presiona 'q' para salir")
    print("-" * 40)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame")
            break

        # Voltear la imagen horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)

        # Convertir BGR a RGB (MediaPipe usa RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Procesar la imagen
        results = hands.process(rgb_frame)

        # Obtener dimensiones del frame
        frame_height, frame_width = frame.shape[:2]

        # Verificar si se detectó una mano
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Dibujar los landmarks en la imagen
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                # Contar dedos extendidos
                fingers = count_extended_fingers(hand_landmarks, handedness)

                # Calcular porcentaje de apertura
                openness = calculate_hand_openness(fingers)

                # Obtener coordenadas de la mano
                x_min, y_min, x_max, y_max = get_hand_bounding_box(
                    hand_landmarks, frame_width, frame_height
                )
                center_x, center_y = get_hand_center(
                    hand_landmarks, frame_width, frame_height
                )

                # Dibujar bounding box en la imagen
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 255), -1)

                # Crear resultado en formato JSON
                result = {
                    "mano_detectada": True,
                    "apertura_porcentaje": openness,
                    "dedos_extendidos": fingers,
                    "coordenadas": {
                        "bounding_box": {
                            "x_min": x_min,
                            "y_min": y_min,
                            "x_max": x_max,
                            "y_max": y_max,
                            "ancho": x_max - x_min,
                            "alto": y_max - y_min
                        },
                        "centro": {
                            "x": center_x,
                            "y": center_y
                        }
                    },
                    "mano": handedness.classification[0].label
                }

                # Imprimir resultado en JSON
                print(json.dumps(result, ensure_ascii=False))

                # Mostrar información en la imagen
                cv2.putText(frame, f"Mano: SI ({handedness.classification[0].label})", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Apertura: {openness}%", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Dedos: {fingers}", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Centro: ({center_x}, {center_y})", (10, 120),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            # No se detectó ninguna mano
            result = {
                "mano_detectada": False,
                "apertura_porcentaje": None,
                "dedos_extendidos": None,
                "coordenadas": None,
                "mano": None
            }
            print(json.dumps(result, ensure_ascii=False))
            cv2.putText(frame, "Mano: NO", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Mostrar la imagen
        cv2.imshow("Detector de Manos", frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    hands.close()


if __name__ == "__main__":
    main()
