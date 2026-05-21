# Dokumentacja komunikacji głosowej🎙️

# 📂Wymagania:
### Aby komunikacja głosowa działała wymagane są pliki/katalogi:
- vosk_model_pl (folder z wymaganą zawartością)
- pl_PL-mc_speech-medium.onnx
- pl_PL-mc_speech-medium.json

Są one dostępne w repozytorium w folderze komunikacja glosowa.

# 🔊Klasa MowaTrenera()
## Dostępne metody dla użytkownika:
### powiedz(tekst)
Przyjmuje tekst który ma powiedzieć i dodaje go do kolejki mowy.
### zamknij()
Czeka na zakończenie aktualnie wypowiadanego zdania, a następnie zwalnia zasoby karty dźwiękowej i zamyka wątek.

# 👂Klasa SluchTrenera()
## Dostępne metody dla użytkownika:
### Zachowanie po inicjalizacji
Po inicjalizacji klasa automatycznie nasłuchuje i obsługuje polecenia użytkownika. Nie potrzebne są do tego dodatkowe metody.

Aby dodać nowe komendy należy dopisać je do metody _obsluz_rozpoznany_tekst(tekst).

Przykład: 
        
        if "koniec" in tekst or "wyłącz" in tekst:
            self.zamknij()
        #tu mozna dodac nowe komendy
### zamknij()
Zwalnia zasoby i zamyka wątek. Po komendzie "koniec" lub "wyłącz" jest wywoływana automatycznie.

Można ją użyć gdy zamykamy program w inny sposób, na przykład:

        if okno_programu_zostalo_zamkniete:
            sluch.zamknij()

# Funkcja pomcnicza
### czy_komunikacja_zostala_zainicjalizowana(mowa, sluch) 
Dzięki tej funkcji możemy sprawdzić czy inicjalizacja komunikacji przebiegła pomyślnie.
Funkcja ta blokuje wykonanie programu do momentu zakończenia konfiguracji.
Warto użyć jej po utworzeniu obu klas.

# 💻 Przykład użycia
    mowa = MowaTrenera()
    sluch = SluchTrenera()

    if czy_komunikacja_zostala_zainicjalizowana(mowa, sluch):
        print("Komunikacja zostala zainicjalizowana")

    mowa.powiedz("testowy tekst 1")
    mowa.powiedz("testowy tekst 2")
    mowa.powiedz("ostatnie zdanie")

    mowa.zamknij()
    #sluch zostanie zamkniety po komendzie "koniec" lub "wyłącz"
