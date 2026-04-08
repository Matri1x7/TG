from telethon import TelegramClient, events, functions
from telethon.tl.functions.account import UpdateStatusRequest
import asyncio

# ==================== MA'LUMOTLAR ====================
API_ID = 31690105                   # O'zingizning API_ID
API_HASH = "a695194214f1e6dc55688bb9f0f43d18"        # O'zingizning API_HASH

client = TelegramClient('MatrixUserBot2', API_ID, API_HASH)

# ====================== HELP ======================
@client.on(events.NewMessage(pattern=r'\.help', outgoing=True))
async def help_command(event):
    help_text = """
**🔥 Matrix User Bot Buyruqlari**

**.start** - Bot holatini tekshirish
**.help** - Barcha buyruqlar ro'yxati
**.name** - Ismni o'zgartirish
**.bio** - Bio o'zgartirish
**.username** - Username o'zgartirish
**.send** - Boshqa odamga xabar yuborish
**.online** - Online holatini yoqish/o'chirish
**.lastseen** - Oxirgi faollikni o'zgartirish
**.forward** - Xabarni forward qilish

**Misollar:**
`.name Elon Musk`
`.bio Salom, men Matrixman`
`.send @username Salom qandaysan?`
`.online on` yoki `.online off`
    """
    await event.edit(help_text)

# ====================== BOSHQA BUYRUQLAR ======================
@client.on(events.NewMessage(pattern=r'\.start', outgoing=True))
async def start(event):
    await event.edit("✅ **Matrix User Bot Ishga Tushdi!**\nYordam uchun `.help` yozing.")

@client.on(events.NewMessage(pattern=r'\.name', outgoing=True))
async def change_name(event):
    try:
        new_name = event.text.split(maxsplit=1)[1]
        await client(functions.account.UpdateProfileRequest(first_name=new_name))
        await event.edit(f"✅ Ism o'zgartirildi:\n**{new_name}**")
    except:
        await event.edit("❌ Format: `.name Yangi Ism`")

@client.on(events.NewMessage(pattern=r'\.bio', outgoing=True))
async def change_bio(event):
    try:
        new_bio = event.text.split(maxsplit=1)[1]
        await client(functions.account.UpdateProfileRequest(about=new_bio))
        await event.edit(f"✅ Bio o'zgartirildi:\n{new_bio}")
    except:
        await event.edit("❌ Format: `.bio Yangi bio`")

@client.on(events.NewMessage(pattern=r'\.username', outgoing=True))
async def change_username(event):
    try:
        new_username = event.text.split(maxsplit=1)[1]
        await client(functions.account.UpdateUsernameRequest(username=new_username))
        await event.edit(f"✅ Username o'zgartirildi: @{new_username}")
    except:
        await event.edit("❌ Format: `.username yangiusername`")

@client.on(events.NewMessage(pattern=r'\.send', outgoing=True))
async def send_to(event):
    try:
        parts = event.text.split(maxsplit=2)
        target = parts[1]
        text = parts[2]
        await client.send_message(target, text)
        await event.edit(f"✅ Xabar yuborildi → {target}")
    except:
        await event.edit("❌ Format: `.send @username Matn`")

@client.on(events.NewMessage(pattern=r'\.online', outgoing=True))
async def online_status(event):
    try:
        status = event.text.split()[1].lower()
        if status == "on":
            await client(UpdateStatusRequest(offline=False))
            await event.edit("✅ **Online** holati yoqildi")
        elif status == "off":
            await client(UpdateStatusRequest(offline=True))
            await event.edit("✅ **Offline** holati yoqildi")
        else:
            await event.edit("❌ `.online on` yoki `.online off`")
    except:
        await event.edit("❌ Format: `.online on` yoki `.online off`")

@client.on(events.NewMessage(pattern=r'\.lastseen', outgoing=True))
async def lastseen(event):
    try:
        await client(UpdateStatusRequest(offline=False))
        await event.edit("✅ Oxirgi faollik ko'rinadigan qilib qo'yildi")
    except:
        await event.edit("❌ Xatolik yuz berdi")

@client.on(events.NewMessage(pattern=r'\.forward', outgoing=True))
async def forward_message(event):
    try:
        replied = await event.get_reply_message()
        if replied:
            await replied.forward_to(event.chat_id)
            await event.edit("✅ Xabar forward qilindi")
        else:
            await event.edit("❌ Javob berilgan xabarni forward qilish uchun `.forward` yozing")
    except:
        await event.edit("❌ Xatolik! Javob berilgan xabarga `.forward` yozing")

# Oddiy xabar
@client.on(events.NewMessage(outgoing=True))
async def default(event):
    if event.text and not event.text.startswith('.'):
        await event.reply("✅ User Bot ishlayapti!\nYordam: `.help`")

print("🚀 Matrix User Bot ishlamoqda...")
client.start()
client.run_until_disconnected()
