from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import config

TEMP_MONGODB = "mongodb+srv://JhoomMusic:JhoomMusic@cluster0.example.mongodb.net/?retryWrites=true&w=majority"

if config.MONGO_DB_URI is None:
    LOGGER(__name__).warning(
        "No MONGO DB URL found.. Your Bot will work on Jhoom's Database"
    )
    temp_client = MongoClient(TEMP_MONGODB)
    temp_db = temp_client.Jhoom
else:
    temp_client = MongoClient(config.MONGO_DB_URI)
    temp_db = temp_client.Jhoom


async def _get_lang(chat_id: int) -> str:
    _lang = await temp_db.language.find_one({"chat_id": chat_id})
    if _lang:
        return _lang["language"]
    return "en"


async def _get_playmode(chat_id: int) -> str:
    mode = await temp_db.playmode.find_one({"chat_id": chat_id})
    if not mode:
        return "Direct"
    return mode["mode"]


async def _get_playtype(chat_id: int) -> str:
    mode = await temp_db.playtypes.find_one({"chat_id": chat_id})
    if not mode:
        return "Everyone"
    return mode["mode"]


async def _get_authuser_names(chat_id: int):
    _notes = []
    async for x in temp_db.authuser.find({"chat_id": chat_id}):
        _notes.append(x)
    return _notes


async def _get_authuser(chat_id: int, user_id: int) -> bool:
    user = await temp_db.authuser.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )
    if not user:
        return False
    return True


async def save_authuser(chat_id: int, user_id: int, user_name):
    await temp_db.authuser.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"user_name": user_name}},
        upsert=True,
    )


async def delete_authuser(chat_id: int, user_id: int):
    await temp_db.authuser.delete_many(
        {"chat_id": chat_id, "user_id": user_id}
    )


async def is_nonadmin(chat_id: int, user_id: int) -> bool:
    user = await temp_db.authuser.find_one(
        {"chat_id": chat_id, "user_id": user_id}
    )
    if not user:
        return True
    return False