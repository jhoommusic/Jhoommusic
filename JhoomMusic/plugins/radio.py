import aiohttp
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from JhoomMusic import app
from JhoomMusic.core.call import Jhoom
from JhoomMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS

# Popular radio stations
RADIO_STATIONS = {
    "bollywood": {
        "name": "🎵 Bollywood Hits",
        "url": "http://hls-01-regions.emgsound.ru/11_bollywood/playlist.m3u8",
        "description": "Latest Bollywood music hits"
    },
    "english": {
        "name": "🎤 English Pop",
        "url": "http://streaming.radio.co/s2c3cc784b/listen",
        "description": "Top English pop songs"
    },
    "classical": {
        "name": "🎼 Classical Music",
        "url": "http://stream.radiotime.com/classical",
        "description": "Beautiful classical compositions"
    },
    "jazz": {
        "name": "🎷 Jazz Radio",
        "url": "http://streaming.radio.co/s8dc929bd0/listen",
        "description": "Smooth jazz music"
    },
    "rock": {
        "name": "🎸 Rock Station",
        "url": "http://streaming.radio.co/s4b5c2d8f1/listen",
        "description": "Classic and modern rock"
    },
    "lofi": {
        "name": "🌙 Lo-Fi Hip Hop",
        "url": "http://streaming.radio.co/s2a8b7c9d3/listen",
        "description": "Chill lo-fi beats"
    },
    "indian": {
        "name": "🇮🇳 Indian Classical",
        "url": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio056/playlist.m3u8",
        "description": "Traditional Indian music"
    },
    "punjabi": {
        "name": "🎵 Punjabi Hits",
        "url": "http://streaming.radio.co/s7f2a1b8c4/listen",
        "description": "Latest Punjabi songs"
    }
}

@app.on_message(filters.command(["radio", "fm"]) & filters.group & ~BANNED_USERS)
async def radio_command(client, message: Message):
    """Play radio stations"""
    
    if len(message.command) == 1:
        # Show available stations
        radio_text = "📻 **Available Radio Stations:**\n\n"
        
        buttons = []
        for key, station in RADIO_STATIONS.items():
            radio_text += f"• **{station['name']}**\n  {station['description']}\n\n"
            buttons.append([
                InlineKeyboardButton(
                    station['name'], 
                    callback_data=f"radio_play_{key}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton("🔍 Search Online", callback_data="radio_search")
        ])
        
        await message.reply_text(
            radio_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    
    # Play specific station
    station_name = message.command[1].lower()
    
    if station_name in RADIO_STATIONS:
        await play_radio_station(message, station_name)
    else:
        # Search for station
        await search_radio_station(message, " ".join(message.command[1:]))

async def play_radio_station(message: Message, station_key: str):
    """Play a radio station"""
    chat_id = message.chat.id
    station = RADIO_STATIONS[station_key]
    
    mystic = await message.reply_text(f"📻 **Connecting to {station['name']}...**")
    
    try:
        # Join voice chat and start streaming
        success = await Jhoom.join_call(
            chat_id,
            chat_id,
            station["url"],
            video=False
        )
        
        if success:
            await mystic.edit_text(
                f"📻 **Now Playing Radio**\n\n"
                f"**Station:** {station['name']}\n"
                f"**Description:** {station['description']}\n"
                f"**Type:** Live Stream",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                        InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}")
                    ],
                    [
                        InlineKeyboardButton("📻 Other Stations", callback_data="radio_list")
                    ]
                ])
            )
        else:
            await mystic.edit_text(
                "❌ **Failed to connect to radio station!**\n\n"
                "Please check if voice chat is active."
            )
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Radio Error:** {str(e)}")

