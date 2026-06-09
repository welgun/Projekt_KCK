package com.example.cybertrener.models;

public class UserData {
    private static String username;
    private static int number_of_reps;
    private static int sets;

    public static int getSets() {
        return sets;
    }

    public static void setSets(int sets) {
        UserData.sets = sets;
    }

    public static int getReps() {
        return number_of_reps;
    }

    public static void setReps(int number_of_reps) {
        UserData.number_of_reps = number_of_reps;
    }

    public static String getUsername() {
        return username;
    }

    public static void setUsername(String username) {
        UserData.username = username;
    }
}
