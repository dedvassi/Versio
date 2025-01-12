import requests
import webbrowser
import time

# URL вашего сервера
SERVER_URL = "https://versio-server.onrender.com"


def start_oauth_process():
    """
    Инициирует процесс авторизации через сервер.
    """
    try:
        # Запрашиваем ссылку авторизации у сервера
        print("Запрашиваем ссылку авторизации у сервера...")
        response = requests.get(f"{SERVER_URL}/authorize")
        if response.status_code == 200:
            auth_url = response.json().get("auth_url")
            if auth_url:
                print(f"Открываем ссылку авторизации в браузере: {auth_url}")
                webbrowser.open(auth_url)  # Открываем ссылку авторизации в браузере

                # Ждем получения токена
                print("Ожидаем получения токена от сервера...")
                wait_for_token()
            else:
                print("Ошибка: сервер не вернул ссылку авторизации.")
        else:
            print(f"Ошибка: не удалось получить ссылку авторизации. Код ответа: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при попытке авторизации: {e}")


def wait_for_token():
    """
    Ждет получения токена от сервера.
    """
    while True:
        try:
            # Проверяем наличие токена на сервере
            response = requests.get(f"{SERVER_URL}/check_token")
            if response.status_code == 200:
                token = response.json().get("access_token")
                if token:
                    print(f"Токен успешно получен: {token}")
                    save_token(token)
                    break
            elif response.status_code == 202:
                # Токен пока недоступен, ждем
                time.sleep(2)
            else:
                print(f"Ошибка при проверке токена. Код ответа: {response.status_code}")
                break
        except Exception as e:
            print(f"Произошла ошибка при ожидании токена: {e}")
            break


def save_token(token):
    """
    Сохраняет токен в файл.
    """
    try:
        with open("token.txt", "w") as f:
            f.write(token)
        print("Токен сохранён в файл.")
    except Exception as e:
        print(f"Произошла ошибка при сохранении токена: {e}")


if __name__ == "__main__":
    # Запуск процесса авторизации
    start_oauth_process()
