import logging

from ..config import gpt_client

logger = logging.getLogger(__name__)


async def send_msg_to_gpt(new: str, prev: str | None, username: str) -> str:
    '''
    Accepts new and previous user mesages and sends them to GPT.

    Returns text of gpt response.
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
        response = await gpt_client.chat.completions.create(
            messages=message_with_context if prev else message_without_context,
            model='gpt-4',
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as err:
        logger.error(f'Error getting gpt response {err}', exc_info=True)
