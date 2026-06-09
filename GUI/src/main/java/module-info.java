module com.example.cybertrener {
    requires javafx.controls;
    requires javafx.fxml;
    //requires javafx.web;

    requires org.controlsfx.controls;
    //requires com.dlsc.formsfx;
    //requires org.kordamp.ikonli.javafx;
    //requires org.kordamp.bootstrapfx.core;
    //requires eu.hansolo.tilesfx;
    requires com.google.gson;
    requires java.net.http;

    opens com.example.cybertrener to javafx.fxml;
    exports com.example.cybertrener;
    exports com.example.cybertrener.controllers;
    opens com.example.cybertrener.controllers to javafx.fxml;
}