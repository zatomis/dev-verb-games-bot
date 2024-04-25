import telegram
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
import logging
import vk_api as vk
import google_dialogflow as gd
from vk_api.exceptions import ApiError
from contextlib import suppress
from alerts import TelegramLogsHandler, handle_error

logger = logging.getLogger(__name__)

def get_dialogflow(event, vk_api, pid, sid, lcode):
    is_fallback, fulfillment_text = gd.detect_intent_texts(pid, sid, event.text, lcode)
    if not is_fallback:
        with suppress(ApiError):
            vk_api.messages.send(user_id=event.user_id,
            message=fulfillment_text, random_id=random.randint(10, 100))



if __name__ == "__main__":
    env: Env = Env()
    env.read_env()
    vk_key_token = env('VK_KEY')
    project_id = env('PROJECT_ID')
    language_code = env('LANGUAGE_CODE')
    vk_session = vk.VkApi(token=vk_key_token)
    vk_api = vk_session.get_api()
    telegram_logs = env.str('TELEGRAM_LOGS_TOKEN')
    chat_id = env.int('TELEGRAM_CHAT_ID')
    tg_bot_logs = telegram.Bot(token=telegram_logs)
    logger.setLevel(logging.INFO)
    telegram_logs_handler = TelegramLogsHandler(
        tg_bot=tg_bot_logs,
        chat_id=chat_id
    )
    logger.addHandler(telegram_logs_handler)
    logger.info('Бот Игра глаголов запущен в vk')

    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    get_dialogflow(event, vk_api, project_id, f'vk{event.user_id}', language_code)
        except Exception as e:
            handle_error(e)
            continue

