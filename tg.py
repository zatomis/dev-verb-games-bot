import logging
import telegram
import google_dialogflow as gd
from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from functools import partial
from alerts import TelegramLogsHandler, handle_error

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )



def get_dialogflow(update: Update, context: CallbackContext, pid, sid, lcode) -> None:
    try:
        update.message.reply_text(gd.detect_intent_texts(pid, sid, update.message.text, lcode))
    except Exception as e:
        handle_error(e)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    env: Env = Env()
    env.read_env()
    token_bot = env('VERBBOT_TOKEN')
    project_id = env('PROJECT_ID')
    session_id = env('SESSION_ID_TG')
    language_code = env('LANGUAGE_CODE')
    updater = Updater(token_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                          partial(get_dialogflow, pid=project_id, sid=session_id, lcode=language_code)))

    telegram_logs = env.str('TELEGRAM_LOGS_TOKEN')
    chat_id = env.int('TELEGRAM_CHAT_ID')
    tg_bot_logs = telegram.Bot(token=telegram_logs)
    logger.setLevel(logging.INFO)
    telegram_logs_handler = TelegramLogsHandler(
        tg_bot=tg_bot_logs,
        chat_id=chat_id
    )
    logger.addHandler(telegram_logs_handler)
    logger.info('Бот Игра глаголов запущен в telegram')

    while True:
        try:
            updater.start_polling()
            updater.idle()
        except Exception as e:
            handle_error(e)
            continue
