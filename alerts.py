import logging
import time

logger = logging.getLogger('Telegram bot logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def handle_error(exception):
    logger.exception(f'Бот завершил работу с ошибкой: {exception}', exc_info=True)
    logger.info('Бот будет перезапущен через 10 минут')
    time.sleep(600)
    logger.info('Бот Игра Глаголов запущен в vk')