import logging

from telebot.types import Message

from ..config import bot
from ..lexicon.lexicon import CMD_MESSAGE, ERROR_MESSAGE
from ..utils.openai_handlers import send_msg_to_gpt
from ..utils.states import GPTHistory

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
async def process_start(message: Message):
    '''Handles start command.'''
    try:
        msg = CMD_MESSAGE['on_start'].format(
            username=message.from_user.username
        )
        await bot.send_message(message.chat.id, text=msg)
    except KeyError as err:
        logger.error(f'KeyError on start {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on start {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on start {err}.', exc_info=True)


@bot.message_handler(commands=['help'])
async def process_help(message: Message):
    '''Handles help command.'''
    try:
        msg = CMD_MESSAGE['on_help']
        await bot.send_message(message.chat.id, text=msg)
    except KeyError as err:
        logger.error(f'KeyError on help {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on help {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on help {err}.', exc_info=True)


@bot.message_handler(commands=['about'])
async def process_about(message: Message):
    '''Handles about command.'''
    try:
        msg = CMD_MESSAGE['on_about']
        await bot.send_message(message.chat.id, text=msg)
    except KeyError as err:
        logger.error(f'KeyError on about {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on about {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on about {err}.', exc_info=True)


@bot.message_handler(commands=['ask'])
async def process_ask(message: Message):
    '''Handles ask command.'''
    try:
        msg = CMD_MESSAGE['on_ask']
        # ошибка при await
        await bot.set_state(
            message.from_user.id,
            GPTHistory.talk_mode
        )
        await bot.send_message(message.chat.id, text=msg)
    except KeyError as err:
        logger.error(f'KeyError on ask {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on ask {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on ask {err}.', exc_info=True)


@bot.message_handler(state=GPTHistory.talk_mode, commands=['restart'])
async def process_restart(message: Message):
    '''Handles restart command with state enabled.'''
    try:
        logger.debug('restart with state')
        chat_id = message.chat.id
        user_id = message.from_user.id
        async with bot.retrieve_data(user_id, chat_id) as data:
            prev_msg = data.get('prev_msg')
            if not prev_msg:
                await bot.send_message(
                    chat_id,
                    text=ERROR_MESSAGE['no_history']
                )
            else:
                data['prev_msg'] = None
        await bot.send_message(user_id, text=CMD_MESSAGE['on_restart'])
        await bot.set_state(user_id, GPTHistory.talk_mode, chat_id)
    except KeyError as err:
        logger.error(f'KeyError on restart {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on restart {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on restart {err}', exc_info=True)


@bot.message_handler(commands=['restart'])
async def process_restart_without_state(message: Message):
    '''Handles restart command without state.'''
    try:
        logger.debug('restart')
        await bot.send_message(
            message.chat.id,
            text=ERROR_MESSAGE['no_talk_state']
        )
    except AttributeError as err:
        logger.error(f'AttrError on restart {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on restart {err}', exc_info=True)


@bot.message_handler(state=GPTHistory.talk_mode.name, commands=['exit'])
async def process_exit(message: Message):
    '''Handles exit command with state enabled.'''
    try:
        await bot.send_message(message.chat.id, text=CMD_MESSAGE['on_exit'])
        await bot.delete_state(message.from_user.id, message.chat.id)
    except KeyError as err:
        logger.error(f'KeyError on restart {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on restart {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on restart {err}', exc_info=True)


@bot.message_handler(commands=['exit'])
async def process_exit_without_sate(message: Message):
    '''Handles exit command without state.'''
    try:
        await bot.send_message(
            message.chat.id,
            text=ERROR_MESSAGE['no_talk_state']
        )
    except KeyError as err:
        logger.error(f'KeyError on restart {err}', exc_info=True)
    except AttributeError as err:
        logger.error(f'AttrError on restart {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on restart {err}', exc_info=True)


@bot.message_handler(state=GPTHistory.talk_mode)
async def process_msg_to_gpt(message: Message):
    '''
    Handles message text with state enabled.

    Sends user message to gpt, awaits answer and responds to user.
    '''
    try:
        logger.debug('Entered talk mode.')
        chat_id = message.chat.id
        user_id = message.from_user.id
        msg = message.text.strip()
        logger.info('Got msg for gpt.')
        async with bot.retrieve_data(user_id, chat_id) as data:
            prev_msg = data.get('prev_msg')
            data['prev_msg'] = msg
        gpt_response = await send_msg_to_gpt(
            new=msg,
            prev=prev_msg,
            username=message.from_user.username
        )
        if gpt_response is not None:
            logger.info('Got response from gpt.')
            await bot.send_message(chat_id, text=gpt_response)
            async with bot.retrieve_data(user_id, chat_id) as data:
                data['prev_msg'] = gpt_response
        else:
            await bot.send_message(
                chat_id, text=ERROR_MESSAGE['on_gpt_error']
            )
        await bot.set_state(user_id, GPTHistory.talk_mode, chat_id)
    except AttributeError as err:
        logger.error(f'AttrError on message {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error processing msg {err}', exc_info=True)


@bot.message_handler()
async def process_msg_without_state(message: Message):
    '''Handles other messages without state.'''
    try:
        logger.info('Out of conversation.')
        await bot.send_message(
            message.chat.id,
            text=ERROR_MESSAGE['no_talk_state']
        )
        state = await bot.get_state(message.from_user.id, message.chat.id)
        print(state)
    except AttributeError as err:
        logger.error(f'AttrError on restart {err}', exc_info=True)
    except Exception as err:
        logger.error(f'Error on restart {err}', exc_info=True)
