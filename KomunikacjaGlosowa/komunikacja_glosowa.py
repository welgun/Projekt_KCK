import time #tylko do testow - pozniej usunac
from piper.voice import PiperVoice
import vosk
import pyaudio
import queue
import threading

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

#model = vosk.Model("vosk-model-pl")

#ponizej jest test komunikacji - do usuniecia pozniej

a = MowaTrenera()

a.powiedz("testowy tekst 1")
a.powiedz("testowy tekst 2")
a.powiedz("ostatnie zdanie")

time.sleep(7)

a.zamknij()