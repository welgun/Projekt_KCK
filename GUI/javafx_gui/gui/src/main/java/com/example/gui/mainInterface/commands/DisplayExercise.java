package com.example.gui.mainInterface.commands;

import com.example.gui.mainInterface.MainInterfaceController;

public class DisplayExercise implements ChatCommand{
    private final MainInterfaceController controller;

    public DisplayExercise(MainInterfaceController controller) {
        this.controller = controller;
    }

    @Override
    public CommandResponse execute(String argument) {
        int num = controller.getExerciseCount();
        return CommandResponse.success("Użytkownik ma wykonać " + num + " powtórzeń");
    }
}

