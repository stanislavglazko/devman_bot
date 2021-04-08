import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


class TelegramLogsHandler(logging.Handler):
    def __init__(self, telegram_bot, telegram_chat_id):
        super().__init__()
        self.bot = telegram_bot
        self.telegram_chat_id = telegram_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.telegram_chat_id, text=log_entry)


def send_message_to_telegram(bot, telegram_chat_id, mark, lesson_title, lesson_url):
    if mark:
        mark = 'К сожалению, в работе нашлись ошибки.'
    else:
        mark = 'Преподавателю все понравилось. Можно приступать к следующему уроку!'
    lesson_url = f'https://dvmn.org{lesson_url}'
    bot.send_message(
        chat_id=telegram_chat_id,
        text=f'У вас проверили работу "{lesson_title}". {mark} Ссылка на задачу: {lesson_url}',
    )


def get_long_polling_checks(devman_token, bot, telegram_chat_id, logger):
    url = 'https://dvmn.org/api/long_polling/'
    header = {'Authorization': f'Token {devman_token}'}
    payload = {}
    while True:
        try:
            response = requests.get(url, headers=header, params=payload)
            unpacked_response = response.json()
            if unpacked_response['status'] == 'found':
                teacher_answer = unpacked_response['new_attempts'][0]
                mark = teacher_answer['is_negative']
                lesson_title = teacher_answer['lesson_title']
                lesson_url = teacher_answer['lesson_url']
                send_message_to_telegram(bot, telegram_chat_id, mark, lesson_title, lesson_url)
                payload = {'timestamp': teacher_answer['timestamp']}
            if unpacked_response['status'] == 'timeout':
                payload = {'timestamp': unpacked_response['timestamp_to_request']}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(60)
            continue


def main():
    load_dotenv()
    devman_token = os.environ["DEVMAN_TOKEN"]
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
    bot = telegram.Bot(token=telegram_bot_token)
    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, telegram_chat_id))
    while True:
        try:
            x = 2 / 0
            get_long_polling_checks(devman_token, bot, telegram_chat_id, logger)
        except Exception as e:
            cause = e.__cause__
            exc_info = (cause.__class__, cause, cause.__traceback__)
            logger.error(str(e), exc_info=exc_info)


if __name__ == '__main__':
    main()
