"""
Core voice chat handler using TgCaller
"""

from typing import Union, Dict, Optional
from tgcaller import TgCaller
from tgcaller.exceptions import NoActiveGroupCall

from JhoomMusic import app, userbot
from JhoomMusic.logging import LOGGER

# Global state
db: Dict[int, list] = {}          # chat_id -> queue of tracks
active_chats: Dict[int, dict] = {}  # chat_id -> current playing info


class Call:
    def __init__(self):
        # Prefer userbot for better stability in voice chats
        client = userbot if userbot else app
        self.tgcaller = TgCaller(client)

    # -------------------- Basic Controls --------------------

    async def pause_stream(self, chat_id: int) -> bool:
        try:
            await self.tgcaller.pause_stream(chat_id)
            if chat_id in active_chats:
                active_chats[chat_id]["playing"] = False
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Pause error [{chat_id}]: {e}")
            return False

    async def resume_stream(self, chat_id: int) -> bool:
        try:
            await self.tgcaller.resume_stream(chat_id)
            if chat_id in active_chats:
                active_chats[chat_id]["playing"] = True
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Resume error [{chat_id}]: {e}")
            return False

    async def mute_stream(self, chat_id: int) -> bool:
        try:
            await self.tgcaller.mute_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Mute error [{chat_id}]: {e}")
            return False

    async def unmute_stream(self, chat_id: int) -> bool:
        try:
            await self.tgcaller.unmute_stream(chat_id)
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Unmute error [{chat_id}]: {e}")
            return False

    async def stop_stream(self, chat_id: int) -> bool:
        """Stop playback and leave the voice chat"""
        try:
            await self.tgcaller.leave_call(chat_id)
        except Exception:
            pass

        if chat_id in db:
            db[chat_id].clear()
        if chat_id in active_chats:
            del active_chats[chat_id]

        return True

    async def leave_call(self, chat_id: int) -> bool:
        return await self.stop_stream(chat_id)

    # -------------------- Core Streaming --------------------

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link: str,
        video: Union[bool, str] = False,
    ) -> bool:
        """
        Join voice chat and start playing.
        `link` can be a direct stream URL or a local file path.
        """
        try:
            # Join the call first
            await self.tgcaller.join_call(chat_id)

            # Start playing
            await self.tgcaller.play(chat_id, link)

            active_chats[chat_id] = {
                "playing": True,
                "original_chat_id": original_chat_id,
                "stream_type": "video" if video else "audio",
                "current": link,
            }
            return True

        except NoActiveGroupCall:
            LOGGER(__name__).error(f"No active voice chat in {chat_id}")
            return False
        except Exception as e:
            LOGGER(__name__).error(f"Join/Play error [{chat_id}]: {e}")
            return False

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = False,
    ) -> bool:
        """Skip to a new track (change current stream)"""
        try:
            # TgCaller play() on already joined call changes the stream
            await self.tgcaller.play(chat_id, link)

            if chat_id in active_chats:
                active_chats[chat_id]["current"] = link
                active_chats[chat_id]["playing"] = True
                active_chats[chat_id]["stream_type"] = "video" if video else "audio"
            else:
                active_chats[chat_id] = {
                    "playing": True,
                    "original_chat_id": chat_id,
                    "stream_type": "video" if video else "audio",
                    "current": link,
                }
            return True
        except Exception as e:
            LOGGER(__name__).error(f"Skip error [{chat_id}]: {e}")
            return False

    # -------------------- Queue Helpers --------------------

    def get_queue(self, chat_id: int) -> list:
        return db.get(chat_id, [])

    def add_to_queue(self, chat_id: int, track: dict):
        if chat_id not in db:
            db[chat_id] = []
        db[chat_id].append(track)

    def clear_queue(self, chat_id: int):
        if chat_id in db:
            db[chat_id].clear()

    def is_active(self, chat_id: int) -> bool:
        return chat_id in active_chats

    # -------------------- Event Handlers --------------------

    async def decorators(self):
        @self.tgcaller.on_kicked()
        async def on_kicked(_, chat_id: int):
            LOGGER(__name__).warning(f"Kicked from {chat_id}")
            if chat_id in active_chats:
                del active_chats[chat_id]
            if chat_id in db:
                db[chat_id].clear()

        @self.tgcaller.on_closed_voice_chat()
        async def on_closed(_, chat_id: int):
            LOGGER(__name__).warning(f"Voice chat closed in {chat_id}")
            if chat_id in active_chats:
                del active_chats[chat_id]
            if chat_id in db:
                db[chat_id].clear()

        @self.tgcaller.on_stream_end()
        async def on_stream_end(_, update):
            chat_id = update.chat_id
            LOGGER(__name__).info(f"Stream ended in {chat_id}")

            # Play next from queue if available
            if chat_id in db and db[chat_id]:
                next_track = db[chat_id].pop(0)
                link = next_track.get("file") or next_track.get("url")
                video = next_track.get("video", False)

                success = await self.skip_stream(chat_id, link, video)
                if not success:
                    await self.leave_call(chat_id)
            else:
                await self.leave_call(chat_id)

    # -------------------- Lifecycle --------------------

    async def start(self):
        await self.tgcaller.start()
        LOGGER(__name__).info("TgCaller started")

    async def stop(self):
        try:
            await self.tgcaller.stop()
        except Exception:
            pass
        LOGGER(__name__).info("TgCaller stopped")


# Global instance
Jhoom = Call()
