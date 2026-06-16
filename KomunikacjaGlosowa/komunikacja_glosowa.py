import time
from piper.voice import PiperVoice
import vosk
import os
vosk.SetLogLevel(-1)
import pyaudio
import queue
import threading
import json


class BladKonfiguracjiMowy(Exception):
    pass


class MowaTrenera:
    def __init__(self):
        self.koniec_inicjalizacji = False
        self.kolejka_zdan = queue.Queue()
        self._skonfiguruj_glos()

        self.glowny_watek = threading.Thread(target=self._glowny_watek_mowy, daemon=False)
        self.glowny_watek.start()
        self.koniec_inicjalizacji = True

    def _skonfiguruj_glos(self):
        try:
            katalog_obecny = os.path.dirname(os.path.abspath(__file__))
            sciezka_modelu = os.path.join(katalog_obecny, "pl_PL-mc_speech-medium.onnx")

            self.glos = PiperVoice.load(sciezka_modelu)
            self.pyaudio_instance = pyaudio.PyAudio()

            self.strumien = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.glos.config.sample_rate,
                output=True
            )
        except Exception as e:
            raise BladKonfiguracjiMowy(f"Nie udalo sie skonfigurowac glosu: {e}") from e

    def powiedz(self, tekst):
        self.kolejka_zdan.put(tekst)

    def _glowny_watek_mowy(self):
        while True:
            tekst = self.kolejka_zdan.get()

            if tekst is None:
                break

            try:
                for chunk in self.glos.synthesize(tekst):
                    self.strumien.write(chunk.audio_int16_bytes)
            except Exception as e:
                print(f"Blad syntezy mowy: {e}")

    def zamknij(self):
        self.kolejka_zdan.put(None)
        self.glowny_watek.join()

        self.strumien.stop_stream()
        self.strumien.close()
        self.pyaudio_instance.terminate()


class BladKonfiguracjiSluchu(Exception):
    pass


class SluchTrenera:
    def __init__(self):
        self.koniec_inicjalizacji = False
        self.pauza = False
        self.zadanie_resetu = False
        self.zadanie_przelaczenia = False
        self.zadanie_dodania_powtorzenia = False
        self.zadanie_odjecia_powtorzenia = False
        self.zadanie_rozpoczecia_treningu = False

        katalog_obecny = os.path.dirname(os.path.abspath(__file__))
        sciezka_vosk = os.path.join(katalog_obecny, "vosk-model-pl")

        self._skonfiguruj_sluch(sciezka_vosk)
        self.dziala = True

        self.watek_sluchania = threading.Thread(target=self._glowny_watek_sluchania, daemon=False)
        self.watek_sluchania.start()
        self.koniec_inicjalizacji = True

    def _skonfiguruj_sluch(self, sciezka_modelu):
        try:
            model = vosk.Model(sciezka_modelu)
            self.rozpoznawacz = vosk.KaldiRecognizer(model, 16000)
            self.pyaudio_instance = pyaudio.PyAudio()
            self.strumien = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000
            )
            self.strumien.start_stream()
        except Exception as e:
            raise BladKonfiguracjiSluchu(f"Błąd konfiguracji: {e}")

    def _glowny_watek_sluchania(self):
        while self.dziala:
            try:
                if not self.dziala:
                    break
                dane = self.strumien.read(4000, exception_on_overflow=False)
                if self.rozpoznawacz.AcceptWaveform(dane):
                    wynik = json.loads(self.rozpoznawacz.Result())
                    tekst = wynik.get("text", "")
                    if tekst:
                        self._obsluz_rozpoznany_tekst(tekst)
                        time.sleep(0.1)
            except Exception as e:
                break

    def _obsluz_rozpoznany_tekst(self, tekst):
        slowa_kluczowe_pauza = ["pauza", "przerwa"]
        slowa_kluczowe_reset = ["reset", "od nowa"]
        slowa_kluczowe_przelacz = ["przełącz kamerę", "przełącz kamere", "zmień kamerę", "zmień kamere"]
        slowa_kluczowe_dodaj = ["dodaj powtórzenie", "zwiększ powtórzenia"]
        slowa_kluczowe_odejmij = ["odejmij powtórzenie", "zmniejsz powtórzenia"]
        slowa_kluczowe_rozpocznij = ["rozpocznij trening", "start"]

        if any(slowo in tekst for slowo in slowa_kluczowe_dodaj):
            self.zadanie_dodania_powtorzenia = True
            print("Wykryto komendę dodania powtórzenia.")
        elif any(slowo in tekst for slowo in slowa_kluczowe_odejmij):
            self.zadanie_odjecia_powtorzenia = True
            print("Wykryto komendę odjęcia powtórzenia.")
        elif any(slowo in tekst for slowo in slowa_kluczowe_pauza):
            self.pauza = not self.pauza
            print(f"Zmieniono stan pauzy: {self.pauza}")
        elif any(slowo in tekst for slowo in slowa_kluczowe_reset):
            self.zadanie_resetu = True
            print("Wykryto komendę resetu.")
        elif any(slowo in tekst for slowo in slowa_kluczowe_przelacz):
            self.zadanie_przelaczenia = True
            print("Wykryto komendę przełączenia kamery.")
        elif any(slowo in tekst for slowo in slowa_kluczowe_rozpocznij):
            self.zadanie_rozpoczecia_treningu = True
            print("Wykryto komendę rozpoczęcia treningu.")

    def sprawdz_i_wyczysc_reset(self):
        if self.zadanie_resetu:
            self.zadanie_resetu = False
            return True
        return False

    def sprawdz_i_wyczysc_przelaczenie(self):
        if self.zadanie_przelaczenia:
            self.zadanie_przelaczenia = False
            return True
        return False

    def sprawdz_i_wyczysc_dodanie_powtorzenia(self):
        if self.zadanie_dodania_powtorzenia:
            self.zadanie_dodania_powtorzenia = False
            return True
        return False

    def sprawdz_i_wyczysc_odjecie_powtorzenia(self):
        if self.zadanie_odjecia_powtorzenia:
            self.zadanie_odjecia_powtorzenia = False
            return True
        return False

    def sprawdz_i_wyczysc_rozpoczecie_treningu(self):
        if self.zadanie_rozpoczecia_treningu:
            self.zadanie_rozpoczecia_treningu = False
            return True
        return False

    def czy_jest_pauza(self):
        return self.pauza

    def zamknij(self):
        self.dziala = False
        time.sleep(0.2)

        self.strumien.stop_stream()
        self.strumien.close()
        self.pyaudio_instance.terminate()

    def czy_dziala(self):
        return self.dziala


def czy_komunikacja_zostala_zainicjalizowana(mowa, sluch):
    while mowa.koniec_inicjalizacji is False or sluch.koniec_inicjalizacji is False:
        time.sleep(0.1)
    return True