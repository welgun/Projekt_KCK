package com.example.gui.mainInterface.commands;

public class CommandResponse {
    private final String message;
    private final boolean isError;

    public CommandResponse(String message, boolean isError) {
        this.message = message;
        this.isError = isError;
    }

    public String getMessage() { return message; }
    public boolean isError() { return isError; }

    // Statyczne metody pomocnicze dla wygody
    public static CommandResponse success(String msg) { return new CommandResponse(msg, false); }
    public static CommandResponse error(String msg) { return new CommandResponse(msg, true); }
}