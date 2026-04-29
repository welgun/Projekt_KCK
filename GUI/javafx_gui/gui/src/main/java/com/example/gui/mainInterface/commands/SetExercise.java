package com.example.gui.mainInterface.commands;

import com.example.gui.mainInterface.MainInterfaceController;

public class SetExercise implements ChatCommand{
    private final MainInterfaceController controller;

    public SetExercise(MainInterfaceController controller) {
        this.controller = controller;
    }

    @Override
    public CommandResponse execute(String argument)  {
        if(argument.isEmpty()) {
            return CommandResponse.error("Niepoprawne użycie komendy. Wpisz 'help'");
        }
        try {
            int num = Integer.parseInt(argument.trim());
            if(num < 0 || num > 20) {
                return CommandResponse.error("Podaj poprawną wartość. (0>x>20)");
            }
            controller.setExerciseCount(num);
            return CommandResponse.success("Set exercise " + num);
        } catch (NumberFormatException e) {
            return CommandResponse.error("Niepoprawne użycie komendy. Wpisz 'help'");
        }
    }
}

