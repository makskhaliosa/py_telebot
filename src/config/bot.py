from openai import AsyncOpenAI
from telebot.asyncio_filters import StateFilter
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.types import BotCommand

from .settings import settings

bot = AsyncTeleBot(
    token=settings.BOT_KEY,
    parse_mode='html',
    state_storage=StateMemoryStorage()
)

bot_commands = [
    BotCommand('start', 'Запустить бота'),
    BotCommand('ask', 'Начать разговор с ChatGPT'),
    BotCommand('restart', 'Обнулить контекст разговора'),
    BotCommand('exit', 'Завершить разговор с ChatGPT'),
    BotCommand('about', 'Информация о боте'),
    BotCommand('help', 'Показать инструкцию')
]

bot.add_custom_filter(StateFilter(bot))

gpt_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
