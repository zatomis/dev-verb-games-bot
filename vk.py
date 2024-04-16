from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
import vk_api as vk
import google_dialogflow as gd
from vk_api.exceptions import ApiError
from contextlib import suppress


def get_dialogflow(event, vk_api):
    with suppress(ApiError):
        vk_api.messages.send(user_id=event.user_id,
        message=gd.detect_intent_texts(project_id, session_id, event.text, language_code),
                             random_id=random.randint(10, 100))



if __name__ == "__main__":
    env: Env = Env()
    env.read_env()
    vk_key_token = env('VK_KEY')
    project_id = env('PROJECT_ID')
    session_id = env('SESSION_ID')
    language_code = env('LANGUAGE_CODE')
    vk_session = vk.VkApi(token=vk_key_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_dialogflow(event, vk_api)
