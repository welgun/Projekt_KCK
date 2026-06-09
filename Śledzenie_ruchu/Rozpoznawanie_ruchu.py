import cv2
import mediapipe as mp
import math
mp_pozycja = mp.solutions.pose
mp_rysowanie = mp.solutions.drawing_utils
film = cv2.VideoCapture(0)
film_bok = cv2.VideoCapture(1)
cv2.namedWindow("Asystent Martwego Ciagu", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Asystent Martwego Ciagu", 1280, 720)
cv2.namedWindow("Widok Boczny", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Widok Boczny", 1280, 720)
pozycja = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pozycja_bok = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
faza_ruchu = "GORA"
licznik_powtorzen = 0
brak_bledu_cwiczenia = True
cel_powtorzen = 5
komunikat = ""
def analizuj_martwy_ciag(punkty, punkty_bok):
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
    ucho = punkty_bok[mp_pozycja.PoseLandmark.LEFT_EAR]
    ramie_b = punkty_bok[mp_pozycja.PoseLandmark.LEFT_SHOULDER]
    biodro_b = punkty_bok[mp_pozycja.PoseLandmark.LEFT_HIP]
    szerokosc_ramion = abs(L_ramie.x - P_ramie.x)
    szerokosc_stop = abs(L_stopa.x - P_stopa.x)
    szerokosc_dloni = abs(L_reka.x - P_reka.x)
    przesuniecie_L_kolana = abs(L_kolano.x - L_stopa.x)
    przesuniecie_P_kolana = abs(P_kolano.x - P_stopa.x)

    plecy_proste = True
    kat1 = math.atan2(ucho.y - ramie_b.y, ucho.x - ramie_b.x)
    kat2 = math.atan2(biodro_b.y - ramie_b.y, biodro_b.x - ramie_b.x)
    kat = math.degrees(abs(kat1 - kat2))
    if kat > 180.0:
        kat = 360.0 - kat
    if kat < 140:
        plecy_proste = False

    poprawna_postawa = True
    komunikat = ""
    tolerancja_kolan = 0.06

    if not plecy_proste:
        komunikat = "Wyprostuj plecy"
        poprawna_postawa = False
    elif szerokosc_stop > szerokosc_ramion * 1.2:
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

while film.isOpened() and film_bok.isOpened():
    sukces, klatka = film.read()
    sukces_bok, klatka_bok = film_bok.read()
    if not sukces or not sukces_bok:
        print("Nie udało się pobrać obrazu z kamery")
        break
    klatka = cv2.flip(klatka, 1)
    klatka_rgb = cv2.cvtColor(klatka, cv2.COLOR_BGR2RGB)
    klatka_bok_rgb = cv2.cvtColor(klatka_bok, cv2.COLOR_BGR2RGB)
    wynik = pozycja.process(klatka_rgb)
    wynik_bok = pozycja_bok.process(klatka_bok_rgb)
    if wynik.pose_landmarks and wynik_bok.pose_landmarks:
        punkty_przod = wynik.pose_landmarks.landmark
        punkty_bok = wynik_bok.pose_landmarks.landmark
        mp_rysowanie.draw_landmarks(klatka, wynik.pose_landmarks, mp_pozycja.POSE_CONNECTIONS)
        mp_rysowanie.draw_landmarks(klatka_bok, wynik_bok.pose_landmarks, mp_pozycja.POSE_CONNECTIONS)
        komunikat, y_dloni, y_bioder, y_kolan, postawa_poprawna = analizuj_martwy_ciag(punkty_przod, punkty_bok)
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
    cv2.putText(klatka, f"Pozostalo: {cel_powtorzen - licznik_powtorzen}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    if licznik_powtorzen >= cel_powtorzen:
        rozmiar_tekstu = cv2.getTextSize("UDALO SIE!", cv2.FONT_HERSHEY_SIMPLEX, 3, 6)[0]
        cv2.putText(klatka, "UDALO SIE!", ((klatka.shape[1] - rozmiar_tekstu[0]) // 2, (klatka.shape[0] + rozmiar_tekstu[1]) // 2), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)
        cv2.imshow("Asystent Martwego Ciagu", klatka)
        cv2.imshow("Widok Boczny", klatka_bok)
        cv2.waitKey(3000)
        break
    cv2.imshow("Asystent Martwego Ciagu", klatka)
    cv2.imshow("Widok Boczny", klatka_bok)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
film.release()
film_bok.release()
cv2.destroyAllWindows()