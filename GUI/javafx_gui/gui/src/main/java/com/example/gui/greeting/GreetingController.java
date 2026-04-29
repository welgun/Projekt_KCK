package com.example.gui.greeting;

import javafx.animation.Animation;
import javafx.animation.FadeTransition;
import javafx.animation.PauseTransition;
import javafx.animation.SequentialTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.VBox;
import javafx.scene.text.Font;
import javafx.stage.Stage;
import javafx.util.Duration;

//
//2. scena powitania uzytkownika
//

public class GreetingController {
    @FXML
    private Label greet;
    @FXML
    private Label text;
    @FXML
    private VBox contentBox;
    @FXML
    private Label success;

    @FXML
    public void initialize() {
        Font playwrite = Font.loadFont(getClass().getResourceAsStream("/com/example/gui/fonts/PlaywriteIE-Regular.ttf"), 14);
        Font barlow = Font.loadFont(getClass().getResourceAsStream("/com/example/gui/fonts/Barlow-Light.ttf"), 14);
        greet.setText("CyberTrener");
        text.setText("Edycja Martwy Ciąg");
        contentBox.setOpacity(0.0);
        success.setOpacity(0.0);

        FadeTransition fadeIn = new FadeTransition(Duration.seconds(2), contentBox);
        fadeIn.setFromValue(0.0);
        fadeIn.setToValue(1.0);

        PauseTransition pause = new PauseTransition(Duration.seconds(2));

        FadeTransition fadeOut = new FadeTransition(Duration.seconds(2), contentBox);
        fadeOut.setFromValue(1.0);
        fadeOut.setToValue(0.0);

        SequentialTransition sequence = new SequentialTransition(fadeIn, pause, fadeOut);

        sequence.setOnFinished(event -> przejdzDoLogowania());

        sequence.play();

        //naciśnięcie spacji powoduje skipa pierwszej sceny
        Platform.runLater(() -> {
            Scene scena = contentBox.getScene();
            scena.setOnKeyPressed(event -> {
                if (event.getCode() == KeyCode.SPACE) {
                    if (sequence != null && sequence.getStatus() == Animation.Status.RUNNING) {
                        System.out.println("Skipnieto animacje");
                        sequence.stop();
                    }
                    przejdzDoLogowania();
                }
            });
        });
    }

    private void przejdzDoLogowania() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/com/example/gui/login/login.fxml"));
            javafx.scene.Parent root = loader.load();
            Scene currentScene = contentBox.getScene();
            currentScene.setRoot(root);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


//
// linia 30 (do sprawdzania załadowania czcionki)
//
/*if (playwrite != null) {
            System.out.println("PRAWIDŁOWA NAZWA DLA CSS (Playwrite): '" + playwrite.getFamily() + "' lub '" + playwrite.getName() + "'");
        } else {
            System.out.println("BŁĄD: Nie znaleziono pliku Playwrite!");
        }

        if (barlow != null) {
            System.out.println("PRAWIDŁOWA NAZWA DLA CSS (Barlow): '" + barlow.getFamily() + "' lub '" + barlow.getName() + "'");
        } else {
            System.out.println("BŁĄD: Nie znaleziono pliku Barlow!");
        }*/
//
//
//