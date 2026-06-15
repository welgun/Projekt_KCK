import cv2
import mediapipe as mp
import threading
import numpy as np
from flask import Flask, Response, request

app = Flask(__name__)

# Globalne zmienne do przechowywania najnowszych klatek
aktualna_klatka_przod = None
aktualna_klatka_bok = None

def generuj_obraz_brak_kamery():
    # Tworzy czarną klatkę 720p z napisem
    puste_tlo = np.zeros((720, 1280, 3), dtype=np.uint8)
    rozmiar_tekstu = cv2.getTextSize("BRAK KAMERY / NIEPODLACZONA", cv2.FONT_HERSHEY_SIMPLEX, 2, 5)[0]
    cv2.putText(puste_tlo, "BRAK KAMERY / NIEPODLACZONA", 
                ((1280 - rozmiar_tekstu[0]) // 2, (720 + rozmiar_tekstu[1]) // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    return puste_tlo

def watek_kamery():
    global aktualna_klatka_przod, aktualna_klatka_bok
    
    # BEZPOŚREDNIE IMPORTY (Rozwiązują problem braku atrybutu 'solutions')
    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing
    
    pozycja = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    # Automatyczne wykrywanie kamery
    film = cv2.VideoCapture(0)
    film.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    film.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while True:
        if not film.isOpened():
            # BRAK KAMERY - ustawiamy sztuczny obraz
            obraz_bledu = generuj_obraz_brak_kamery()
            aktualna_klatka_przod = obraz_bledu
            aktualna_klatka_bok = obraz_bledu
            cv2.waitKey(1000) # Czekamy sekunde przed ponowna proba
            film = cv2.VideoCapture(0) # Próbujemy podłączyć ponownie
            continue

        sukces, nowa_klatka = film.read()
        if not sukces:
            film.release()
            continue

        klatka = cv2.flip(nowa_klatka, 1)
        klatka_bok = klatka.copy()
        
        # Analiza sylwetki
        klatka_rgb = cv2.cvtColor(klatka, cv2.COLOR_BGR2RGB)
        wynik = pozycja.process(klatka_rgb)
        
        if wynik.pose_landmarks:
            mp_drawing.draw_landmarks(klatka, wynik.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            mp_drawing.draw_landmarks(klatka_bok, wynik.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Sztuczne nałożenie napisów dla testu
            #cv2.putText(klatka, "WIDOK FRONTOWY", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 250, 234), 2)
            #cv2.putText(klatka_bok, "WIDOK BOCZNY", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 250, 234), 2)

        aktualna_klatka_przod = klatka
        aktualna_klatka_bok = klatka_bok

# Uruchamiamy odczyt z kamery w tle
threading.Thread(target=watek_kamery, daemon=True).start()

def strumien_wideo(widok):
    global aktualna_klatka_przod, aktualna_klatka_bok
    while True:
        klatka_do_wyslania = aktualna_klatka_przod if widok == "przod" else aktualna_klatka_bok
        
        if klatka_do_wyslania is None:
            klatka_do_wyslania = generuj_obraz_brak_kamery()

        # Konwersja obrazu OpenCV (numpy array) na format JPEG
        ret, jpeg = cv2.imencode('.jpg', klatka_do_wyslania)
        frame = jpeg.tobytes()
        
        # Formatowanie jako strumień MJPEG (multipart)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Nasz nowy endpoint dla JavaFX
@app.route('/api/video_feed')
def video_feed():
    widok = request.args.get('widok', 'przod') 
    
    # Wybór odpowiedniej klatki z globalnych zmiennych
    klatka_do_wyslania = aktualna_klatka_przod if widok == "przod" else aktualna_klatka_bok
    
    if klatka_do_wyslania is None:
        klatka_do_wyslania = generuj_obraz_brak_kamery()

    # Szybka konwersja klatki OpenCV na zwykły plik JPEG w pamięci
    ret, jpeg = cv2.imencode('.jpg', klatka_do_wyslania)
    
    # Zwracamy to do Javy jako pojedynczy, standardowy obraz (image/jpeg)
    return Response(jpeg.tobytes(), mimetype='image/jpeg')

if __name__ == '__main__':
    print("Serwer wideo uruchomiony! Oczekuje na połączenie z Javy...")
    app.run(debug=False, port=5001)