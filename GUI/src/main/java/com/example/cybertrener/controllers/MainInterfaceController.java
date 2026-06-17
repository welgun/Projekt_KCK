package com.example.cybertrener.controllers;

import com.example.cybertrener.services.ApiService;
import com.example.cybertrener.models.UserData;
import javafx.animation.ParallelTransition;
import javafx.animation.TranslateTransition;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.*;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.util.Duration;
import javafx.scene.control.ComboBox;
import javafx.scene.image.ImageView;
import javafx.animation.Timeline;
import javafx.scene.image.Image;
import javafx.scene.control.TableView;
import javafx.scene.control.TableColumn;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.beans.property.SimpleStringProperty;
import com.example.cybertrener.models.TrainingSession;

public class MainInterfaceController {

    @FXML private VBox sideMenu;
    @FXML private Button menuButton;

    @FXML private StackPane setupOverlay;
    @FXML private VBox loginBox;
    @FXML private VBox registerBox;
    @FXML private VBox changePasswordBox;

    @FXML private TextField loginNickField;
    @FXML private PasswordField loginPasswdField;
    @FXML private Button loginButton;
    @FXML private Label loginErrorLabel;

    @FXML private TextField regNickField;
    @FXML private PasswordField regPasswdField;
    @FXML private PasswordField regConfirmPasswdField;
    @FXML private Button registerButton;
    @FXML private Label registerErrorLabel;

    @FXML private TextField changePwNickField;
    @FXML private PasswordField oldPasswdField;
    @FXML private PasswordField newPasswdField;
    @FXML private Button changePwButton;
    @FXML private Label changePwErrorLabel;

    @FXML private ImageView cameraView;
    @FXML private ComboBox<String> cameraSelector;
    @FXML private Button startCamButton;

    @FXML private VBox historyBox;
    @FXML private TableView<TrainingSession> historyTable;
    @FXML private TableColumn<TrainingSession, String> colDate;
    @FXML private TableColumn<TrainingSession, Integer> colReps;
    @FXML private TableColumn<TrainingSession, Integer> colGoal;
    @FXML private TableColumn<TrainingSession, Integer> colDuration;
    @FXML private TableColumn<TrainingSession, String> colStatus;

    @FXML private VBox statsBox;
    @FXML private LineChart<String, Number> progressChart;

    private Timeline videoLoop;
    private String currentView = "przod";

    private boolean isMenuOpen = false;

