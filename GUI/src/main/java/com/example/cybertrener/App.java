package com.example.cybertrener;

import com.example.cybertrener.core.SceneManager;
import javafx.application.Application;
import javafx.scene.image.Image;
import javafx.scene.text.Font;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Objects;

public class App extends Application {
    @Override
    public void start(Stage stage) throws IOException {
        Font.loadFont(getClass().getResourceAsStream("fonts/BitcountPropSingle-Regular.ttf"), 64);
        Font.loadFont(getClass().getResourceAsStream("fonts/Barlow-Medium.ttf"), 18);
        Font.loadFont(getClass().getResourceAsStream("fonts/PlayWriteIE-Regular.ttf"), 18);

        stage.setResizable(true);
        stage.setMinWidth(1280);
        stage.setMinHeight(720);

        stage.setWidth(1280);
        stage.setHeight(720);
        SceneManager.setStage(stage);
        SceneManager.setTitle("Cybertrener");
        // ikona pobrana z https://pl.freepik.com/ikona/sport_18669673#fromView=keyword&page=1&position=0&uuid=e6cf192f-4a76-4e4e-bde9-ecb2f53fe444
        Image icon = new Image(Objects.requireNonNull(getClass().getResourceAsStream("/com/example/cybertrener/img/sport.png")));
        SceneManager.setImage(icon);
        SceneManager.switchScene("greeting/greeting.fxml");
        stage.show();
    }
}
