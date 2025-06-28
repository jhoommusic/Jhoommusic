import asyncio
from typing import Union, Dict, Optional
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
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ..logging import LOGGER

# Global variables for queue management
db = {}
active_chats = {}

class Call:
    def __init__(self):
        self.pytgcalls = PyTgCalls(
            config.userbot if config.userbot else config.app,
            cache_duration=100,
        )

    async def pause_stream(self, chat_id: int):
        """Pause the current stream"""
        try:
            await self.pytgcalls.pause_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error pausing stream in {chat_id}: {e}")
            return False

    async def resume_stream(self, chat_id: int):
        """Resume the paused stream"""
        try:
            await self.pytgcalls.resume_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error resuming stream in {chat_id}: {e}")
            return False

    async def stop_stream(self, chat_id: int):
        """Stop the current stream and leave call"""
        try:
            await self.pytgcalls.leave_group_call(chat_id)
            if chat_id in db:
                db[chat_id].clear()
            if chat_id in active_chats:
                del active_chats[chat_id]
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error stopping stream in {chat_id}: {e}")
            return False

    async def skip_stream(self, chat_id: int, link: str, video: Union[bool, str] = None):
        """Skip to next track"""
        try:
            if video:
                stream = VideoPiped(
                    link,
                    HighQualityVideo(),
                    headers=self.get_headers(),
                )
            else:
                stream = AudioPiped(
                    link, 
                    HighQualityAudio(), 
                    headers=self.get_headers()
                )
            
            await self.pytgcalls.change_stream(chat_id, stream)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error skipping stream in {chat_id}: {e}")
            return False

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link: str,
        video: Union[bool, str] = None,
    ):
        """Join voice chat and start streaming"""
        try:
            if video:
                stream = VideoPiped(
                    link,
                    HighQualityVideo(),
                    headers=self.get_headers(),
                )
            else:
                stream = AudioPiped(
                    link, 
                    HighQualityAudio(), 
                    headers=self.get_headers()
                )

            await self.pytgcalls.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().local_stream,
            )
            
            active_chats[chat_id] = {
                "playing": True,
                "original_chat_id": original_chat_id,
                "stream_type": "video" if video else "audio"
            }
            
            return True
        except NoActiveGroupCall:
            LOGGER(__name__).error(f"No active voice chat in {chat_id}")
            return False
        except Exception as e:
            LOGGER(__name__).error(f"Error joining call in {chat_id}: {e}")
            return False

    async def leave_call(self, chat_id: int):
        """Leave voice chat"""
        try:
            await self.pytgcalls.leave_group_call(chat_id)
            if chat_id in active_chats:
                del active_chats[chat_id]
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error leaving call in {chat_id}: {e}")
            return False

    async def mute_stream(self, chat_id: int):
        """Mute the stream"""
        try:
            await self.pytgcalls.mute_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error muting stream in {chat_id}: {e}")
            return False

    async def unmute_stream(self, chat_id: int):
        """Unmute the stream"""
        try:
            await self.pytgcalls.unmute_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Error unmuting stream in {chat_id}: {e}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """Get headers for streaming"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def decorators(self):
        """Set up event decorators"""
        @self.pytgcalls.on_kicked()
        async def on_kicked(_, chat_id: int):
            LOGGER(__name__).warning(f"Assistant kicked from {chat_id}")
            if chat_id in active_chats:
                del active_chats[chat_id]

        @self.pytgcalls.on_closed_voice_chat()
        async def on_closed_voice_chat(_, chat_id: int):
            LOGGER(__name__).warning(f"Voice chat closed in {chat_id}")
            if chat_id in active_chats:
                del active_chats[chat_id]

        @self.pytgcalls.on_stream_end()
        async def on_stream_end(_, update):
            chat_id = update.chat_id
            LOGGER(__name__).info(f"Stream ended in {chat_id}")
            
            # Check if there are more tracks in queue
            if chat_id in db and db[chat_id]:
                # Play next track
                next_track = db[chat_id].pop(0)
                await self.skip_stream(
                    chat_id, 
                    next_track["file"], 
                    next_track.get("video", False)
                )
            else:
                # No more tracks, leave call
                await self.leave_call(chat_id)

    async def start(self):
        """Start PyTgCalls"""
        await self.pytgcalls.start()
        LOGGER(__name__).info("PyTgCalls started successfully")

    async def stop(self):
        """Stop PyTgCalls"""
        await self.pytgcalls.stop()
        LOGGER(__name__).info("PyTgCalls stopped")

# Create global instance
Jhoom = Call()