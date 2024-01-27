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
        response = await gpt_client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': prev, 'name': username},
                {'role': 'user', 'content': new, 'name': username}
            ],
            model='gpt-4',
            temperature=5
        )
        return response.choices[0].message.content
    except Exception as err:
        logger.error(f'Error getting gpt response {err}', exc_info=True)
