package com.example.gui.mainInterface.commands;

import javafx.application.Platform;

public class Quit implements ChatCommand{
    @Override
    public CommandResponse execute(String argument) {
        Platform.exit();
        System.exit(0);
        return CommandResponse.success("Trwa zamykanie");
    }
}
