from pyrogram import Client
from pyrogram.session import StringSession

api_id = 25115099
api_hash = "ee0b6a29d4918aa6dabeb181d2c15a36"

with Client(session_name=StringSession(), api_id=api_id, api_hash=api_hash) as app:
    print("\n✅ Your STRING_SESSION:\n")
    print(app.export_session_string())
