import cv2
import mediapipe as mp

mp_pozycja = mp.solutions.pose
mp_rysowanie = mp.solutions.drawing_utils
film = cv2.VideoCapture(0)
pozycja = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def analizuj_martwy_ciag(punkty):
    L_ramie = punkty[mp_pozycja.PoseLandmark.LEFT_SHOULDER]
    P_ramie = punkty[mp_pozycja.PoseLandmark.RIGHT_SHOULDER]
    L_reka = punkty[mp_pozycja.PoseLandmark.LEFT_WRIST]
    P_reka = punkty[mp_pozycja.PoseLandmark.RIGHT_WRIST]
    L_stopa = punkty[mp_pozycja.PoseLandmark.LEFT_ANKLE]
    P_stopa = punkty[mp_pozycja.PoseLandmark.RIGHT_ANKLE]
    L_kolano = punkty[mp_pozycja.PoseLandmark.LEFT_KNEE]
    P_kolano = punkty[mp_pozycja.PoseLandmark.RIGHT_KNEE]

    szerokosc_ramion = abs(L_ramie.x - P_ramie.x)
    szerokosc_stop = abs(L_stopa.x - P_stopa.x)
    szerokosc_dloni = abs(L_reka.x - P_reka.x)

    przesuniecie_L_kolana = abs(L_kolano.x - L_stopa.x)
    przesuniecie_P_kolana = abs(P_kolano.x - P_stopa.x)

    komunikat = ""
    tolerancja_kolan = 0.06 
    if szerokosc_stop > szerokosc_ramion * 1.2:
        komunikat = "Zwez stopy"
    elif szerokosc_stop < szerokosc_ramion * 0.8:
        komunikat = "Rozszerz stopy"
    elif szerokosc_dloni < szerokosc_stop * 1.05:
        komunikat = "Zlap sztange szerzej"
    elif szerokosc_dloni > szerokosc_ramion * 1.4:
        komunikat = "Zlap sztange weziej"
    elif przesuniecie_L_kolana > tolerancja_kolan or przesuniecie_P_kolana > tolerancja_kolan:
        komunikat = "Pilnuj kolan musza byc nad stopami"
    else:
        komunikat = "Poprawna postawa"
    return komunikat

while film.isOpened():
    sukces, klatka = film.read()
    if not sukces:
        print("Nie udało się pobrać obrazu z kamery")
        break
    klatka_rgb = cv2.cvtColor(klatka, cv2.COLOR_BGR2RGB)
    wynik = pozycja.process(klatka_rgb)
    if wynik.pose_landmarks:
        punkty = wynik.pose_landmarks.landmark
        mp_rysowanie.draw_landmarks(klatka, wynik.pose_landmarks, mp_pozycja.POSE_CONNECTIONS)
        komunikat = analizuj_martwy_ciag(punkty)
        cv2.putText(klatka, f"Wskazowka: {komunikat}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow("Asystent Martwego Ciagu", klatka)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
film.release()
cv2.destroyAllWindows()