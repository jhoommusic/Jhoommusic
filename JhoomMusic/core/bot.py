import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

import config
from ..logging import LOGGER


class JhoomBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "JhoomMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = self.first_name = get_me.first_name
        self.mention = get_me.mention

        try:
            await self.send_message(
                config.LOG_GROUP_ID, "Bot Started Successfully"
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()
        
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote Bot as Admin in Logger Group"
            )
            sys.exit()
        
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()