from telebot.asyncio_handler_backends import State, StatesGroup


class GPTHistory(StatesGroup):
    '''Состояния для разговора с чатом.'''
    prev_msg = State()
    talk_mode = State()
