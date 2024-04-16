import logging
import google_dialogflow as gd
from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )



def get_dialogflow(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(gd.detect_intent_texts(project_id, session_id, update.message.text, language_code))


def main() -> None:
    updater = Updater(token_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_dialogflow))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    env: Env = Env()
    env.read_env()
    token_bot = env('VERBBOT_TOKEN')
    project_id = env('PROJECT_ID')
    session_id = env('SESSION_ID')
    language_code = env('LANGUAGE_CODE')
    main()
