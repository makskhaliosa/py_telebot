import logging

from openai import AsyncStream
from telebot.async_telebot import AsyncTeleBot

from ..config import gpt_client

logger = logging.getLogger(__name__)


async def _get_gpt_response(new: str, prev: str | None, username: str) -> str:
    '''
    Accepts new, previous user mesages and username and sends them to GPT.

    Returns stream with partial reponses to itirate through.
    '''
    try:
        logger.info('Sending msg to gpt...')
        message_with_context = [
            {'role': 'user', 'content': prev, 'name': username},
            {'role': 'user', 'content': new, 'name': username}
        ]
        message_without_context = [
            {'role': 'user', 'content': new, 'name': username}
        ]
        stream = await gpt_client.chat.completions.create(
            messages=message_with_context if prev else message_without_context,
            model='gpt-4',
            temperature=0,
            stream=True
        )
        return stream
    except Exception as err:
        logger.error(f'Error getting gpt response {err}', exc_info=True)
        return None


async def _handle_stream(
        stream: AsyncStream,
        chat_id: int,
        bot: AsyncTeleBot
) -> str:
    '''
    Itirates through gpt stream.

    Sends parts of message to user as they come from stream.
    '''
    try:
        full_response = ''
        sent_msg_id = None
        async for chunk in stream:
            msg_piece = chunk.choices[0].delta.content
            if msg_piece:
                full_response += msg_piece
                if sent_msg_id is None:
                    msg = await bot.send_message(chat_id, full_response)
                    sent_msg_id = msg.id
                else:
                    await bot.edit_message_text(
                        text=full_response,
                        chat_id=chat_id,
                        message_id=sent_msg_id
                    )
        return full_response if full_response else None
    except TypeError as err:
        logger.error(f'TypeError in handle stream {err}', exc_info=True)
        return None
    except Exception as err:
        logger.error(f'Error in handle stream {err}', exc_info=True)
        return None


async def handle_msg_exchange(
        new: str,
        prev: str | None,
        username: str,
        chat_id: int,
        bot: AsyncTeleBot
) -> str:
    '''
    Accepts new, previous user mesages, username, chat_id and bot instance.

    Handles sending message to user and returns full reponse.
    '''
    try:
        gpt_stream = await _get_gpt_response(
            new=new,
            prev=prev,
            username=username
        )
        if gpt_stream is not None:
            logger.info('Got response from gpt.')
            full_response = await _handle_stream(gpt_stream, chat_id, bot)
            return full_response
        logger.warning('Did not get any response.')
        return None
    except Exception as err:
        logger.error(f'Error in send msg to gpt {err}', exc_info=True)
        return None
