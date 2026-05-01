## 1. Podstawy komunikacji

Zasady łączenia się z API:
*   **Adres bazowy (Środowisko lokalne):** `http://localhost:5000`
*   **Format wymiany danych:** JSON.

---

## 2. Dostępne Endpointy

Lista aktualnie zaimplementowanych endpointów.

### Logowanie Użytkownika

*   **Endpoint:** `/api/login`

**Zapytanie**
{
  "username": "nazwa_uzytkownika",
  "password": "haslo_uzytkownika"
}
**Odpowiedzi**
HTTP 200 OK:
{
  "message": "Zalogowano pomyślnie!",
  "user_id": 1,
  "username": "admin"
}
HTTP 401 Unauthorized
{
  "error": "Nieprawidłowy login lub hasło"
}
HTTP 400 Bad Request 
{
  "error": "Brak loginu lub hasła"
}