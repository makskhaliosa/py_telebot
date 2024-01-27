import asyncio
import logging
import sys

from src.config import bot, bot_commands
from src.services import handlers

logger = logging.getLogger(__name__)


async def main():
    '''Starts bot.'''
    await bot.delete_my_commands()
    await bot.set_my_commands(commands=bot_commands)
    logger.info('Starting bot.')
    await bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error('Interrupted. Stopping bot.')
        sys.exit()