    @FXML
    public void initialize() {
        sideMenu.setTranslateX(-300);

        setupOverlay.setVisible(true);
        loginBox.setVisible(true);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(false);

        loginButton.setDisable(true);
        registerButton.setDisable(true);
        changePwButton.setDisable(true);

        loginNickField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) loginNickField.setText(val.replaceAll("\\s", ""));
            loginErrorLabel.setText("");
            validateLoginForm();
        });
        loginPasswdField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) loginPasswdField.setText(val.replaceAll("\\s", ""));
            loginErrorLabel.setText("");
            validateLoginForm();
        });

        regNickField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) regNickField.setText(val.replaceAll("\\s", ""));
            registerErrorLabel.setText("");
            validateRegisterForm();
        });
        regPasswdField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) regPasswdField.setText(val.replaceAll("\\s", ""));
            registerErrorLabel.setText("");
            validateRegisterForm();
        });
        regConfirmPasswdField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) regConfirmPasswdField.setText(val.replaceAll("\\s", ""));
            registerErrorLabel.setText("");
            validateRegisterForm();
        });

        changePwNickField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) changePwNickField.setText(val.replaceAll("\\s", ""));
            changePwErrorLabel.setText("");
            validateChangePasswordForm();
        });
        oldPasswdField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) oldPasswdField.setText(val.replaceAll("\\s", ""));
            changePwErrorLabel.setText("");
            validateChangePasswordForm();
        });
        newPasswdField.textProperty().addListener((obs, old, val) -> {
            if (val.contains(" ")) newPasswdField.setText(val.replaceAll("\\s", ""));
            changePwErrorLabel.setText("");
            validateChangePasswordForm();
        });
        cameraSelector.getItems().addAll(
                "Kamera Frontowa (Widok z przodu)",
                "Kamera Boczna (Profil)"
        );
        cameraSelector.getSelectionModel().selectFirst();
        cameraSelector.setOnAction(e -> {
            if (cameraSelector.getSelectionModel().getSelectedIndex() == 0) {
                currentView = "przod";
            } else {
                currentView = "bok";
            }
        });

        historyBox.setVisible(false);

        colDate.setCellValueFactory(new PropertyValueFactory<>("date"));
        colReps.setCellValueFactory(new PropertyValueFactory<>("reps_done"));
        colGoal.setCellValueFactory(new PropertyValueFactory<>("reps_goal"));
        colDuration.setCellValueFactory(new PropertyValueFactory<>("duration_seconds"));

        colStatus.setCellValueFactory(cellData -> {
            int status = cellData.getValue().getIs_goal_achieved();
            return new SimpleStringProperty(status == 1 ? "Trening Udany" : "Przerwany");
        });

        statsBox.setVisible(false);

        startCameraStream();
        startStatusPolling();
    }

    private void validateLoginForm() {
        boolean valid = !loginNickField.getText().trim().isEmpty() && !loginPasswdField.getText().isEmpty();
        loginButton.setDisable(!valid);
    }

    private void validateRegisterForm() {
        String password = regPasswdField.getText();
        String confirm = regConfirmPasswdField.getText();

        boolean isNickNotEmpty = !regNickField.getText().trim().isEmpty();
        boolean isPasswordNotEmpty = !password.isEmpty();
        boolean doPasswordsMatch = password.equals(confirm);

        registerButton.setDisable(!(isNickNotEmpty && isPasswordNotEmpty && doPasswordsMatch));

        if (!doPasswordsMatch && !confirm.isEmpty()) {
            registerErrorLabel.setText("Hasła nie są identyczne!");
        } else {
            registerErrorLabel.setText("");
        }
    }

    private void validateChangePasswordForm() {
        boolean valid = !changePwNickField.getText().trim().isEmpty() &&
                !oldPasswdField.getText().isEmpty() &&
                !newPasswdField.getText().isEmpty();
        changePwButton.setDisable(!valid);
    }

    @FXML private void showRegisterForm() {
        loginErrorLabel.setText("");
        registerErrorLabel.setText("");
        changePwErrorLabel.setText("");

        statsBox.setVisible(false);
        loginBox.setVisible(false);
        changePasswordBox.setVisible(false);
        registerBox.setVisible(true);
    }

    @FXML private void showLoginForm() {
        loginErrorLabel.setText("");
        registerErrorLabel.setText("");
        changePwErrorLabel.setText("");

        statsBox.setVisible(false);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(false);
        loginBox.setVisible(true);
    }

    @FXML private void showChangePasswordForm() {
        loginErrorLabel.setText("");
        registerErrorLabel.setText("");
        changePwErrorLabel.setText("");

        statsBox.setVisible(false);
        loginBox.setVisible(false);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(true);
    }

    @FXML
    private void showHistoryForm() {
        if (isMenuOpen) toggleMenu();

        loginBox.setVisible(false);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(false);

        statsBox.setVisible(false);
        setupOverlay.setVisible(true);
        historyBox.setVisible(true);

        loadHistoryData();
    }

    @FXML private void handleSettingsClick() {
        toggleMenu();
        changePwErrorLabel.setText("");
        setupOverlay.setVisible(true);
        loginBox.setVisible(false);
        registerBox.setVisible(false);
        historyBox.setVisible(false);
        statsBox.setVisible(false);
        changePasswordBox.setVisible(true);
    }

    @FXML private void hideChangePasswordForm() {
        changePwErrorLabel.setText("");
        changePwNickField.clear();
        oldPasswdField.clear();
        newPasswdField.clear();

        if (UserData.getUsername() == null || UserData.getUsername().isEmpty()) {
            changePasswordBox.setVisible(false);
            loginBox.setVisible(true);
        } else {
            setupOverlay.setVisible(false);
            changePasswordBox.setVisible(false);
        }
    }

    @FXML
    private void handleLogin() {
        String username = loginNickField.getText().trim();
        String password = loginPasswdField.getText();

        loginButton.setText("Logowanie...");
        loginButton.setDisable(true);
        loginErrorLabel.setText("");

        ApiService.loginUser(username, password,
                () -> Platform.runLater(() -> {
                    UserData.setUsername(username);
                    setupOverlay.setVisible(false);
                    loginBox.setVisible(false);
                }),
                (error) -> Platform.runLater(() -> {
                    loginButton.setText("Zaloguj się");
                    validateLoginForm();
                    loginErrorLabel.setStyle("-fx-text-fill: #ff3333; -fx-font-weight: bold;");
                    loginErrorLabel.setText(error);
                })
        );
    }

    @FXML
    private void handleRegister() {
        String username = regNickField.getText().trim();
        String password = regPasswdField.getText();

        registerButton.setText("Tworzenie konta...");
        registerButton.setDisable(true);
        registerErrorLabel.setText("");

        ApiService.registerUser(username, password,
                () -> Platform.runLater(() -> {
                    showLoginForm();
                    loginNickField.setText(username);
                    loginErrorLabel.setStyle("-fx-text-fill: #34FAEA; -fx-font-weight: bold;");
                    loginErrorLabel.setText("Konto utworzone pomyślnie. Zaloguj się!");
                    registerButton.setText("Utwórz konto");
                    validateRegisterForm();
                }),
                (error) -> Platform.runLater(() -> {
                    registerButton.setText("Utwórz konto");
                    validateRegisterForm();
                    registerErrorLabel.setText(error);
                })
        );
    }

    @FXML
    private void handleChangePassword() {
        String username = changePwNickField.getText().trim();
        String oldPassword = oldPasswdField.getText();
        String newPassword = newPasswdField.getText();

        changePwButton.setText("Zmieniam...");
        changePwButton.setDisable(true);
        changePwErrorLabel.setText("");

        ApiService.changePassword(username, oldPassword, newPassword,
                () -> Platform.runLater(() -> {
                    changePwNickField.clear();
                    oldPasswdField.clear();
                    newPasswdField.clear();

                    showLoginForm();
                    loginNickField.setText(username);
                    loginErrorLabel.setStyle("-fx-text-fill: #34FAEA; -fx-font-weight: bold;");
                    loginErrorLabel.setText("Hasło zmienione pomyślnie! Zaloguj się ponownie.");

                    changePwButton.setText("Zapisz nowe hasło");
                    validateChangePasswordForm();
                }),
                (error) -> Platform.runLater(() -> {
                    changePwButton.setText("Zapisz nowe hasło");
                    validateChangePasswordForm();
                    changePwErrorLabel.setText(error);
                })
        );
    }

    @FXML
    private void handleLogout() {
        if (isMenuOpen) {
            toggleMenu();
        }

        UserData.setUsername("");
        UserData.setReps(0);

        loginNickField.clear();
        loginPasswdField.clear();

        loginErrorLabel.setStyle("-fx-text-fill: #34FAEA; -fx-font-weight: bold;");
        loginErrorLabel.setText("Zostałeś wylogowany.");
        loginButton.setText("Zaloguj się");
        loginButton.setDisable(true);

        setupOverlay.setVisible(true);
        loginBox.setVisible(true);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(false);
        historyBox.setVisible(false);
        statsBox.setVisible(false);

        System.out.println("Użytkownik został pomyślnie wylogowany.");
    }

    @FXML
    private void toggleMenu() {
        TranslateTransition menuTran = new TranslateTransition(Duration.seconds(0.3), sideMenu);
        TranslateTransition buttonTran = new TranslateTransition(Duration.seconds(0.3), menuButton);
        double menuWidth = sideMenu.getWidth();

        if (isMenuOpen) {
            menuTran.setToX(-menuWidth);
            buttonTran.setToX(0);
            isMenuOpen = false;
        } else {
            menuTran.setToX(0);
            buttonTran.setToX(menuWidth);
            isMenuOpen = true;
        }
        ParallelTransition pt = new ParallelTransition(menuTran, buttonTran);
        pt.play();
    }

    @FXML
    private void hideHistoryForm() {
        setupOverlay.setVisible(false);
        historyBox.setVisible(false);
    }

    private void loadHistoryData() {
        if (ApiService.currentUserId == -1) return;

        ApiService.getTrainingHistory(ApiService.currentUserId,
                history -> Platform.runLater(() -> {
                    historyTable.getItems().setAll(history);
                }),
                error -> Platform.runLater(() -> {
                    System.out.println("Błąd ładowania tabeli: " + error);
                })
        );
    }

    @FXML
    private void showStatsForm() {
        if (isMenuOpen) toggleMenu();

        loginBox.setVisible(false);
        registerBox.setVisible(false);
        changePasswordBox.setVisible(false);
        historyBox.setVisible(false);

        setupOverlay.setVisible(true);
        statsBox.setVisible(true);

        loadStatsData();
    }

    @FXML
    private void hideStatsForm() {
        setupOverlay.setVisible(false);
        statsBox.setVisible(false);
    }

    private void loadStatsData() {
        if (ApiService.currentUserId == -1) return;

        ApiService.getTrainingHistory(ApiService.currentUserId,
                history -> Platform.runLater(() -> {
                    XYChart.Series<String, Number> series = new XYChart.Series<>();
                    series.setName("Skuteczność (%)");

                    int trainingNumber = 1;
                    for (int i = history.size() - 1; i >= 0; i--) {
                        TrainingSession session = history.get(i);

                        double ratio = 0;
                        if (session.getReps_goal() > 0) {
                            ratio = ((double) session.getReps_done() / session.getReps_goal()) * 100.0;
                        }

                        series.getData().add(new XYChart.Data<>("T" + trainingNumber, ratio));
                        trainingNumber++;
                    }

                    progressChart.getData().clear();
                    progressChart.getData().add(series);
                }),
                error -> Platform.runLater(() -> System.out.println("Błąd ładowania statystyk: " + error))
        );
    }

    @FXML
    private void startTrainingStream() {
        System.out.println("Przycisk ROZPOCZNIJ TRENING został wciśnięty!");

        startCamButton.setDisable(true);
        startCamButton.setVisible(false);

        ApiService.startTraining(
                () -> {
                    System.out.println("Trening rozpoczęty pomyślnie.");
                },
                (error) -> {
                    System.err.println("Nie udało się rozpocząć treningu: " + error);
                    Platform.runLater(() -> {
                        startCamButton.setDisable(false);
                        startCamButton.setVisible(true);
                    });
                }
        );
    }

    private Timeline statusPollingTimeline;

    private void startStatusPolling() {
        if (statusPollingTimeline != null) {
            statusPollingTimeline.stop();
        }

        statusPollingTimeline = new Timeline(new javafx.animation.KeyFrame(Duration.seconds(1), event -> {
            ApiService.checkTrainingStatus(isRunning -> {
                Platform.runLater(() -> {
                    if (isRunning) {
                        if (startCamButton.isVisible()) {
                            startCamButton.setDisable(true);
                            startCamButton.setVisible(false);
                            System.out.println("Trening rozpoczął się (wykryto w tle) - przycisk schowany.");
                        }
                    } else {
                        if (!startCamButton.isVisible()) {
                            startCamButton.setDisable(false);
                            startCamButton.setVisible(true);
                            System.out.println("Trening został zakończony - przycisk przywrócony.");

                            loadHistoryData();
                        }
                    }
                });
            });
        }));
        statusPollingTimeline.setCycleCount(Timeline.INDEFINITE);
        statusPollingTimeline.play();
    }

    private volatile boolean isCameraRunning = false;

    private void startCameraStream() {
        isCameraRunning = true;

        Thread streamThread = new Thread(() -> {
            while (isCameraRunning) {
                try {
                    String url = "http://localhost:5001/api/video_feed?widok=" + currentView + "&time=" + System.currentTimeMillis();

                    Image frame = new Image(url, false);

                    if (!frame.isError()) {
                        Platform.runLater(() -> cameraView.setImage(frame));
                    }

                    Thread.sleep(33);

                } catch (Exception e) {
                    try { Thread.sleep(500); } catch (InterruptedException ex) {}
                }
            }
        });

        streamThread.setDaemon(true);
        streamThread.start();
    }
}