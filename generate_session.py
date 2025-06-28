#!/usr/bin/env python3
import asyncio
from pyrogram import Client

print("Pyrogram String Session Generator")
print("=" * 50)

API_ID = input("Enter your API_ID: ")
API_HASH = input("Enter your API_HASH: ")

async def main():
    async with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as app:
        print("\nYour String Session:")
        print("=" * 50)
        print(await app.export_session_string())
        print("=" * 50)
        print("\nSave this string session safely!")

if __name__ == "__main__":
    asyncio.run(main())