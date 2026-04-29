package com.example.gui.mainInterface;

import com.example.gui.mainInterface.commands.*;
import javafx.fxml.FXML;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;

import java.util.HashMap;
import java.util.Map;

//
//4. dalsze działanie aplikacji
//

public class MainInterfaceController {
    private final Map<String, ChatCommand> commands = new HashMap<>();
    @FXML
    private Label napis;
    @FXML
    private Text ilosc;
    @FXML
    private VBox logs;
    @FXML
    private TextField prompt;
    @FXML
    private ScrollPane scrollik;
    private String nick;
    private int exerciseCount;

    enum isUser {
        USER,
        BOT,
        ERROR
    }

    @FXML
    public void initialize() {
        commands.put("help", new Help());
        commands.put("quit", new Quit());
        commands.put("clear", new Clear(this.logs));
        commands.put("dispex", new DisplayExercise(this));
        commands.put("setex", new SetExercise(this));
        ilosc.wrappingWidthProperty().bind(logs.widthProperty().subtract(20));
        logs.setAlignment(Pos.TOP_LEFT);
        logs.heightProperty().addListener((observable, oldValue, newValue) -> {
            scrollik.setVvalue(1.0); // 1.0 oznacza dół, 0.0 oznacza górę
        });
    }

    @FXML
    private void handleCommand() {
        String input = prompt.getText().trim();
        appendMessage(nick + ": " + input, isUser.USER);
        String[] parts = input.split(" ", 2);
        String commandName = parts[0].toLowerCase();
        String argument = (parts.length > 1) ? parts[1] : "";
        ChatCommand command = commands.get(commandName);
        if (command != null) {
            CommandResponse response = command.execute(argument);

            // Decydujemy o typie wiadomości na podstawie flagi isError
            isUser type = response.isError() ? isUser.ERROR : isUser.BOT;
            appendMessage("Bot: " + response.getMessage(), type);
        } else {
            appendMessage("Bot: Nie znam komendy '" + input + "'. Wpisz 'help'.", isUser.ERROR);
        }

        prompt.clear();
    }

    public void setNickname(String przekazanyNick) {
        this.nick = przekazanyNick;
        updateUI();
    }

    public int getExerciseCount() {
        return this.exerciseCount;
    }

    public void setExerciseCount(int liczba) {
        try {
            this.exerciseCount = liczba;
            updateUI();
        } catch(NumberFormatException e) {
            System.out.println("Blad: " + e.getMessage());
        }
    }

    private void updateUI() {
        if (nick != null) {
            if (napis != null) {
                napis.setText(nick /*+ " = super ziomek"*/);
            }
            if (ilosc != null) {
                ilosc.setText("Użytkownik chce zrobic: " + exerciseCount + " powtorzen");
            }
            System.out.println("Dane kompletne - UI zaktualizowane!");
        }
    }


    private void appendMessage(String text, isUser przelacz) {
        Label label = new Label(text);
        label.setWrapText(true);
        label.setMaxWidth(Double.MAX_VALUE);

        // Tutaj możesz dodać stylizację CSS, np. inny kolor dla użytkownika, inny dla bota
        if (przelacz == isUser.USER) {
            label.getStyleClass().add("user-label");
        } else if(przelacz == isUser.BOT) {
            label.getStyleClass().add("bot-label");
        } else if(przelacz == isUser.ERROR) {
            label.getStyleClass().add("err-label");
        }

        logs.getChildren().add(label); // chatHistoryVBox to Twój kontener na wiadomości
    }
}
