package com.example.cybertrener.services;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.function.Consumer;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class ApiService {
    public static int currentUserId = -1;
    private static final String BASE_URL = "http://localhost:5000";
    private static final String TRACKING_URL = "http://localhost:5001";
    private static final HttpClient client = HttpClient.newHttpClient();
    private static final Gson gson = new Gson();

    private static String getErrorMessage(String responseBody, int statusCode) {
        try {
            JsonObject json = gson.fromJson(responseBody, JsonObject.class);
            if (json != null && json.has("error")) {
                return json.get("error").getAsString();
            }
        } catch (Exception e) {

        }
        return "Nieoczekiwany błąd serwera. Kod: " + statusCode;
    }

    public static void loginUser(String username, String password, Runnable onSuccess, Consumer<String> onError) {
        JsonObject jsonBody = new JsonObject();
        jsonBody.addProperty("username", username);
        jsonBody.addProperty("password", password);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/api/login"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(response -> {
                    if (response.statusCode() == 200) {
                        JsonObject json = gson.fromJson(response.body(), JsonObject.class);
                        int userId = json.get("user_id").getAsInt();
                        ApiService.currentUserId = userId;
                        onSuccess.run();
                    } else {
                        onError.accept(getErrorMessage(response.body(), response.statusCode()));
                    }
                })
                .exceptionally(e -> {
                    onError.accept("Brak połączenia z serwerem bazy danych.");
                    return null;
                });
    }

    public static void registerUser(String username, String password, Runnable onSuccess, Consumer<String> onError) {
        JsonObject jsonBody = new JsonObject();
        jsonBody.addProperty("username", username);
        jsonBody.addProperty("password", password);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/api/register"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(response -> {
                    if (response.statusCode() == 201) {
                        onSuccess.run();
                    } else {
                        onError.accept(getErrorMessage(response.body(), response.statusCode()));
                    }
                })
                .exceptionally(e -> {
                    onError.accept("Brak połączenia z serwerem bazy danych.");
                    return null;
                });
    }

    public static void changePassword(String username, String oldPassword, String newPassword, Runnable onSuccess, Consumer<String> onError) {
        JsonObject jsonBody = new JsonObject();
        jsonBody.addProperty("username", username);
        jsonBody.addProperty("old_password", oldPassword);
        jsonBody.addProperty("new_password", newPassword);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/api/change_password"))
                .header("Content-Type", "application/json")
                .PUT(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(response -> {
                    if (response.statusCode() == 200 || response.statusCode() == 201) {
                        onSuccess.run();
                    } else {
                        onError.accept(getErrorMessage(response.body(), response.statusCode()));
                    }
                })
                .exceptionally(e -> {
                    onError.accept("Brak połączenia z serwerem bazy danych.");
                    return null;
                });
    }

    public static void startTraining(Runnable onSuccess, Consumer<String> onError) {
        JsonObject jsonBody = new JsonObject();
        jsonBody.addProperty("user_id", currentUserId);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(TRACKING_URL + "/api/start_training"))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody.toString()))
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(response -> {
                    if (response.statusCode() == 200) {
                        onSuccess.run();
                    } else {
                        onError.accept("Błąd podczas uruchamiania treningu.");
                    }
                })
                .exceptionally(e -> {
                    onError.accept("Brak połączenia z serwerem wideo.");
                    return null;
                });
    }

    public static void checkTrainingStatus(Consumer<Boolean> onStatusReceived) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(TRACKING_URL + "/api/training_status"))
                .GET()
                .build();

        client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenAccept(response -> {
                    if (response.statusCode() == 200) {
                        try {
                            JsonObject json = gson.fromJson(response.body(), JsonObject.class);
                            boolean isRunning = json.get("trening_rozpoczety").getAsBoolean();
                            onStatusReceived.accept(isRunning);
                        } catch (Exception e) {
                            onStatusReceived.accept(false);
                        }
                    } else {
                        onStatusReceived.accept(false);
                    }
                })
                .exceptionally(e -> {
                    onStatusReceived.accept(false);
                    return null;
                });
    }
}