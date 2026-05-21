import requests

BASE_URL = 'http://127.0.0.1:5000/api'

# Dane testowego użytkownika
USERNAME = "konto_testowe"
PASSWORD = "moje_stare_haslo"
NEW_PASSWORD = "moje_nowe_haslo"

print("=== START TESTÓW API ===\n")

print("1. TEST REJESTRACJI")
res_register = requests.post(f"{BASE_URL}/register", json={
    "username": USERNAME,
    "password": PASSWORD
})
print(f"Status: {res_register.status_code} | Odpowiedź: {res_register.json()}\n")

print("2. TEST ZMIANY HASŁA")
res_change_pw = requests.put(f"{BASE_URL}/change_password", json={
    "username": USERNAME,
    "old_password": PASSWORD,
    "new_password": NEW_PASSWORD
})
print(f"Status: {res_change_pw.status_code} | Odpowiedź: {res_change_pw.json()}\n")

print("3. TEST LOGOWANIA STARYM HASŁEM (OCZEKIWANY BŁĄD)")
res_login_old = requests.post(f"{BASE_URL}/login", json={
    "username": USERNAME,
    "password": PASSWORD
})
print(f"Status: {res_login_old.status_code} | Odpowiedź: {res_login_old.json()}\n")

print("4. TEST LOGOWANIA NOWYM HASŁEM")
res_login_new = requests.post(f"{BASE_URL}/login", json={
    "username": USERNAME,
    "password": NEW_PASSWORD
})
print(f"Status: {res_login_new.status_code} | Odpowiedź: {res_login_new.json()}\n")

print("5. TEST USUWANIA KONTA")
res_delete = requests.delete(f"{BASE_URL}/delete_account", json={
    "username": USERNAME,
    "password": NEW_PASSWORD
})
print(f"Status: {res_delete.status_code} | Odpowiedź: {res_delete.json()}\n")

print("6. TEST LOGOWANIA PO USUNIĘCIU KONTA (OCZEKIWANY BŁĄD)")
res_login_deleted = requests.post(f"{BASE_URL}/login", json={
    "username": USERNAME,
    "password": NEW_PASSWORD
})
print(f"Status: {res_login_deleted.status_code} | Odpowiedź: {res_login_deleted.json()}\n")

print("=== KONIEC TESTÓW ===")