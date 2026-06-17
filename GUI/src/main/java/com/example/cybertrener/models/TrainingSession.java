package com.example.cybertrener.models;

public class TrainingSession {
    private String date;
    private int reps_done;
    private int reps_goal;
    private int is_goal_achieved;
    private int duration_seconds;

    public String getDate() { return date; }
    public int getReps_done() { return reps_done; }
    public int getReps_goal() { return reps_goal; }
    public int getIs_goal_achieved() { return is_goal_achieved; }
    public int getDuration_seconds() { return duration_seconds; }
}