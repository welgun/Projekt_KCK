import time #tylko do testow - pozniej usunac
import pyttsx3
import vosk
import pyaudio
import queue
import threading

class MowaTrenera:
    def __init__(self):
        self.kolejka_zdan = queue.Queue()
        glowny_watek_mowy = threading.Thread(target=self._glowny_watek_mowy, daemon=True)
        glowny_watek_mowy.start()

    def _skonfiguruj_glos(self, silnik):
        silnik.setProperty('rate', 150)

        glosy = silnik.getProperty('voices')
        for glos in glosy:
            if 'pl' in glos.languages or 'pol' in glos.name.lower() or 'polish' in glos.name.lower():
                silnik.setProperty('voice', glos.id)
                break

    def powiedz(self, tekst):
        self.kolejka_zdan.put(tekst)

    def _glowny_watek_mowy(self):
        while True:
            tekst = self.kolejka_zdan.get()
            silnik = pyttsx3.init()
            self._skonfiguruj_glos(silnik)
            silnik.say(tekst)
            silnik.runAndWait()
            del silnik

#model = vosk.Model("vosk-model-pl")

#ponizej jest test komunikacji - do usuniecia pozniej

a = MowaTrenera()

a.powiedz("testowy tekst 1")
a.powiedz("testowy tekst 2")
a.powiedz("ostatnie zdanie")

time.sleep(10)