# Dokumentacja API (Serwer Flask)

## 1. Podstawy komunikacji

Zasady łączenia się z API:
*   **Adres bazowy (Środowisko lokalne):** `http://localhost:5000`
*   **Format wymiany danych:** JSON.
*   **Wymagany nagłówek dla zapytań POST:** `Content-Type: application/json`

---

## 2. Dostępne Endpointy

Lista aktualnie zaimplementowanych endpointów.

### Logowanie Użytkownika

*   **Endpoint:** `/api/login`
*   **Metoda HTTP:** `POST`

**Zapytanie:**
{
  "username": "nazwa_uzytkownika",
  "password": "haslo_uzytkownika"
}

**Odpowiedzi:**

* **HTTP 200 OK**
{
  "message": "Zalogowano pomyślnie!",
  "user_id": 1,
  "username": "admin"
}

* **HTTP 401 Unauthorized**
{
  "error": "Nieprawidłowy login lub hasło"
}

* **HTTP 400 Bad Request**
{
  "error": "Brak loginu lub hasła"
}

---

### Rejestracja Użytkownika

*   **Endpoint:** `/api/register`
*   **Metoda HTTP:** `POST`

**Zapytanie:**
{
  "username": "nowy_uzytkownik",
  "password": "nowe_haslo"
}

**Odpowiedzi:**

* **HTTP 201 Created** (Użytkownik został pomyślnie utworzony)
{
  "message": "Zarejestrowano pomyślnie!",
  "user_id": 2,
  "username": "nowy_uzytkownik"
}

* **HTTP 409 Conflict** (Login jest już zajęty)
{
  "error": "Użytkownik o takim loginie już istnieje"
}

* **HTTP 400 Bad Request** (Brak wymaganych danych w zapytaniu)
{
  "error": "Brak loginu lub hasła"
}

* **HTTP 500 Internal Server Error** 
{
  "error": "Błąd bazy danych podczas rejestracji"
}