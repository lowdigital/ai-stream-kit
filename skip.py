import time
import pytchat
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_DOMAIN  = os.getenv("API_DOMAIN")
STREAM_ID   = os.getenv("STREAM_ID")

def console_msg(message, color='white'):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    colors = {
        'white': '\x1b[37m',
        'yellow': '\x1b[33m',
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'pink': '\x1b[35m',
        'cyan': '\x1b[38;5;51m'
    }
    text_color = colors.get(color, colors['white'])
    print(f'\x1b[36m{formatted_date}\x1b[0m {text_color}{message}\x1b[0m')
    
def send_skip_request(username):
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(f"https://{API_DOMAIN}/app/api/skip-push.php", data={"name": username}, headers=headers)
        if response.status_code == 200:
            console_msg(f"Запрос на пропуск сценария успешно отправлен для пользователя {username}", 'green')
        else:
            console_msg(f"Ошибка при отправке запроса для пользователя {username}. Статус: {response.status_code}", 'red')
            print(response.text)
    except Exception as e:
        console_msg("Ошибка при отправке запроса:", 'red')
        print(e)

while True:
    try:
        chat = pytchat.create(video_id=STREAM_ID)
        while chat.is_alive():
            try:
                for c in chat.get().sync_items():
                    console_msg(f"[{c.author.name}]: {c.message}")
                    if "/skip" in c.message:
                        send_skip_request(c.author.name)
            except Exception as e:
                console_msg(f"Ошибка при получении сообщений чата:", 'red')
                print(e)
                time.sleep(5)
                break
    except Exception as e:
        console_msg(f"Ошибка при создании объекта чата: {e}", 'red')
        print(e)
        time.sleep(5)