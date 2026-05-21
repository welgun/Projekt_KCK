package com.example.gui;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import java.io.IOException;

//
//1. pierwsze zaladowanie aplikacji odbywa sie tu
//

public class App extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource("greeting/greeting.fxml"));
        Scene scene = new Scene(fxmlLoader.load(), 1280, 720);
        stage.setTitle("CyberTrener");

        stage.setMinWidth(1280);   // Minimalna szerokość
        stage.setMinHeight(720);  // Minimalna wysokość

        var iconStream = App.class.getResourceAsStream("/com/example/gui/icons/sport.png");

        if (iconStream != null) {
            Image icon = new Image(iconStream);
            // ikona pobrana z https://pl.freepik.com/ikona/sport_18669673#fromView=keyword&page=1&position=0&uuid=e6cf192f-4a76-4e4e-bde9-ecb2f53fe444
            stage.getIcons().add(icon);
        } else {
            System.out.println("Błąd: Nie znaleziono pliku ikony!");
        }

        stage.setScene(scene);
        stage.show();
        System.out.println("Uruchomiono aplikacje");
    }
}
