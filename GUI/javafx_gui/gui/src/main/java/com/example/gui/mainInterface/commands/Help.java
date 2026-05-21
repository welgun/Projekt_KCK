package com.example.gui.mainInterface.commands;

public class Help implements ChatCommand{
    @Override
    public CommandResponse execute(String argument) {
        return CommandResponse.success("Użycie ? help\n" +
                " ? help - wyswietla dostępne komendy\n" +
                " ? clear - czyści konsole\n" +
                " ? quit - zamyka aplikację\n" +
                " ? dispex - wyświetla liczbę powtórzeń, które użytkownik powinien wykonać\n" +
                " ? setex <liczba> - zmienia liczbe powtórzeń do wykonania");
    }
}
