import time #tylko do testow - pozniej usunac
from piper.voice import PiperVoice
import vosk
import pyaudio
import queue
import threading
import json

class BladKonfiguracjiMowy(Exception):
    pass

class MowaTrenera:
    def __init__(self):
        self.kolejka_zdan = queue.Queue()

        self._skonfiguruj_glos()

        self.glowny_watek = threading.Thread(target=self._glowny_watek_mowy, daemon=True)
        self.glowny_watek.start()

    def _skonfiguruj_glos(self):
        try:
            self.glos = PiperVoice.load("pl_PL-mc_speech-medium.onnx")
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
        self._skonfiguruj_sluch("vosk-model-pl")
        self.dziala = True

        self.watek_sluchania = threading.Thread(target=self._glowny_watek_sluchania, daemon=False)
        self.watek_sluchania.start()

    def _skonfiguruj_sluch(self, sciezka_modelu):
        # ... Twoja konfiguracja (bez zmian) ...
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
            dane = self.strumien.read(4000, exception_on_overflow=False)
            if self.rozpoznawacz.AcceptWaveform(dane):
                wynik = json.loads(self.rozpoznawacz.Result())
                tekst = wynik.get("text", "")
                if tekst:
                    self.obsluz_rozpoznany_tekst(tekst)
                    time.sleep(0.1)

    def obsluz_rozpoznany_tekst(self, tekst):
        print(f"Trener usłyszał: {tekst}") #do testow - mozna potem usunac
        if "koniec" in tekst or "wyłącz" in tekst:
            self.zamknij()

    def zamknij(self):
        self.dziala = False

        self.strumien.stop_stream()
        self.strumien.close()
        self.pyaudio_instance.terminate()


#ponizej jest test komunikacji - do usuniecia pozniej

mowa = MowaTrenera()
sluch = SluchTrenera()

mowa.powiedz("testowy tekst 1")
mowa.powiedz("testowy tekst 2")
mowa.powiedz("ostatnie zdanie")

mowa.zamknij()