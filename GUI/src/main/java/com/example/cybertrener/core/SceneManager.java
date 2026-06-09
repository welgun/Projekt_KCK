package com.example.cybertrener.core;

import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import java.io.IOException;

public class SceneManager {
    private static Stage stage;

    public static void setStage(Stage primaryStage) {
        stage = primaryStage;
    }

    public static void switchScene(String fxmlPath) {
        try {
            String fullPath = "/com/example/cybertrener/view/" + fxmlPath;
            FXMLLoader loader = new FXMLLoader(SceneManager.class.getResource(fullPath));
            Parent root = loader.load();

            if (stage.getScene() == null) {
                Scene scene = new Scene(root, 1280, 720);
                stage.setScene(scene);
            } else {
                stage.getScene().setRoot(root);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void setImage(Image img) {
        stage.getIcons().add(img);
    }

    public static void setTitle(String title) {
        stage.setTitle(title);
    }
}
