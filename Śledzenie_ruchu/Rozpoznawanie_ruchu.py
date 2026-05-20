import cv2
import mediapipe as mp

mp_pozycja = mp.solutions.pose
mp_rysowanie = mp.solutions.drawing_utils
film = cv2.VideoCapture(0)
pozycja = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

faza_ruchu = "GORA"
licznik_powtorzen = 0
brak_bledu_cwiczenia = True

def analizuj_martwy_ciag(punkty):
    L_ramie = punkty[mp_pozycja.PoseLandmark.LEFT_SHOULDER]
    P_ramie = punkty[mp_pozycja.PoseLandmark.RIGHT_SHOULDER]
    L_reka = punkty[mp_pozycja.PoseLandmark.LEFT_WRIST]
    P_reka = punkty[mp_pozycja.PoseLandmark.RIGHT_WRIST]
    L_stopa = punkty[mp_pozycja.PoseLandmark.LEFT_ANKLE]
    P_stopa = punkty[mp_pozycja.PoseLandmark.RIGHT_ANKLE]
    L_kolano = punkty[mp_pozycja.PoseLandmark.LEFT_KNEE]
    P_kolano = punkty[mp_pozycja.PoseLandmark.RIGHT_KNEE]
    L_biodro = punkty[mp_pozycja.PoseLandmark.LEFT_HIP]
    P_biodro = punkty[mp_pozycja.PoseLandmark.RIGHT_HIP]
    szerokosc_ramion = abs(L_ramie.x - P_ramie.x)
    szerokosc_stop = abs(L_stopa.x - P_stopa.x)
    szerokosc_dloni = abs(L_reka.x - P_reka.x)

    przesuniecie_L_kolana = abs(L_kolano.x - L_stopa.x)
    przesuniecie_P_kolana = abs(P_kolano.x - P_stopa.x)

    poprawna_postawa = True
    komunikat = ""
    tolerancja_kolan = 0.06 
    if szerokosc_stop > szerokosc_ramion * 1.2:
        komunikat = "Zwez stopy"
        poprawna_postawa = False
    elif szerokosc_stop < szerokosc_ramion * 0.8:
        komunikat = "Rozszerz stopy"
        poprawna_postawa = False
    elif szerokosc_dloni < szerokosc_stop * 1.05:
        komunikat = "Zlap sztange szerzej"
        poprawna_postawa = False
    elif szerokosc_dloni > szerokosc_ramion * 1.4:
        komunikat = "Zlap sztange weziej"
        poprawna_postawa = False
    elif przesuniecie_L_kolana > tolerancja_kolan or przesuniecie_P_kolana > tolerancja_kolan:
        komunikat = "Pilnuj kolan musza byc nad stopami"
        poprawna_postawa = False
    else:
        komunikat = "Poprawna postawa"
        poprawna_postawa = True

    wysokosc_dloni = (L_reka.y + P_reka.y) / 2
    wysokosc_bioder = (L_biodro.y + P_biodro.y) / 2
    wysokosc_kolan = (L_kolano.y + P_kolano.y) / 2
    return komunikat, wysokosc_dloni, wysokosc_bioder, wysokosc_kolan, poprawna_postawa

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
        komunikat, y_dloni, y_bioder, y_kolan, postawa_poprawna = analizuj_martwy_ciag(punkty)
        if faza_ruchu == "GORA":
            if y_dloni > y_kolan:
                faza_ruchu = "DOL"
                brak_bledu_cwiczenia = True     
        elif faza_ruchu == "DOL":
            if not postawa_poprawna:
                brak_bledu_cwiczenia = False
            if y_dloni < y_bioder:
                faza_ruchu = "GORA"
                if brak_bledu_cwiczenia:
                    licznik_powtorzen += 1
    cv2.putText(klatka, f"Wskazowka: {komunikat}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(klatka, f"Faza: {faza_ruchu}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(klatka, f"Powtorzenia: {licznik_powtorzen}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Asystent Martwego Ciagu", klatka)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
film.release()
cv2.destroyAllWindows()