async def search_radio_station(message: Message, query: str):
    """Search for radio stations online"""
    mystic = await message.reply_text(f"🔍 **Searching for radio stations: {query}**")
    
    try:
        # Search using radio-browser API
        async with aiohttp.ClientSession() as session:
            search_url = f"http://all.api.radio-browser.info/json/stations/byname/{query}"
            
            async with session.get(search_url) as response:
                if response.status == 200:
                    stations = await response.json()
                    
                    if not stations:
                        return await mystic.edit_text(
                            f"❌ **No radio stations found for:** {query}"
                        )
                    
                    # Show top 5 results
                    results_text = f"🔍 **Search Results for:** {query}\n\n"
                    buttons = []
                    
                    for i, station in enumerate(stations[:5]):
                        name = station.get('name', 'Unknown')
                        country = station.get('country', 'Unknown')
                        url = station.get('url_resolved', station.get('url', ''))
                        
                        if url:
                            results_text += f"{i+1}. **{name}** ({country})\n"
                            buttons.append([
                                InlineKeyboardButton(
                                    f"{i+1}. {name[:30]}...",
                                    callback_data=f"radio_custom_{i}"
                                )
                            ])
                    
                    # Store search results temporarily
                    if not hasattr(app, 'radio_search_results'):
                        app.radio_search_results = {}
                    app.radio_search_results[message.chat.id] = stations[:5]
                    
                    await mystic.edit_text(
                        results_text,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                else:
                    await mystic.edit_text("❌ **Failed to search radio stations**")
    
    except Exception as e:
        await mystic.edit_text(f"❌ **Search Error:** {str(e)}")

@app.on_callback_query(filters.regex(r"radio_play_(.+)"))
async def radio_play_callback(client, callback_query: CallbackQuery):
    """Handle radio station play callback"""
    station_key = callback_query.data.split("_")[2]
    
    if station_key in RADIO_STATIONS:
        # Create a fake message object for play_radio_station
        fake_message = type('obj', (object,), {
            'chat': callback_query.message.chat,
            'reply_text': callback_query.message.edit_text
        })
        
        await play_radio_station(fake_message, station_key)
    else:
        await callback_query.answer("❌ Station not found!", show_alert=True)

@app.on_callback_query(filters.regex(r"radio_custom_(\d+)"))
async def radio_custom_callback(client, callback_query: CallbackQuery):
    """Handle custom radio station play"""
    index = int(callback_query.data.split("_")[2])
    chat_id = callback_query.message.chat.id
    
    if (hasattr(app, 'radio_search_results') and 
        chat_id in app.radio_search_results and
        index < len(app.radio_search_results[chat_id])):
        
        station = app.radio_search_results[chat_id][index]
        station_url = station.get('url_resolved', station.get('url', ''))
        station_name = station.get('name', 'Unknown Station')
        
        if station_url:
            mystic = await callback_query.message.edit_text(
                f"📻 **Connecting to {station_name}...**"
            )
            
            try:
                success = await Jhoom.join_call(
                    chat_id,
                    chat_id,
                    station_url,
                    video=False
                )
                
                if success:
                    await mystic.edit_text(
                        f"📻 **Now Playing Radio**\n\n"
                        f"**Station:** {station_name}\n"
                        f"**Country:** {station.get('country', 'Unknown')}\n"
                        f"**Type:** Live Stream",
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                                InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}")
                            ]
                        ])
                    )
                else:
                    await mystic.edit_text("❌ **Failed to connect to radio station!**")
            
            except Exception as e:
                await mystic.edit_text(f"❌ **Radio Error:** {str(e)}")
        else:
            await callback_query.answer("❌ Invalid station URL!", show_alert=True)
    else:
        await callback_query.answer("❌ Station not found!", show_alert=True)

@app.on_callback_query(filters.regex("radio_list"))
async def radio_list_callback(client, callback_query: CallbackQuery):
    """Show radio stations list"""
    radio_text = "📻 **Available Radio Stations:**\n\n"
    
    buttons = []
    for key, station in RADIO_STATIONS.items():
        radio_text += f"• **{station['name']}**\n  {station['description']}\n\n"
        buttons.append([
            InlineKeyboardButton(
                station['name'], 
                callback_data=f"radio_play_{key}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton("🔍 Search Online", callback_data="radio_search")
    ])
    
    await callback_query.message.edit_text(
        radio_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex("radio_search"))
async def radio_search_callback(client, callback_query: CallbackQuery):
    """Handle radio search callback"""
    await callback_query.message.edit_text(
        "🔍 **Radio Search**\n\n"
        "Use `/radio <station name>` to search for radio stations.\n\n"
        "**Examples:**\n"
        "• `/radio bbc`\n"
        "• `/radio jazz`\n"
        "• `/radio hindi`"
    )