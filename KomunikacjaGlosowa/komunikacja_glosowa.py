import time #tylko do testow - pozniej usunac
from piper.voice import PiperVoice
import vosk
import pyaudio
import queue
import threading

class MowaTrenera:
    def __init__(self):
        self.kolejka_zdan = queue.Queue()

        self._skonfiguruj_glos()

        glowny_watek_mowy = threading.Thread(target=self._glowny_watek_mowy, daemon=True)
        glowny_watek_mowy.start()

    def _skonfiguruj_glos(self):
        self.glos = PiperVoice.load("pl_PL-mc_speech-medium.onnx")
        self.pyaudio_instance = pyaudio.PyAudio()

        self.strumien = self.pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.glos.config.sample_rate,
            output=True
        )

    def powiedz(self, tekst):
        self.kolejka_zdan.put(tekst)

    def _glowny_watek_mowy(self):
        while True:
            tekst = self.kolejka_zdan.get()

            for chunk in self.glos.synthesize(tekst):
                dane_audio = chunk.audio_int16_bytes
                self.strumien.write(dane_audio)

#model = vosk.Model("vosk-model-pl")

#ponizej jest test komunikacji - do usuniecia pozniej

a = MowaTrenera()

a.powiedz("testowy tekst 1")
a.powiedz("testowy tekst 2")
a.powiedz("ostatnie zdanie")

time.sleep(10)