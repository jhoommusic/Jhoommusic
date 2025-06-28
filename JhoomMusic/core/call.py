import asyncio
from typing import Union
from pyrogram import Client
from pyrogram.types import Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, VideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)

import config
from ..logging import LOGGER


class Call:
    def __init__(self):
        self.pytgcalls = PyTgCalls(
            config.userbot,
            cache_duration=100,
        )

    async def pause_stream(self, chat_id: int):
        try:
            await self.pytgcalls.pause_stream(chat_id)
        except:
            pass

    async def resume_stream(self, chat_id: int):
        try:
            await self.pytgcalls.resume_stream(chat_id)
        except:
            pass

    async def stop_stream(self, chat_id: int):
        try:
            await self.pytgcalls.leave_group_call(chat_id)
        except:
            pass

    async def force_stop_stream(self, chat_id: int):
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await self.stop_stream(chat_id)

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        if video:
            stream = VideoPiped(
                link,
                HighQualityVideo(),
                headers=headers,
            )
        else:
            stream = AudioPiped(link, HighQualityAudio(), headers=headers)
        try:
            await self.pytgcalls.change_stream(
                chat_id,
                stream,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error in skip_stream: {e}")
            return False
        return True

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        stream = (
            AudioPiped(
                file_path,
                HighQualityAudio(),
                headers=headers,
                additional_ffmpeg_parameters=f"-ss {to_seek} -t {duration}",
            )
            if mode == "audio"
            else VideoPiped(
                file_path,
                HighQualityVideo(),
                headers=headers,
                additional_ffmpeg_parameters=f"-ss {to_seek} -t {duration}",
            )
        )
        try:
            await self.pytgcalls.change_stream(chat_id, stream)
        except Exception as e:
            LOGGER(__name__).error(f"Error in seek_stream: {e}")
            return False
        return True

    async def stream_call(self, link):
        try:
            await self.pytgcalls.join_group_call(
                config.LOG_GROUP_ID,
                AudioPiped(link, HighQualityAudio(), headers=headers),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error in stream_call: {e}")

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        if video:
            stream = VideoPiped(
                link,
                HighQualityVideo(),
                headers=headers,
            )
        else:
            stream = AudioPiped(link, HighQualityAudio(), headers=headers)
        try:
            await self.pytgcalls.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            LOGGER(__name__).error(f"Error in join_call: {e}")
            return False
        return True

    async def leave_call(self, chat_id: int):
        try:
            await self.pytgcalls.leave_group_call(chat_id)
        except:
            pass

    async def mute_stream(self, chat_id: int):
        try:
            await self.pytgcalls.mute_stream(chat_id)
        except:
            pass

    async def unmute_stream(self, chat_id: int):
        try:
            await self.pytgcalls.unmute_stream(chat_id)
        except:
            pass

    async def decorators(self):
        @self.pytgcalls.on_kicked()
        async def on_kicked(_, chat_id: int):
            LOGGER(__name__).warning(f"Assistant kicked from {chat_id}")

        @self.pytgcalls.on_closed_voice_chat()
        async def on_closed_voice_chat(_, chat_id: int):
            LOGGER(__name__).warning(f"Voice chat closed in {chat_id}")

    async def start(self):
        await self.pytgcalls.start()

    async def stop(self):
        await self.pytgcalls.stop()


Jhoom = Call()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}