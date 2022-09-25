import wget
import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
import lyricsgenius
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery 
from yt_dlp import YoutubeDL

ydl_opts = {
    'format': 'best',
    'keepvideo': True,
    'prefer_ffmpeg': False,
    'geo_bypass': True,
    'outtmpl': '%(title)s.%(ext)s',
    'quite': True
}



#config#

bot = Client(
    'moonBot', 
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(
    filters.command(["start", "raven"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgIAAxkBAAFQmQABYvQfJR6i6yqB3kYZGUvCDrI8c2QAAn4FAALSWogBauDUxjcpjiApBA")
    await message.reply_text(
        f"""**Salam {message.from_user.mention} 🎵\nMən Poseidon!\n
● **Sənin üçün YouTube və digər platformalardan musiqi yükləmək üçün yaradılmışam.**

● **İşlətmə qaydasını görmək üçün əmrlər butonuna tıkla.**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " ᴘʟᴀʏʟɪ̇sᴛ ✨", 
                        url=f"https://t.me/{Config.PLAYLIST_NAME}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔧 əᴍʀʟəʀ" , callback_data= "cbbilgi"
                    ),
                    InlineKeyboardButton(
                        "ʙʟᴏɢ 🌴",
                        url=f"https://t.me/Nixhaad"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧑🏻‍💻 ᴏᴡɴᴇʀ",
                        url=f"https://t.me/{Config.BOT_OWNER}"
                    )
                    
                ]
                
           ]
        ), 
    ) 
    



@bot.on_callback_query(filters.regex("cbbilgi"))
async def cbbilgi(_, query: CallbackQuery):
    await query.edit_message_text(f"""<b>Salam {query.from_user.mention}!\nBu botun əmrlər menyusu..🔧\n\n ● /song - Musiqi adı vəya YouTube linki (musiqi yükləmə)\n\n● /lyrics - Musiqi adı (mahnı sözləri)\n\n● /video - Video adı vəya YouTube linki (video yükləmə)\n\n</b>""",
    reply_markup=InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton(
                         "Ana Səhifə", callback_data="cbstart")
                 ] 
             ]
         )
         )

# ~~~~~~~~~~~~~~~~~~~~~~ Poseidon song ~~~~~~~~~~~~~~~~~~~~~~


@bot.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(f"""**Salam {query.from_user.mention} 🎵\nMən Medusa !\n\n● **YouTube üzərindən musiqi yükləmə botu.**\n\n● **İstifadə qaydası üçün Əmrlər menyusunu açın.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " ᴘʟᴀʏʟɪ̇sᴛ ✨", 
                        url=f"https://t.me/{Config.PLAYLIST_NAME}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔧 Əmrlər" , callback_data= "cbbilgi"
                    ),
                    InlineKeyboardButton(
                        "ʙʟᴏɢ 🌴",
                        url=f"https://t.me/Nixhaad"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🧑🏻‍💻 ᴏᴡɴᴇʀ",
                        url=f"https://t.me/{Config.BOT_OWNER}"
                    )
                    
                ]
                
           ]
        ), 
    ) 

#alive mesajı#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('Aktivəm Sahibim..⚡️')



  
#music indirme#

@bot.on_message(filters.command("song") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>Sorğunuz axtarılır ... 🔍</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>❌ Xəta! Musiqini tapa bilmədim.\n\n Zəhmət olmasa daha dəqiq məlumat verin.</b>")
        print(str(e))
        return
    m.edit("<b>📥 Yüklənir...</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**╭───────────────**\n**├▷ ♬ Başlıq: [{title[:35]}]({link})**\n**├───────────────**\n**├▷ Playlist 🌴 @{Config.PLAYLIST_NAME}**\n**╰───────────────**"
        res = f"**╭───────────────**\n**├▷ ♬ Başlıq: [{title[:35]}]({link})**\n**├───────────────**\n**├▷👤 İstəyən** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n**├───────────────**\n**├▷⚡️ Bot: @{Config.BOT_USERNAME}**\n**╰───────────────**"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("📤 Göndərilir..")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="ᴘᴏsᴇɪ̇ᴅᴏɴ")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=res, performer="ᴍᴇᴅᴜsᴀ", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>❌ Xəta düzələnə qədər gözləyin..</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

# şarkı sözü 

@bot.on_message(filters.command("lyrics") & ~filters.edited)
async def get_lyric_genius(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**işlədilişi:**\n\n/lyrics (Mahnı adı)")
    m = await message.reply_text("🔍 Mahnı sözləri axtarılır ...")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("❌ `404` Mahnı sözləri tapılmadı..")
    xxx = f"""
**sᴀʀᴋɪ:** {query}
**sᴀɴᴀᴛᴄɪ:** {S.artist}
**sᴀʀᴋɪ sᴏᴢᴜ:**
{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`Lyrics Text`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)


# video indirme 

@bot.on_message(
    filters.command(["video", "vsong"]) & ~filters.edited
)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("📥 **video yüklənir...**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **Xəta:** {e}")
    preview = wget.download(thumbnail)
    await msg.edit("📤 **video göndərilir...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)

bot.run()

