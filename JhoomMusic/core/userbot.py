import sys
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING_SESSION),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant...")
        try:
            await self.one.start()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Assistant Account has failed to access the log Group. Make sure that you have added your assistant to your log channel and promoted as admin! \n\nError: {ex}"
            )
            sys.exit()
        try:
            try:
                await self.one.send_message(config.LOG_GROUP_ID, "Assistant Started")
            except:
                LOGGER(__name__).error(
                    f"Assistant Account has failed to access the log Group. Make sure that you have added your assistant to your log channel and promoted as admin!"
                )
                sys.exit()
            try:
                await self.one.join_chat("JhoomMusicSupport")
                await self.one.join_chat("JhoomMusicChannel")
            except:
                pass
            get_me = await self.one.get_me()
            self.one.username = get_me.username
            self.one.id = get_me.id
            self.one.mention = get_me.mention
            self.one.name = get_me.first_name
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")
        except Exception as ex:
            LOGGER(__name__).error(
                f"Assistant Account has failed to access the log Group.\n  Reason : {ex}"
            )
            sys.exit()

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistant...")
        try:
            await self.one.stop()
        except:
            pass