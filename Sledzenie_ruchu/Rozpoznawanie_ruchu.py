import cv2
import math
import time
import sys
import os
import threading
import numpy as np
from flask import Flask, Response, request
import signal

aktualny_folder = os.path.dirname(os.path.abspath(__file__))
folder_glowny = os.path.dirname(aktualny_folder)
folder_komunikacji = os.path.join(folder_glowny, 'KomunikacjaGlosowa')
sys.path.append(folder_komunikacji)

from komunikacja_glosowa import MowaTrenera, SluchTrenera, czy_komunikacja_zostala_zainicjalizowana

app = Flask(__name__)

aktualna_klatka_przod = None
aktualna_klatka_bok = None
zamien_kamery = False
trening_rozpoczety = False

def generuj_obraz_brak_kamery():
    puste_tlo = np.zeros((720, 1280, 3), dtype=np.uint8)
    rozmiar_tekstu = cv2.getTextSize("BRAK KAMERY / NIEPODLACZONA", cv2.FONT_HERSHEY_SIMPLEX, 2, 5)[0]
    cv2.putText(puste_tlo, "BRAK KAMERY / NIEPODLACZONA",
                ((1280 - rozmiar_tekstu[0]) // 2, (720 + rozmiar_tekstu[1]) // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    return puste_tlo

CZAS_STABILIZACJI = 1.0
CZAS_COOLDOWN = 4.0
TOLERANCJA_ZLEJ_POSTAWY_SEKUNDY = 1.0

def analizuj_martwy_ciag(punkty, punkty_bok, mp_pozycja):
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

def watek_kamery():
    global aktualna_klatka_przod, aktualna_klatka_bok, zamien_kamery

    from mediapipe.python.solutions import pose as mp_pose
    from mediapipe.python.solutions import drawing_utils as mp_drawing

    mp_pozycja = mp_pose
    mp_rysowanie = mp_drawing

    pozycja = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pozycja_bok = mp_pozycja.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    faza_ruchu = "GORA"
    licznik_powtorzen = 0
    brak_bledu_cwiczenia = True
    cel_powtorzen = 5
    komunikat = ""

    ostatni_komunikat_wykryty = ""
    czas_rozpoczecia_komunikatu = 0.0
    ostatni_powiedziany_komunikat = ""
    czas_ostatniego_mowienia = 0.0

    czas_rozpoczecia_bledu = 0.0

    global trening_rozpoczety

    mowa = MowaTrenera()
    sluch = SluchTrenera()
    if czy_komunikacja_zostala_zainicjalizowana(mowa, sluch):
        print("Moduły głosowe gotowe.")

    witaj_powiedziane = False

    film_przod = cv2.VideoCapture(0)
    film_przod.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    film_przod.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    film_bok = cv2.VideoCapture(1)
    film_bok.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    film_bok.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        if not film_przod.isOpened() or not film_bok.isOpened():
            obraz_bledu = generuj_obraz_brak_kamery()
            aktualna_klatka_przod = obraz_bledu
            aktualna_klatka_bok = obraz_bledu

            time.sleep(1)
            if not film_przod.isOpened():
                film_przod = cv2.VideoCapture(0)
                film_przod.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                film_przod.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            if not film_bok.isOpened():
                film_bok = cv2.VideoCapture(1)
                film_bok.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                film_bok.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            continue

        if not sluch.czy_dziala():
            mowa.powiedz("Zamykam program.")
            time.sleep(2)
            break

        sukces_przod, nowa_klatka_przod = film_przod.read()
        sukces_bok, nowa_klatka_bok = film_bok.read()

        if not sukces_przod or not sukces_bok:
            print("Nie udało się pobrać obrazu z kamer")
            film_przod.release()
            film_bok.release()
            continue

        if sluch.czy_jest_pauza():
            if 'klatka' in locals() and 'klatka_bok' in locals():
                klatka_pauza = klatka.copy()
                rozmiar_tekstu = cv2.getTextSize("PAUZA", cv2.FONT_HERSHEY_SIMPLEX, 3, 6)[0]
                cv2.putText(klatka_pauza, "PAUZA", ((klatka_pauza.shape[1] - rozmiar_tekstu[0]) // 2, (klatka_pauza.shape[0] + rozmiar_tekstu[1]) // 2),cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 6)
                aktualna_klatka_przod = klatka_pauza
                aktualna_klatka_bok = klatka_bok
            continue

        if sluch.sprawdz_i_wyczysc_reset():
            licznik_powtorzen = 0
            mowa.powiedz("Zeruję licznik powtórzeń.")

        if sluch.sprawdz_i_wyczysc_przelaczenie():
            zamien_kamery = not zamien_kamery
            mowa.powiedz("Zmieniam widok")

        if sluch.sprawdz_i_wyczysc_dodanie_powtorzenia():
            cel_powtorzen += 1
            mowa.powiedz(f"Zwiększono cel powtórzeń do {cel_powtorzen}")

        if sluch.sprawdz_i_wyczysc_odjecie_powtorzenia():
            if cel_powtorzen > 1:
                cel_powtorzen -= 1
                mowa.powiedz(f"Zmniejszono cel powtórzeń do {cel_powtorzen}")
            else:
                mowa.powiedz("Cel powtórzeń nie może być mniejszy niż jeden")

        klatka = cv2.flip(nowa_klatka_przod, 1)
        klatka_bok = nowa_klatka_bok

        klatka_rgb = cv2.cvtColor(klatka, cv2.COLOR_BGR2RGB)
        klatka_bok_rgb = cv2.cvtColor(klatka_bok, cv2.COLOR_BGR2RGB)

        wynik = pozycja.process(klatka_rgb)
        wynik_bok = pozycja_bok.process(klatka_bok_rgb)

        if trening_rozpoczety:
            if not witaj_powiedziane:
                mowa.powiedz("Witaj w asystencie martwego ciągu. Przygotuj się do ćwiczenia.")
                witaj_powiedziane = True

            wynik = pozycja.process(klatka_rgb)
            wynik_bok = pozycja_bok.process(klatka_bok_rgb)

            if wynik.pose_landmarks and wynik_bok.pose_landmarks:
                punkty_przod = wynik.pose_landmarks.landmark
                punkty_bok = wynik_bok.pose_landmarks.landmark
                mp_rysowanie.draw_landmarks(klatka, wynik.pose_landmarks, mp_pozycja.POSE_CONNECTIONS)
                mp_rysowanie.draw_landmarks(klatka_bok, wynik_bok.pose_landmarks, mp_pozycja.POSE_CONNECTIONS)
                komunikat, y_dloni, y_bioder, y_kolan, postawa_poprawna = analizuj_martwy_ciag(punkty_przod, punkty_bok,
                                                                                               mp_pozycja)

                aktualny_czas = time.time()

                if komunikat != ostatni_komunikat_wykryty:
                    ostatni_komunikat_wykryty = komunikat
                    czas_rozpoczecia_komunikatu = aktualny_czas

                if aktualny_czas - czas_rozpoczecia_komunikatu >= CZAS_STABILIZACJI:
                    if komunikat == "Poprawna postawa":
                        if ostatni_powiedziany_komunikat != "Poprawna postawa":
                            mowa.powiedz("Poprawna postawa")
                            ostatni_powiedziany_komunikat = "Poprawna postawa"
                            czas_ostatniego_mowienia = aktualny_czas
                    else:
                        if (ostatni_powiedziany_komunikat != komunikat) or (
                                aktualny_czas - czas_ostatniego_mowienia >= CZAS_COOLDOWN):
                            mowa.powiedz(komunikat)
                            ostatni_powiedziany_komunikat = komunikat
                            czas_ostatniego_mowienia = aktualny_czas

                if faza_ruchu == "GORA":
                    if y_dloni > y_kolan:
                        faza_ruchu = "DOL"
                        brak_bledu_cwiczenia = True
                        czas_rozpoczecia_bledu = 0.0
                elif faza_ruchu == "DOL":
                    if not postawa_poprawna:
                        if czas_rozpoczecia_bledu == 0.0:
                            czas_rozpoczecia_bledu = aktualny_czas
                        elif aktualny_czas - czas_rozpoczecia_bledu >= TOLERANCJA_ZLEJ_POSTAWY_SEKUNDY:
                            brak_bledu_cwiczenia = False
                    else:
                        czas_rozpoczecia_bledu = 0.0

                    if y_dloni < y_bioder:
                        faza_ruchu = "GORA"
                        if brak_bledu_cwiczenia:
                            licznik_powtorzen += 1
                            mowa.powiedz("Powtórzenie zaliczono")
                        else:
                            mowa.powiedz("Powtórzenia nie zaliczono")

        cv2.putText(klatka, f"Wskazowka: {komunikat}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(klatka, f"Faza: {faza_ruchu}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(klatka, f"Powtorzenia: {licznik_powtorzen}", (20, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(klatka, f"Pozostalo: {cel_powtorzen - licznik_powtorzen}", (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)

        if licznik_powtorzen >= cel_powtorzen:
            rozmiar_tekstu = cv2.getTextSize("UDALO SIE!", cv2.FONT_HERSHEY_SIMPLEX, 3, 6)[0]
            cv2.putText(klatka, "UDALO SIE!",((klatka.shape[1] - rozmiar_tekstu[0]) // 2, (klatka.shape[0] + rozmiar_tekstu[1]) // 2), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 6)

            aktualna_klatka_przod = klatka
            aktualna_klatka_bok = klatka_bok

            time.sleep(3)
            licznik_powtorzen = 0
            trening_rozpoczety = False
            witaj_powiedziane = False
            continue
        else:
            pass

        aktualna_klatka_przod = klatka
        aktualna_klatka_bok = klatka_bok

    film_przod.release()
    film_bok.release()
    mowa.zamknij()
    sluch.zamknij()

threading.Thread(target=watek_kamery, daemon=True).start()

@app.route('/api/start_training', methods=['POST'])
def start_training():
    global trening_rozpoczety
    trening_rozpoczety = True
    return {"status": "success", "message": "Trening rozpoczęty."}

@app.route('/api/training_status', methods=['GET'])
def training_status():
    global trening_rozpoczety
    return {"trening_rozpoczety": trening_rozpoczety}

@app.route('/api/video_feed')
def video_feed():
    widok = request.args.get('widok', 'przod')

    global zamien_kamery
    if zamien_kamery:
        if widok == "przod":
            widok = "bok"
        else:
            widok = "przod"

    klatka_do_wyslania = aktualna_klatka_przod if widok == "przod" else aktualna_klatka_bok

    if klatka_do_wyslania is None:
        klatka_do_wyslania = generuj_obraz_brak_kamery()

    ret, jpeg = cv2.imencode('.jpg', klatka_do_wyslania)

    return Response(jpeg.tobytes(), mimetype='image/jpeg')

def obsluga_zakonczenia(sig, frame):
    print("\nZamykanie programu (Ctrl+C)...")
    os._exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, obsluga_zakonczenia)
    print("Serwer wideo z analiza ruchu uruchomiony! Oczekuje na polaczenie z Javy na porcie 5001...")
    app.run(debug=False, port=5001, use_reloader=False)