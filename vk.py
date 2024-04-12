from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
import random
import vk_api as vk


env: Env = Env()
env.read_env()
vk_key_token = env('VK_KEY')
project_id = env('PROJECT_ID')
session_id = env('SESSION_ID')
language_code = env('LANGUAGE_CODE')


def detect_intent_texts(project_id, session_id, texts, language_code):
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return str(response.query_result.fulfillment_text)


def echo(event, vk_api):
    vk_api.messages.send(user_id=event.user_id,
        message=detect_intent_texts(project_id, session_id, event.text, language_code), random_id=random.randint(10,100))


if __name__ == "__main__":
    vk_session = vk.VkApi(token=vk_key_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
