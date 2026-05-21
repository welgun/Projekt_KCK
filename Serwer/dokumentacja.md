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
```json
{
  "username": "nazwa_uzytkownika",
  "password": "haslo_uzytkownika"
}
```
**Odpowiedzi:**

* **HTTP 200 OK**
```json
{
  "message": "Zalogowano pomyślnie!",
  "user_id": 1,
  "username": "admin"
}
```

* **HTTP 401 Unauthorized**
```json
{
  "error": "Nieprawidłowy login lub hasło"
}
```

* **HTTP 400 Bad Request**
```json
{
  "error": "Brak loginu lub hasła"
}
```

---

### Rejestracja Użytkownika

*   **Endpoint:** `/api/register`
*   **Metoda HTTP:** `POST`

**Zapytanie:**
```json
{
  "username": "nowy_uzytkownik",
  "password": "nowe_haslo"
}
```

**Odpowiedzi:**

* **HTTP 201 Created** (Użytkownik został pomyślnie utworzony)
```json
{
  "message": "Zarejestrowano pomyślnie!",
  "user_id": 2,
  "username": "nowy_uzytkownik"
}
```

* **HTTP 409 Conflict** (Login jest już zajęty)
```json
{
  "error": "Użytkownik o takim loginie już istnieje"
}
```

* **HTTP 400 Bad Request** (Brak wymaganych danych w zapytaniu)
```json
{
  "error": "Brak loginu lub hasła"
}
```

* **HTTP 500 Internal Server Error** 
```json
{
  "error": "Błąd bazy danych podczas rejestracji"
}

### Zmiana hasła

*   **Endpoint:** `/api/change_password`
*   **Metoda HTTP:** `PUT`


**Zapytanie:**
{
    "username": "admin",
    "old_password": "test1234",
    "new_password": "nowe_bezpieczne_haslo"
}

**Odpowiedzi:**

* **HTTP 201 Created**
{
  "message": "Hasło zostało zmienione pomyślnie!"
}

* **HTTP 400 Bad Request** (Brak wszystkich wymaganych pól)
{
  "error": "Brak nazwy użytkownika, starego lub nowego hasła"
}

* **HTTP 401 Unauthorized** (Podano błędne obecne hasło lub użytkownik nie istnieje)
{
  "error": "Nieprawidłowy login lub aktualne hasło"
}
* **HTTP 500 Internal Server Error**
{
  "error": "Błąd bazy danych podczas zmiany hasła"
}

### Usuwanie użytkownika

*   **Endpoint:** `/api/delete_account`
*   **Metoda HTTP:** `DELETE`

* **HTTP 200** (usunięto konto)
{
  "message": "Konto zostało trwale usunięte."
}

* **HTTP 400 Bad Request** (Brak loginu lub hasła w zapytaniu)
{
  "error": "Brak loginu lub hasła"
}

* **HTTP 401 Unauthorized** (Podano błędne hasło przy próbie usunięcia)
{
  "error": "Nieprawidłowy login lub hasło"
}

* **HTTP 500 Internal Server Error**
{
  "error": "Błąd bazy danych podczas usuwania konta"
}