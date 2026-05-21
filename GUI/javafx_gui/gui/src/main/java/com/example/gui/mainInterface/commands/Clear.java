package com.example.gui.mainInterface.commands;

import javafx.scene.layout.VBox;

public class Clear implements ChatCommand{
    private final VBox toClear;
    public Clear(VBox boks) {
        this.toClear = boks;
    }

    @Override
    public CommandResponse execute(String argument) {
        toClear.getChildren().clear();
        return CommandResponse.success("cleared.");
    }
}
