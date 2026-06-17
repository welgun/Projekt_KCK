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
```
### Zmiana hasła

*   **Endpoint:** `/api/change_password`
*   **Metoda HTTP:** `PUT`


**Zapytanie:**
```json
{
    "username": "admin",
    "old_password": "test1234",
    "new_password": "nowe_bezpieczne_haslo"
}
```

**Odpowiedzi:**

* **HTTP 201 Created**
```json
{
  "message": "Hasło zostało zmienione pomyślnie!"
}
```

* **HTTP 400 Bad Request** (Brak wszystkich wymaganych pól)
```json
{
  "error": "Brak nazwy użytkownika, starego lub nowego hasła"
}
```

* **HTTP 401 Unauthorized** (Podano błędne obecne hasło lub użytkownik nie istnieje)
```json
{
  "error": "Nieprawidłowy login lub aktualne hasło"
}
```
* **HTTP 500 Internal Server Error**
```json
{
  "error": "Błąd bazy danych podczas zmiany hasła"
}
```

### Usuwanie użytkownika

*   **Endpoint:** `/api/delete_account`
*   **Metoda HTTP:** `DELETE`

* **HTTP 200** (usunięto konto)
```json
{
  "message": "Konto zostało trwale usunięte."
}
```

* **HTTP 400 Bad Request** (Brak loginu lub hasła w zapytaniu)
```json
{
  "error": "Brak loginu lub hasła"
}
```

* **HTTP 401 Unauthorized** (Podano błędne hasło przy próbie usunięcia)
```json
{
  "error": "Nieprawidłowy login lub hasło"
}
```

* **HTTP 500 Internal Server Error**
```json
{
  "error": "Błąd bazy danych podczas usuwania konta"
}
```

### Zapis Treningu (Statystyk)

Zapisuje statystyki z treningu do bazy danych. Wymaga podania `user_id`.

* **Endpoint:** `/api/stats/save`
* **Metoda HTTP:** `POST`

**Zapytanie:**
{
  "user_id": 1,
  "date": "2026-06-17",
  "reps_done": 12,
  "reps_goal": 15,
  "is_goal_achieved": false,
  "duration_seconds": 120
}

**Odpowiedzi:**
* 🟢 **HTTP 201 Created** {
  "message": "Trening zapisany pomyślnie!",
  "training_id": 1
}
* 🔴 **HTTP 400 Bad Request** (Brak któregoś z pól)


### Pobieranie Statystyk Użytkownika

Zwraca listę wszystkich treningów przypisanych do danego użytkownika (od najnowszego). Zmienną `user_id` należy przekazać jako parametr URL (?user_id=X).

* **Endpoint:** `/api/stats/get?user_id={id}` (np. /api/stats/get?user_id=1)
* **Metoda HTTP:** `GET`

**Zapytanie:**
(Brak ciała zapytania - nie wysyłamy JSON-a, używamy tylko adresu URL z parametrem)

**Odpowiedzi:**
* 🟢 **HTTP 200 OK** (Zwraca tablicę obiektów. Może być pusta [])
[
  {
    "id": 5,
    "user_id": 1,
    "date": "2026-06-17",
    "reps_done": 12,
    "reps_goal": 15,
    "is_goal_achieved": 0,
    "duration_seconds": 120
  }
]
* 🔴 **HTTP 400 Bad Request** {
  "error": "Brak parametru user_id w adresie URL"
}