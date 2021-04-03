import os

import requests
import telegram
from dotenv import load_dotenv


def send_message_to_telegram(bot, telegram_chat_id, mark, lesson_title, lesson_url):
    if mark:
        mark = 'К сожалению, в работе нашлись ошибки.'
    else:
        mark = 'Преподавателю все понравилось. Можно приступать к следующему уроку!'
    lesson_url = 'https://dvmn.org' + lesson_url
    bot.send_message(
        chat_id=telegram_chat_id,
        text=f'У вас проверили работу "{lesson_title}". {mark} Ссылка на задачу: {lesson_url}',
    )


def get_long_polling_checks(devman_token, bot, telegram_chat_id):
    url = 'https://dvmn.org/api/long_polling/'
    header = {'Authorization': f'Token {devman_token}'}
    payload = {}
    while True:
        try:
            response = requests.get(url, headers=header, params=payload)
            response = response.json()
            if response['status'] == 'found':
                new_attempts = response['new_attempts'][0]
                mark = new_attempts['is_negative']
                lesson_title = new_attempts['lesson_title']
                lesson_url = new_attempts['lesson_url']
                send_message_to_telegram(bot, telegram_chat_id, mark, lesson_title, lesson_url)
                payload = {'timestamp': new_attempts['timestamp']}
            if response['status'] == 'timeout':
                payload = {'timestamp': response['timestamp_to_request']}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue


def main():
    load_dotenv()
    devman_token = os.getenv("DEVMAN_TOKEN")
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = telegram.Bot(token=telegram_bot_token)
    get_long_polling_checks(devman_token, bot, telegram_chat_id)


if __name__ == '__main__':
    main()
