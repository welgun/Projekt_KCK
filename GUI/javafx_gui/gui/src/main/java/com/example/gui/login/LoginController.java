package com.example.gui.login;

import com.example.gui.mainInterface.MainInterfaceController;
import javafx.animation.FadeTransition;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.control.TextFormatter;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import javafx.util.Duration;

//
//3. tu odbywa się logowanie po powitaniu
//

public class LoginController {
    @FXML
    private Label login;
    @FXML
    private TextField inLogin;
    @FXML
    private VBox loginBox;
    @FXML
    private Label count;
    @FXML
    private TextField inCount;
    private String nickname;
    private int exCount;

    @FXML
    public void initialize() {
        login.setText("Wprowadź nazwę użytkownika: ");
        count.setText("Podaj liczbe poprawnych powtorzen: ");
        TextFormatter<String> blokadaSpacji = new TextFormatter<>(zmiana -> {
            if (zmiana.getText().contains(" ")) {
                return null;
            }
            return zmiana;
        });   //blokuje mozliwosc wprowadzenia spacji do inputa

        TextFormatter<String> onlyNum = new TextFormatter<>(change -> {
           if (change.getText().matches("[0-9]*")) {
               return change;
           }
           return null;
        });   //umozliwia wprowadzenie tylko liczb do pola inCount

        inLogin.setTextFormatter(blokadaSpacji);
        inCount.setTextFormatter(onlyNum);

        Platform.runLater(() -> {
            inLogin.requestFocus();
            inCount.requestFocus();
        });    //zapobiega bugom w postaci wielokrotnego przełączania sceny jezeli nacisniemy spacje bądź enter
    }
    @FXML
    protected void onLoginButtonClick(ActionEvent event) {
        String wpisanyTekst = inLogin.getText();
        String tempExCount = inCount.getText();


        if (wpisanyTekst.trim().isEmpty()) {
            login.setText("Hej, pole nie może być puste!");
            login.setStyle("-fx-text-fill: #e74c3c;");
            return;
        }

        if (tempExCount.trim().isEmpty()) {
            count.setText("Hej, pole nie może być puste!");
            count.setStyle("-fx-text-fill: #e74c3c;");
            return;
        }

        this.nickname = wpisanyTekst;
        this.exCount = Integer.parseInt(tempExCount);

        if(this.exCount >= 20 || this.exCount <= 0) {
            System.out.println("Wprowadzono niepoprawna wartosc do pola inCount");
            count.setText("Podaj mniejszą ilość");
            count.setStyle("-fx-text-fill: #e74c3c;");
            return;
        }

        login.setStyle("-fx-text-fill: #0fb9b1;");
        login.setText("Witaj na treningu, " + nickname + "!");

        inLogin.setDisable(true);
        loginBox.setDisable(true);

        FadeTransition fadeOut = new FadeTransition(Duration.seconds(1), loginBox);
        fadeOut.setFromValue(1.0);
        fadeOut.setToValue(0.0);

        fadeOut.setOnFinished(ev -> {
            try {
                System.out.println("Zarejestrowano użytkownika: " + nickname);
                System.out.println("Podano ilosc poprawnych powtorzen: " + exCount);
                FXMLLoader loader = new FXMLLoader(getClass().getResource("/com/example/gui/mainInterface/mainInterface.fxml"));
                javafx.scene.Parent root = loader.load();

                MainInterfaceController mainInterfaceController = loader.getController();

                mainInterfaceController.setNickname(this.nickname);
                mainInterfaceController.setExerciseCount(this.exCount);

                // Pobierz scenę z dowolnego elementu (np. pola tekstowego lub guzika) i ustaw root
                inLogin.getScene().setRoot(root);
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        fadeOut.play();
    }
}
