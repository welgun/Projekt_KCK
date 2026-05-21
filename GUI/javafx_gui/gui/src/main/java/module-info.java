module com.example.gui {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.gui to javafx.fxml;
    exports com.example.gui;
    exports com.example.gui.greeting;
    opens com.example.gui.greeting to javafx.fxml;
    opens com.example.gui.login to javafx.fxml;
    exports com.example.gui.login;
    opens com.example.gui.mainInterface to javafx.fxml;
    exports com.example.gui.mainInterface;
}