package com.example.cybertrener.controllers;

import com.example.cybertrener.core.SceneManager;
import javafx.animation.FadeTransition;
import javafx.animation.PauseTransition;
import javafx.animation.SequentialTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.util.Duration;

public class GreetingController {

    @FXML private VBox mainContainer;

    private SequentialTransition sequence;

    @FXML
    public void initialize() {
        FadeTransition fadeIn = new FadeTransition(Duration.seconds(1), mainContainer);
        fadeIn.setFromValue(0);
        fadeIn.setToValue(1);

        PauseTransition pause = new PauseTransition(Duration.seconds(2));

        FadeTransition fadeOut = new FadeTransition(Duration.seconds(1), mainContainer);
        fadeOut.setFromValue(1);
        fadeOut.setToValue(0);

        sequence = new SequentialTransition(fadeIn, pause, fadeOut);

        sequence.setOnFinished(e -> {
            SceneManager.switchScene("mainInterface/mainInterface.fxml");
        });

        sequence.play();

        Platform.runLater(() -> {
            if (mainContainer.getScene() != null) {
                mainContainer.getScene().setOnKeyPressed(event -> {
                    if (event.getCode() == KeyCode.SPACE) {
                        sequence.stop();

                        SceneManager.switchScene("mainInterface/mainInterface.fxml");
                    }
                });
            }
        });
    }
}