import logging
from datetime import datetime
from nicegui import ui

logger = logging.getLogger()


async def logs():
    log = ui.log(max_lines=10).classes('w-full')

    while True:
        log.clear()
        with open('web.log', 'r') as f:
            for line in f:
                log.push(line)
        await asyncio.sleep(1)



