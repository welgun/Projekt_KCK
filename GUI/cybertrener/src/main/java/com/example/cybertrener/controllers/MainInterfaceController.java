package com.example.cybertrener.controllers;

import javafx.animation.ParallelTransition;
import javafx.animation.TranslateTransition;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.layout.VBox;
import javafx.util.Duration;
import com.example.cybertrener.models.UserData;
import javafx.scene.control.TextField;
import javafx.scene.layout.StackPane;

public class MainInterfaceController {

    @FXML private VBox sideMenu;
    @FXML private Button menuButton;

    @FXML private StackPane setupOverlay;
    @FXML private TextField nickField;
    @FXML private TextField setsField;
    @FXML private TextField repsField;
    @FXML private Button startButton;

    private boolean isMenuOpen = false;

    @FXML
    public void initialize() {
        sideMenu.setTranslateX(-300);
        startButton.setDisable(true);

        nickField.textProperty().addListener((observable, oldValue, newValue) -> {
            validateForm();
        });

        setsField.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                setsField.setText(newValue.replaceAll("[^\\d]", ""));
            } else if (!newValue.isEmpty()) {
                try {
                    int val = Integer.parseInt(newValue);
                    if (val > 20) {
                        setsField.setText("20");
                    }
                } catch (NumberFormatException e) {
                    setsField.setText("");
                }
            }
            validateForm();
        });

        repsField.textProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue.matches("\\d*")) {
                repsField.setText(newValue.replaceAll("[^\\d]", ""));
            } else if (!newValue.isEmpty()) {
                try {
                    int val = Integer.parseInt(newValue);
                    if (val > 20) {
                        repsField.setText("20");
                    }
                } catch (NumberFormatException e) {
                    repsField.setText("");
                }
            }
            validateForm();
        });
    }

    private void validateForm() {
        boolean isNickValid = nickField.getText() != null && !nickField.getText().trim().isEmpty();
        boolean isSetsValid = setsField.getText() != null && !setsField.getText().trim().isEmpty();
        boolean isRepsValid = repsField.getText() != null && !repsField.getText().trim().isEmpty();

        startButton.setDisable(!(isNickValid && isRepsValid && isSetsValid));
    }

    @FXML
    private void toggleMenu() {
        Duration animDuration = Duration.seconds(0.3);

        TranslateTransition menuTransition = new TranslateTransition(animDuration, sideMenu);
        TranslateTransition buttonTransition = new TranslateTransition(animDuration, menuButton);

        double menuWidth = sideMenu.getWidth();

        if (isMenuOpen) {
            menuTransition.setToX(-menuWidth);
            buttonTransition.setToX(0);
            isMenuOpen = false;
        } else {
            menuTransition.setToX(0);
            buttonTransition.setToX(menuWidth);
            isMenuOpen = true;
        }

        ParallelTransition parallelTransition = new ParallelTransition(menuTransition, buttonTransition);
        parallelTransition.play();
    }

    @FXML
    private void startTraining() {
        UserData.setUsername(nickField.getText().trim());
        UserData.setReps(Integer.parseInt(repsField.getText()));
        UserData.setSets(Integer.parseInt(setsField.getText()));

        setupOverlay.setVisible(false);

        System.out.println("Nick: " + UserData.getUsername() + " Ilość serii: "+ UserData.getSets() +" Powtórzenia: " + UserData.getReps());
    }
}