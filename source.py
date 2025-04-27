# المكتبات الأساسية
import os
import asyncio
import time
import re
import logging
import subprocess
import webbrowser
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from urllib.parse import urlparse
from io import BytesIO
import random

# مكتبات معالجة الميديا
from PIL import Image, ImageDraw, ImageFont
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from telegraph import Telegraph
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL

# مكتبات التليثون
from telethon import (
    TelegramClient, 
    events, 
    functions, 
    types, 
    Button
)
from telethon.sessions import StringSession
from telethon.errors import (
    SessionPasswordNeededError,
    ChannelPrivateError
)
from telethon.tl.functions import (
    account,
    photos,
    messages,
    contacts,
    channels
)
from telethon.tl.types import (
    MessageMediaPhoto,
    InputPeerSelf,
    InputMediaPhoto,
    InputMediaDocument,
    User,
    Channel,
    ChannelParticipantAdmin,
    ChannelParticipantCreator
)
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    LeaveChannelRequest,
    GetFullChannelRequest
)
from telethon.tl.functions.messages import (
    SendMessageRequest,
    SendMediaRequest,
    DeleteChatUserRequest
)
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import GetUserPhotosRequest

# مكتبات الترجمة والمناطق الزمنية
from deep_translator import GoogleTranslator
import pytz

#لتشغيل على خادم
import http.server
import socketserver
import threading

from telethon import events
import urllib.parse

from telethon import events, types
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantRequest

from telethon.tl.functions.stories import GetPinnedStoriesRequest, GetStoriesArchiveRequest
from telethon.tl.types import InputPeerUser
from datetime import datetime
from telethon import types, events

# ===== الثوابت والإعدادات ===== #

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
STRING_SESSION = os.getenv('STRING_SESSION')


MAX_WARNINGS = 7

# ===== حالات النظام ===== #
protection_enabled = False

# مفتاح CoinMarketCap
CMC_API_KEY = os.getenv('CMC_API_KEY')  

# ===== قوائم التتبع ===== #
repeat_tasks = {}      # تتبع مهام التكرار
accepted_users = {}    # المستخدمون المقبولون
warned_users = {}      # المستخدمون المحذرون
muted_users = set()    # المستخدمون المكتومون
imitated_users = set() # قائمة المستخدمين الذين يتم تقليدهم

# ===== تهيئة العميل ===== #
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def start_client():
    """تهيئة وتوصيل العميل"""
    try:
        await client.connect()
        
        if not await client.is_user_authorized():
            print("⚠️ الجلسة غير صالحة، يلزم إنشاء جلسة جديدة")
            exit(1)
            
        print("✅ تم تسجيل الدخول باستخدام كود التيرمكس بنجاح!")
        return client
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التسجيل: {e}")
        exit(1)
        
@client.on(events.NewMessage(pattern=r'\.اوامري'))
async def show_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهلاً بك فـي قـائمة الأوامـر الـخاصة بسـورس إيــريــن** ⎚
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.م1` - **أوامر الحساب** ☆
2- ☆ `.م2` - **أوامر الاسم الوقتي** ☆
3- ☆ `.م3` - **أوامر البحث والتحميل** ☆
4- ☆ `.م4` - **أوامر الألعاب والتسلية** ☆
5- ☆ `.م5` - **أوامر الذكاء الاصطناعي** ☆
6- ☆ `.م6` - **أوامر الذاتية** ☆
7- ☆ `.م7` - **أوامر التكرار** ☆
8- ☆ `.م8` - **أوامر الميديا والصيغ** ☆
9- ☆ `.م9` - **أوامر الحماية والتحكم** ☆
10- ☆ `.م10` - **أوامر القنوات والمجموعات** ☆
11- ☆ `.م11` - **أوامر التخزين والترجمة** ☆
12- ☆ `.م12` - **أوامر إضافية** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)
    
@client.on(events.NewMessage(pattern=r'\.م1$'))
async def show_commands_list(event):
    commands_message = """
╭━━━┳━━━━╮
**أهـلاً بك فـي قـائمة الحساب الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.ايدي` - **عرض معلومات المستخدم** ☆
2- ☆ `.تليغراف` - **رفع الصور إلى تيليجراف** ☆
3- ☆ `.كتم` - **كتم المستخدم** ☆
4- ☆ `.الغاء كتم` - **إلغاء كتم المستخدم** ☆
5- ☆ `.المكتومين` - **عرض قائمة المكتومين** ☆
6- ☆ `.بلوك` - **حظر المستخدم** ☆
7- ☆ `.لصوره` - **تحويل ملصق إلى صورة** ☆
8- ☆ `.فحص` - **فحص البوت** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م2$'))
async def show_timed_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الوقتي الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.الاسم التلقائي` - **تفعيل التوقيت التلقائي للاسم** ☆
2- ☆ `.ايقاف الاسم التلقائي` - **إيقاف التوقيت التلقائي للاسم** ☆
3- ☆ `.وقتيه1` - **زخرفة الأرقام بالنمط 𝟘𝟙𝟚𝟛** ☆
4- ☆ `.وقتيه2` - **زخرفة الأرقام بالنمط ⓪➀➁➂** ☆
5- ☆ `.وقتيه3` - **زخرفة الأرقام بالنمط ⓿➊➋➌** ☆
6- ☆ `.التوقيت` - **عرض قائمة التوقيتات المتاحة** ☆
7- ☆ `.وقت مصر` - **تفعيل توقيت مصر** ☆
8- ☆ `.وقت سوريا` - **تفعيل توقيت سوريا** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م3$'))
async def show_search_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة البحث والتحميل الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.بحث` + كلمة - **البحث عن فيديو على يوتيوب** ☆
2- ☆ `.تيك` + رابط - **تحميل فيديو من تيك توك** ☆
3- ☆ `.انستا` + رابط - **تحميل من إنستجرام** ☆
4- ☆ `.يوت` + رابط - **تحميل من يوتيوب** ☆
5- ☆ `.بنترست` + رابط - **تحميل من بنترست** ☆
6- ☆ `.عربي` - **ترجمة النص للإنجليزية (بالرد)** ☆
7- ☆ `.انجلش` - **ترجمة النص للعربية (بالرد)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م4$'))
async def show_games_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الألعاب والتسلية الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.تسلية` - **عرض أوامر التسلية** ☆
2- ☆ `.مسدس` - **رسم مسدس** ☆
3- ☆ `.كلب` - **رسم كلب** ☆
4- ☆ `.سبونج بوب` - **رسم شخصية سبونج بوب** ☆
5- ☆ `.إبرة` - **رسم إبرة** ☆
6- ☆ `.وحش` - **رسم وحش** ☆
7- ☆ `.مروحية` - **رسم مروحية** ☆
8- ☆ `.كت` - **سؤال عشوائي للتسلية** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م5$'))
async def show_ai_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الذكاء الاصطناعي الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.س` + سؤال - **سؤال الذكاء الاصطناعي** ☆
2- ☆ `.تهكير` - **محاكاة عملية تهكير (فكاهي)** ☆
3- ☆ `.قتل` + اسم - **لعبة قتل (فكاهي)** ☆
4- ☆ `.قاتل` + اسم - **لعبة قتل متقدمة (فكاهي)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م6$'))
async def show_self_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الأوامـر الذاتية بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.ذاتيه` - **حفظ ذاتية (بالرد على صورة/فيديو)** ☆
2- ☆ `.الذاتيه تشغيل` - **تفعيل الحفظ التلقائي للذاتية** ☆
3- ☆ `.الذاتيه ايقاف` - **إيقاف الحفظ التلقائي للذاتية** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م7$'))
async def show_repeat_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة التكرار الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.تكرار` + عدد + نص - **تكرار النص** ☆
2- ☆ `.تكرار ملصق` + عدد - **تكرار ملصق (بالرد)** ☆
3- ☆ `.وقف التكرار` - **إيقاف جميع عمليات التكرار** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م8$'))
async def show_media_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الميديا والصيغ الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.حول بصمه` - **تحويل فيديو إلى بصمة صوتية (بالرد)** ☆
2- ☆ `.حول صوت` - **تحويل فيديو إلى ملف صوتي (بالرد)** ☆
3- ☆ `.لمتحركه` - **تحويل صورة/ملصق إلى متحركة (بالرد)** ☆
4- ☆ `.لمتحرك` - **تحويل فيديو إلى متحركة (بالرد)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)
    
@client.on(events.NewMessage(pattern=r'\.م9$'))
async def show_protection_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الحمايـة والتحكـم بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.الحمايه تفعيل` - **تفعيل الحماية التلقائية** ☆
2- ☆ `.الحمايه تعطيل` - **تعطيل الحماية التلقائية** ☆
3- ☆ `.قبول` - **قبول مستخدم (بالرد)** ☆
4- ☆ `.رفض` - **رفض مستخدم (بالرد)** ☆
5- ☆ `.المقبولين` - **عرض قائمة المقبولين** ☆
6- ☆ `.انتحال` - **انتحال هوية مستخدم (بالرد)** ☆
7- ☆ `.اعاده` - **استعادة الهوية الأصلية** ☆
8- ☆ `.تقليد` - **تقليد مستخدم (بالرد)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)        

@client.on(events.NewMessage(pattern=r'\.م10$'))
async def show_channels_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة إدارة القنـوات والمجموعات ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.انضم` + رابط - **الانضمام لقناة/مجموعة** ☆
2- ☆ `.غادر` + رابط - **مغادرة قناة/مجموعة** ☆
3- ☆ `.دعمكم` - **تجميع نقاط بوت دعمكم** ☆
4- ☆ `.ايقاف دعمكم` - **إيقاف التجميع** ☆
5- ☆ `.لانهائي دعمكم` - **تجميع لانهائي** ☆
6- ☆ `.نقاط دعمكم` - **عرض النقاط** ☆
7- ☆ `.هدية دعمكم` - **تجميع الهدية** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م11$'))
async def show_channels_commands(event):
    commands_message = """
╭━━━┳━━━━╮
أهــلاً بك فـي قـائمة إدارة القنـوات والمجموعات ⎚
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.تخزين` - **تفعيل تخزين الرسائل** ☆
2- ☆ `.الغاء التخزين` - **إيقاف تخزين الرسائل** ☆
3- ☆ `.عربي` - **ترجمة النص للإنجليزية (بالرد)** ☆
4- ☆ `.انجلش` - **ترجمة النص للعربية (بالرد)** ☆
5- ☆ `.حذف` - **حذف الرسالة (بالرد)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'\.م12$'))
async def show_additional_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الأوامـر الإضافيـة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.مدينة` - **رسم مدينة** ☆
2- ☆ `.حفظ` - **حفظ منشور من قناة/مجموعة (بالرد على الرابط)** ☆
3- ☆ `.قتل` + اسم - **لعبة قتل (فكاهي)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)
    
# تحويل الأرقام إلى الزخارف المختلفة
def to_smart_numbers(number_str, style):
    styles = {
        'normal': '0123456789',
        'style1': '𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡',  # 10 characters
        'style2': '⓪➀➁➂➃➄➅➆➇➈',  # 10 characters
        'style3': '⓿➊➋➌➍➎➏➐➑➒'   # 10 characters
    }

    # تحقق من أن النمط موجود في القاموس
    if style not in styles:
        raise ValueError("Invalid style. Available styles are: normal, style1, style2, style3.")
    
    # تأكد من أن السلسلتين لهما نفس الطول
    normal_style = styles['normal']
    selected_style = styles[style]
    if len(normal_style) != len(selected_style):
        raise ValueError("The normal style and the selected style must have the same length.")
    
    conversion = str.maketrans(normal_style, selected_style)
    return number_str.translate(conversion)

# الحصول على الوقت المحلي
def get_local_time(timezone_str, style='normal'):
    local_tz = pytz.timezone(timezone_str)
    current_time = datetime.now(local_tz).strftime("%I:%M")
    return to_smart_numbers(current_time, style)

timed_update_running = False
current_timezone = 'Africa/Cairo'
current_style = 'normal'

# تحديث الاسم بناءً على الوقت والزخرفة المختارة
async def update_name(timezone_str, style='normal'):
    me = await client.get_me()
    current_time = get_local_time(timezone_str, style)
    new_name = current_time
    await client(UpdateProfileRequest(first_name=new_name))

# الأمر لتفعيل الاسم التلقائي
@client.on(events.NewMessage(pattern=r'\.الاسم التلقائي'))
async def start_timed_update(event):
    global timed_update_running
    global current_style

    if not timed_update_running:
        timed_update_running = True
        await event.edit("**• جـارِ تفعيـل الاسـم الوقتـي ⅏. . .**")
        await asyncio.sleep(2)
        await event.edit("**⎉╎تـم بـدء الاسـم الوقتـي🝛 .. بنجـاح ✓**")
        await asyncio.sleep(5)
        await event.delete()

        while timed_update_running:
            await update_name(current_timezone, current_style)
            await asyncio.sleep(60)  # التحديث كل دقيقة
    else:
        await event.edit("**⚠️ التحديث التلقائي للاسم يعمل بالفعل.**")

# أوامر لتفعيل الزخرفة المختلفة
async def activate_style(event, style, style_name):
    global current_style
    global timed_update_running

    if current_style == style:
        await event.edit(f"**⚠️ الزخرفة {style_name} مفعلة بالفعل.**")
    else:
        current_style = style
        await event.edit("**✾╎جـاري اضـافة زخـرفـة الوقتيـه لـ بوتـك 💞🦾 . . .**")
        await asyncio.sleep(2)
        if timed_update_running:
            await event.edit(f"**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓** \n **✾╎نـوع الزخـرفـه: ** {style_name}")
        else:
            await event.edit(f"**✾╎تم تغييـر زغـرفة الاسـم الوقتـي .. بنجـاح✓** \n **✾╎نـوع الزخـرفـه:** {style_name}\n✾╎الان ارسـل ↶ `.الاسم التلقائي`")
           
@client.on(events.NewMessage(pattern=r'\.وقتيه1'))
async def activate_style1(event):
    await activate_style(event, 'style1', '𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡')

@client.on(events.NewMessage(pattern=r'\.وقتيه2'))
async def activate_style2(event):
    await activate_style(event, 'style2', '⓪➀➁➂➃➄➅➆➇➈')

@client.on(events.NewMessage(pattern=r'\.وقتيه3'))
async def activate_style3(event):
    await activate_style(event, 'style3', '⓿➊➋➌➍➎➏➐➑➒')

# الأمر لإيقاف الاسم التلقائي
@client.on(events.NewMessage(pattern=r'\.ايقاف الاسم التلقائي'))
async def stop_timed_update(event):
    global timed_update_running
    if timed_update_running:
        timed_update_running = False
        await event.edit("⛔ تم إيقاف الاسم التلقائي بنجاح.")
    else:
        await event.edit("**⚠️ لا يوجد تحديث تلقائي للاسم مفعّل.**")
  	    

@client.on(events.NewMessage(pattern=r'\.ايدي'))
async def show_user_info(event):
    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        if reply_message.sender_id:
            user = await client.get_entity(reply_message.sender_id)

            await event.edit("جاري عرض المعلومات...")

            user_photo_path = 'user_photo.jpg'
            await client.download_profile_photo(user.id, file=user_photo_path)

            bio = getattr(user, 'about', "لا يوجد")
            user_id = user.id
            username = user.username if user.username else "غير متوفر"
            user_name = user.first_name or "غير متوفر"

            try:
                photos = await client(GetUserPhotosRequest(user.id, offset=0, max_id=0, limit=1))
                num_photos = len(photos.photos)
            except Exception as e:
                num_photos = "لا يمكن الحصول على عدد الصور"

            messages_count = 0
            interaction = "نار وشرر" if messages_count > 100 else "ضعيف"
            groups_count = "لا يوجد"
            creation_date = "تاريخ عشوائي"

            user_info_message = (
                f"⎚• مـعلومـات المسـتخـدم مـن بـوت إيــريــن\n"
                f"ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆\n"
                f"✦ الاســم    ⤎ `{user_name}`\n"
                f"✦ اليـوزر    ⤎ @{username}\n"
                f"✦ الايـدي    ⤎ `{user_id}`\n"
                f"✦ الرتب     ⤎ مميز\n"
                f"✦ الرسائل  ⤎ {messages_count}\n"
                f"✦ التفاعل  ⤎ {interaction}\n"
                f"✦ الـمجموعات المشتـركة ⤎ {groups_count}\n"
                f"✦ الإنشـاء  ⤎ {creation_date}\n"
                f"✦ البايـو   ⤎ {bio}\n"
                f"ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆"
            )

            await client.send_file(event.chat_id, user_photo_path, caption=user_info_message)
            await event.delete()
            os.remove(user_photo_path)
        else:
            await event.edit("⚠️ لم أتمكن من العثور على معلومات عن هذا المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم للحصول على معلوماته.")

async def upload_to_telegraph(image_path):
    try:
        response = telegraph.upload_file(image_path)
        return 'https://telegra.ph' + response[0]
    except Exception as e:
        print(f"خطأ أثناء رفع الصورة: {e}")
        return None
# إضافة أمر .بل
@client.on(events.NewMessage(pattern=r'\.بلوك'))
async def block_user(event):
    if event.is_reply:
        # الحصول على معلومات الرسالة التي تم الرد عليها
        replied_message = await event.get_reply_message()
        user_id = replied_message.sender_id
        
        # التحقق من أن المستخدم موجود
        if user_id:
            try:
                # حظر المستخدم
                await client(BlockRequest(user_id))
                
                # إرسال رسالة في نفس الرسالة بعد حظر المستخدم
                block_message = (
                    f"− الحيـوان : {replied_message.sender.first_name} 🫏\n"
                    "− تم حظـره .. بنجـاح ☑️\n"
                    "− لايمكنـه ازعـاجـك الان 🚷"
                )
                await event.edit(block_message)
            except Exception as e:
                await event.edit(f"⚠️ حدث خطأ أثناء محاولة حظر المستخدم: {str(e)}")
        else:
            await event.edit("⚠️ لم يتم العثور على المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد حظره.")
        

@client.on(events.NewMessage(pattern=r'\.حذف'))
async def delete_message(event):
    if event.reply_to_msg_id:
        await client.delete_messages(event.chat_id, message_ids=[event.reply_to_msg_id])
        await event.delete()
    else:
        await event.edit("⚠️ يرجى الرد على الرسالة التي تريد حذفها.")

@client.on(events.NewMessage(pattern=r'\.التوقيت'))
async def show_timezones(event):
    timezone_message = (
        "**🌍 قائمة التوقيتات:**\n\n"
        "1. `.وقت مصر` 🇪🇬 - تفعيل التوقيت الخاص بمصر.\n"
        "2. `.وقت سوريا` 🇸🇾 - تفعيل التوقيت الخاص بسوريا.\n"
        "3. `.وقت العراق` 🇮🇶 - تفعيل التوقيت الخاص بالعراق.\n"
        "4. `.وقت اليمن` 🇾🇪 - تفعيل التوقيت الخاص باليمن.\n"
    )
    
    await event.edit(timezone_message)

@client.on(events.NewMessage(pattern=r'\.وقت مصر'))
async def set_time_egypt(event):
    global current_timezone
    current_timezone = 'Africa/Cairo'
    await event.edit("تم تفعيل وقت مصر بنجاح ✅")

@client.on(events.NewMessage(pattern=r'\.وقت سوريا'))
async def set_time_syria(event):
    global current_timezone
    current_timezone = 'Asia/Damascus'
    await event.edit("تم تفعيل وقت سوريا بنجاح ✅")

@client.on(events.NewMessage(pattern=r'\.وقت العراق'))
async def set_time_iraq(event):
    global current_timezone
    current_timezone = 'Asia/Baghdad'
    await event.edit("تم تفعيل وقت العراق بنجاح ✅")

@client.on(events.NewMessage(pattern=r'\.وقت اليمن'))
async def set_time_yemen(event):
    global current_timezone
    current_timezone = 'Asia/Aden'
    await event.edit("تم تفعيل وقت اليمن بنجاح ✅")
    
@client.on(events.NewMessage(pattern=r'\.تسلية'))
async def show_entertainment_commands(event):
    entertainment_commands = (
      "╭━━━┳━━━━╮\n"
        "**أهلاً بك فـي قـائمة التسلية الـخاصة بسـورس إيــريــن ⎚**\n"
        "╰━━━┻━━━━╯\n"
        "ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆\n"
        "1- ☆ .مسدس - **رسم مسدس** ☆\n"
        "2- ☆ .كلب - **رسم كلب** ☆\n"
        "3- ☆ .سبونج بوب - **رسم شخصية سبونج بوب** ☆\n"
        "4- ☆ .إبرة - **رسم إبرة **☆\n"
        "5- ☆ .وحش - **رسم وحش** ☆\n"
        "6- ☆ .مروحية -** رسم مروحية** ☆\n"
        "7- ☆ .تهكير - **لتنفيذ عملية تهكير **☆\n"
        "8- ☆ .قتل - **لتنفيذ عملية قتل** ☆\n"
 "9- ☆ `.قاتل` - **+ اسم الشخص - لتنفيذ عملية قتل** ☆ \n"
"10- ☆ `.انتحال` - **بالرد على الشخص** ☆\n"
"11- ☆ `.تقليد` - **بالرد على الشخص** ☆  \n"
          "ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆"
    )
    
    await event.edit(entertainment_commands) 
   
@client.on(events.NewMessage(pattern=r'\.مسدس'))
async def draw_gun(event):
    gun_art = (
        "░▐█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄\n"
        "░███████████████████████\n"
        "░▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓◤\n"
        "░▀░▐▓▓▓▓▓▓▌▀█░░░█▀░\n"
        "░░░▓▓▓▓▓▓█▄▄▄▄▄█▀░░\n"
        "░░█▓▓▓▓▓▌░░░░░░░░░░\n"
        "░▐█▓▓▓▓▓░░░░░░░░░░░\n"
        "░▐██████▌░░░░░░░░░░"
    )
    await event.edit(gun_art)

@client.on(events.NewMessage(pattern=r'\.كلب'))
async def draw_dog(event):
    dog_art = (
        "╥━━━━━━━━╭━━╮━━┳\n"
        "╢╭╮╭━━━━━┫┃▋▋━▅┣\n"
        "╢┃╰┫┈┈┈┈┈┃┃┈┈╰┫┣\n"
        "╢╰━┫┈┈┈┈┈╰╯╰┳━╯┣\n"
        "╢┊┊┃┏┳┳━━┓┏┳┫┊┊┣\n"
        "╨━━┗┛┗┛━━┗┛┗┛━━┻"
    )
    await event.edit(dog_art)

@client.on(events.NewMessage(pattern=r'\.سبونج بوب'))
async def draw_spongebob(event):
    spongebob_art = (
        "┈┈ ╱▔▔▔▔▔▔▔▔▔▔▔▏\n"
        "┈╱╭▏╮╭┻┻╮╭┻┻╮ ╭▏\n"
        "▕╮╰▏╯┃╭╮┃┃╭╮┃ ╰▏\n"
        "▕╯┈▏┈┗┻┻┛┗┻┻┻╮ ▏\n"
        "▕╭╮▏╮┈┈┈┈┏━━━╯ ▏\n"
        "▕╰╯▏╯╰┳┳┳┳┳┳╯ ╭▏\n"
        "▕┈╭▏╭╮┃┗┛┗┛┃┈ ╰▏\n"
        "▕┈╰▏╰╯╰━━━━╯┈┈ ▏I'm سبـونـج بــوب"
    )
    await event.edit(spongebob_art)

@client.on(events.NewMessage(pattern=r'\.إبرة'))
async def draw_needle(event):
    needle_art = (
        "────▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀█─█\n"
        "▀▀▀▀▄─█─█─█─█─█─█──█▀█\n"
        "─────▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀─▀\n"
        "\n🚹 ╎ تنح واخذ الابره عزيزي 👨🏻‍⚕🤭😂"
    )
    await event.edit(needle_art)

@client.on(events.NewMessage(pattern=r'\.وحش'))
async def draw_monster(event):
    monster_art = (
        "▄███████▄\n"
        "█▄█████▄█\n"
        "█▼▼▼▼▼█\n"
        "██____█▌\n"
        "█▲▲▲▲▲█\n"
        "█████████\n"
        "_████"
    )
    await event.edit(monster_art)
@client.on(events.NewMessage(pattern=r'\.مدينة'))
async def draw_city(event):
    city_art = (
        "☁️☁️☁️🌞      ☁️     ☁️  ☁️ ☁️\n"
        "  ☁️ ☁️  ✈️    ☁️    🚁    ☁️    ☁️            \n"
        "☁️  ☁️    ☁️       ☁️     ☁️   ☁️ ☁️\n"
        "       🏬🏨🏫🏢🏤🏥🏦🏪🏫\n"
        "         🌲|         l🚍  |🌳👭\n"
        "        🌳|  🚘  l 🏃   |🌴 👬                       \n"
        " 👬🌴|          l  🚔    |🌲\n"
        "     🌲|   🚖   l              |                               \n"
        "   🌳|🚶        |   🚍     | 🌴🚴🚴\n"
        "  🌴|               |                |🌲"
    )
    await event.edit(city_art)    

@client.on(events.NewMessage(pattern=r'\.مروحية'))
async def draw_helicopter(event):
    helicopter_message = "بـدء اقـلاع المـروحيـه ...🚁"
    await event.edit(helicopter_message)

    helicopter_art_1 = (
        "    🔲 ▬▬▬.◙.▬▬▬ 🔳\n"
        "        ═▂▄▄▓▄▄▂\n"
        "       ◢◤    █▀▀████▄▄▄▄◢◤\n"
        "       █▄ █ █▄ ███▀▀▀▀▀▀▀╬\n"
        "       ◥█████◤\n"
        "         ══╩══╩══\n"
        "              ╬═╬\n"
        "              ╬═╬\n"
        "              ╬═╬ ☻/\n"
        "              ╬═╬/▌\n"
        "              ╬═╬//"
    )

    helicopter_art_2 = (
        "    🔳 ▬▬▬.◙.▬▬▬ 🔲\n"
        "        ═▂▄▄▓▄▄▂\n"
        "       ◢◤    █▀▀████▄▄▄▄◢◤\n"
        "       █▄ █ █▄ ███▀▀▀▀▀▀▀╬\n"
        "       ◥█████◤\n"
        "         ══╩══╩══\n"
        "              ╬═╬\n"
        "              ╬═╬\n"
        "              ╬═╬ ☻/\n"
        "              ╬═╬/▌\n"
        "              ╬═╬//"
    )

    for _ in range(8):
        await asyncio.sleep(2)
        await event.edit(helicopter_art_1)
        await asyncio.sleep(1)
        await event.edit(helicopter_art_2)

from telethon import events
import asyncio

@client.on(events.NewMessage(pattern=r'\.تهكير'))
async def hacking_simulation(event):
    hacking_steps = [
        "جـارِ تهكيـر المستخدم...",
        "⌔: تم تحديد المستخدم لـ تهكيـره ✅",
        "⌔: جـارِ الاتصال بـ خـوادم إيــريــن المتخصصه بالـتهكيـر",
        "⪼ جـارِ الان ... اختـراق الضـحيـة 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 84%\n█████████████████████▒▒▒▒",
        "⪼ جـارِ ... اختـراق الضـحيـة 100%\n█████████تـم تهكيـره ✅███████████",
        "⪼ تـم اختـراق الحسـاب .. بنجـاح ☑️\n\n⪼ قـم بالـدفع الـى 𓆩EᏒEᑎ𓆪 💲\n⪼ لعـدم نشـر معلـوماتك وصـورك 📑"
    ]
    
    for step in hacking_steps:
        await event.edit(step)
        await asyncio.sleep(2)  # تعديل فترة الانتظار إلى ٢ ثواني

@client.on(events.NewMessage(pattern=r'\.قاتل (.+)'))
async def killer(event):
    # الحصول على الاسم المدخل في الأمر
    name = event.pattern_match.group(1)
    
    # تأكد من أن البوت لن يتفاعل مع الرسائل المعدلة (التحقق باستخدام edit_date)
    if event.message.edit_date is not None:
        return

    # قائمة الرسائل التي سيتم عرضها بالتتابع
    messages = [
        "Ready Commando __𓆩EᏒEᑎ𓆪",
        "Ｆｉｉｉｉｉｒｅ",
        f"Commando 𓆩EᏒEᑎ𓆪   \n\n_/﹋|_\n (҂_´)\n <,︻╦╤─ ҉ - \n _/﹋|_",
        f"Commando 𓆩EᏒEᑎ𓆪   \n\n_/﹋|_\n (҂_´)\n <,︻╦╤─ ҉ - - \n _/﹋|_",
        f"Commando 𓆩EᏒEᑎ𓆪   \n\n_/﹋|_\n (҂_´)\n <,︻╦╤─ ҉ - - - - - - -\n _/﹋|_",
        f"Commando 𓆩EᏒEᑎ𓆪   \n\n_/﹋|_\n (҂_´)\n <,︻╦╤─                    {name} مات \n _/﹋|_"
    ]

    # تنفيذ كل تعديل على الرسالة
    for message in messages:
        await event.edit(message)
        await asyncio.sleep(2)  # الانتظار لمدة ثانية واحدة بين كل تعديل
    
    # التأكد من أن العملية لا تتكرر مرة أخرى
    return

        
    for message in messages:
        await event.edit(message)
        await asyncio.sleep(1)  # انتظر لمدة ثانية واحدة بين كل تعديل

                
    for message in messages:
        await event.edit(message)
        await asyncio.sleep(1)  # انتظر لمدة ثانية واحدة بين كل تعديل        








@client.on(events.NewMessage(pattern=r'\.م3'))
async def show_search_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة البحث الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.بحث` - **مثال (.بحث قرآن كريم)** ☆
2- ☆ `.تيك` -** مثال (.تيك + رابط أو الرد على رابط)** ☆
3-☆ `.انستا` - **مثال (.انستا + رابط أو الرد على رابط)** ☆
4- ☆ `.يوت` - **مثال (.يوت + الرابط أو الرد على رابط)**☆
5- ☆ `.بنترست` - **مثال (.بنترست + الرابط أو الرد على رابط)**☆
**(قريبا سيتم اضافة اوامر بحث جديدة)**
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    
    await event.edit(commands_message)        
                
                                
                        




# أمر كتم المستخدم
@client.on(events.NewMessage(pattern=r'\.كتم'))
async def mute_user(event):
    global muted_users

    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        user_id = reply_message.sender_id
        user = await client.get_entity(user_id)

        if user_id:
            muted_users.add(user_id)  # نستخدم user_id لتخزين المستخدم
            await event.edit(f"تم كتم المستخدم بنجاح ✅")

            # التعامل مع رسائل المستخدم المكتوم
            @client.on(events.NewMessage(from_users=user_id))
            async def handle_muted_users(event):
                if event.sender_id in muted_users:
                    await event.delete()  # حذف الرسالة من عندي وعنده
        else:
            await event.edit("⚠️ لم أتمكن من تحديد المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد كتمه.")

# أمر إلغاء كتم المستخدم
@client.on(events.NewMessage(pattern=r'\.الغاء الكتم'))
async def unmute_user(event):
    global muted_users

    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        user_id = reply_message.sender_id
        user = await client.get_entity(user_id)

        if user_id:
            if user_id in muted_users:
                muted_users.remove(user_id)
                await event.edit(f"تم إلغاء كتم المستخدم بنجاح ✅")
            else:
                await event.edit(f"المستخدم ليس مكتوم ⚠️") 
        else:
            await event.edit("⚠️ لم أتمكن من تحديد المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد إلغاء كتمه.")

# أمر عرض قائمة المكتومين
@client.on(events.NewMessage(pattern=r'\.المكتومين'))
async def list_muted_users(event):
    if not muted_users:
        await event.edit("لا يوجد مستخدمين مكتومين حالياً.")
        return

    # إعداد قائمة المستخدمين المكتومين
    muted_list = []
    for user_id in muted_users:
        user = await client.get_entity(user_id)
        muted_list.append(f"• @{user.username or 'مستخدم بدون يوزر نيم'}")

    # إعداد الرسالة التي ستعرض عدد وأسماء المستخدمين المكتومين
    muted_list_str = "\n".join(muted_list)
    count = len(muted_users)
    response = f"عدد المستخدمين المكتومين: {count}\n{muted_list_str}"
    
    await event.edit(response)

# اسم المستخدم للبوت الذكي
gpt_bot_username = '@Amigoo_Chat_Bot'

@client.on(events.NewMessage(pattern=r'\.س$'))
async def handle_ai_command(event):
    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2:
        await event.reply("⚠️ يرجى إدخال السؤال بعد الأمر .س")
        return

    question = parts[1]

    # إرسال رسالة "⏳ GPT-4o يعمل على طلبك. يرجى الانتظار لحظة . . ."
    processing_message = await event.edit("⏳ GPT-4o يعمل على طلبك. يرجى الانتظار لحظة . . .")

    try:
        # إرسال السؤال إلى بوت الذكاء الاصطناعي
        await client.send_message(gpt_bot_username, question)

        # الانتظار للحصول على الإجابة
        response_received = False
        for _ in range(30):  # عدد المحاولات
            async for message in client.iter_messages(gpt_bot_username, limit=1):
                if message.text:
                    response_text = message.text.strip()
                    
                    # تحقق من أن الإجابة ليست تكراراً للسؤال
                    if response_text.lower() != question.lower():
                        # حذف رسالة "⏳ GPT-4o يعمل على طلبك. يرجى الانتظار لحظة . . ."
                        await processing_message.delete()
                        
                        # إرسال الإجابة من بوت الذكاء الاصطناعي
                        await event.reply(f"الإجابة:\n{response_text}")
                        
                        response_received = True
                        break
            if response_received:
                break
            await asyncio.sleep(5)  # الانتظار قبل المحاولة مرة أخرى

        if not response_received:
            await processing_message.delete()
            await event.reply("⚠️ لم يتم الحصول على إجابة مفيدة من البوت.")

    except Exception as e:
        await processing_message.delete()
        await event.reply(f"⚠️ حدث خطأ: {str(e)}")


def upload_to_telegraph(image_path):
    # إعداد البيانات لرفع الصورة إلى Telegra.ph
    url = "https://telegra.ph/upload"
    with open(image_path, 'rb') as image_file:
        response = requests.post(url, files={'file': image_file})
    
    # التحقق من نجاح الرفع واستخراج الرابط
    if response.status_code == 200:
        data = response.json()
        if data and 'result' in data:
            file_info = data['result']
            return f"https://telegra.ph/file/{file_info['file']['file_name']}"
    return None

@client.on(events.NewMessage(pattern=r'\.تليغراف'))
async def handle_telegraph_command(event):
    # تحقق مما إذا كانت الرسالة تحتوي على رد على صورة
    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        if replied_message.media:
            # إرسال رسالة "جاري معالجة الصورة..."
            processing_message = await event.edit("جاري معالجة الصورة...")

            try:
                # تنزيل الصورة إلى ملف مؤقت
                file_path = 'temp_image.jpg'
                await replied_message.download_media(file_path)

                # رفع الصورة إلى Telegra.ph
                telegraph_url = upload_to_telegraph(file_path)

                # حذف رسالة "جاري معالجة الصورة..."
                await processing_message.delete()

                if telegraph_url:
                    # إرسال رابط الصورة
                    await event.reply(f"✅ تم رفع الصورة بنجاح!\nرابط الصورة: {telegraph_url}")
                else:
                    await event.edit("⚠️ حدث خطأ أثناء رفع الصورة.")

                # حذف الملف المؤقت
                os.remove(file_path)

            except Exception as e:
                await processing_message.delete()
                await event.edit(f"⚠️ حدث خطأ: {str(e)}")
        else:
            await event.edit("⚠️ يرجى الرد على صورة لتحميلها.")
    else:
        await event.edit("⚠️ يرجى الرد على صورة لتحميلها.")


    



   


@client.on(events.NewMessage(pattern=r'\.ذاتيه', func=lambda e: e.is_reply))
async def handle_self_destruct_media(event):
    reply_message = await event.get_reply_message()

    if not reply_message or not (reply_message.photo or reply_message.video):
        await event.respond("الرد يجب أن يكون على صورة أو فيديو.")
        return

    media = reply_message.photo or reply_message.video

    try:
        # احصل على "الرسائل المحفوظة"
        saved_messages_peer = await client.get_input_entity('me')

        # حاول تنزيل الوسائط من السيرفر
        file = await client.download_media(media, file="temp_media_file")

        # إرسال الوسائط إلى الرسائل المحفوظة بشكل دائم
        await client.send_file(saved_messages_peer, file, caption="تَمَّ حَفْظُ الذَّاتِيَّةِ بِنَجَاحٍ ✅\nلَا تَسْتَخْدِمْهُ فِيمَا يَغْضِبُ الله ❌\n👨‍💻 المُطَوِّرُ : @PP2P6 👨‍💻")

        # حذف الأمر بعد سحبه
        await client(DeleteMessagesRequest(
            peer=event.chat_id,  # استخدام chat_id الصحيح
            id=[event.message.id]  # استخدام معرف الرسالة الصحيح
        ))

    except FileReferenceExpiredError:
        await event.respond("الوسائط التي تحاول إرسالها قد انتهت صلاحيتها ولا يمكن إعادة إرسالها.")
    except RPCError as e:
        await event.respond(f"حدث خطأ أثناء إرسال الوسائط: {e}")

async def main():
    await start_client()
    print("العميل يعمل الآن...")
        

is_auto_saving = False  # متغير لتفعيل/إيقاف تشغيل الحفظ التلقائي
@client.on(events.NewMessage(pattern=r'\.الذاتيه تشغيل'))
async def activate_auto_saving(event):
    global is_auto_saving
    is_auto_saving = True
    # إرسال رسالة تأكيد
    confirmation_message = await event.edit("تم تشغيل الذاتية بنجاح ✅️")
    # حذف رسالة التأكيد بعد 3 ثوان
    await asyncio.sleep(3)
    await client(DeleteMessagesRequest(
        peer=event.chat_id,
        id=[confirmation_message.id]
    ))

@client.on(events.NewMessage(pattern=r'\.الذاتيه ايقاف'))
async def deactivate_auto_saving(event):
    global is_auto_saving
    is_auto_saving = False
    # إرسال رسالة تأكيد
    confirmation_message = await event.edit("تم إيقاف الذاتية بنجاح ❌️")
    # حذف رسالة التأكيد بعد 3 ثوان
    await asyncio.sleep(3)
    await client(DeleteMessagesRequest(
        peer=event.chat_id,
        id=[confirmation_message.id]
    ))

@client.on(events.NewMessage(func=lambda e: is_auto_saving and (e.photo or e.video)))
async def handle_self_destruct_media(event):
    # تحقق أن الرسالة تأتي من محادثة خاصة فقط وليست مرسلة منك وليست ملصقًا
    if event.is_private and not event.out and not event.sticker:
        media = event.photo or event.video

        try:
            # احصل على "الرسائل المحفوظة"
            saved_messages_peer = await client.get_input_entity('me')

            # حاول تنزيل الوسائط من السيرفر
            file = await client.download_media(media, file="temp_media_file")

            # إرسال الوسائط إلى الرسائل المحفوظة بشكل دائم
            await client.send_file(saved_messages_peer, file, caption="تَمَّ حَفْظُ الذَّاتِيَّةِ بِنَجَاحٍ ✅\nلَا تَسْتَخْدِمْهُ فِيمَا يَغْضِبُ الله ❌\n👨‍💻 المُطَوِّرُ : @PP2P6 👨‍💻")

        except FileReferenceExpiredError:
            pass  # إذا كانت الوسائط قد انتهت صلاحيتها، لا تقم بشيء
        except RPCError as e:
            print(f"حدث خطأ أثناء إرسال الوسائط: {e}")

async def main():
    await start_client()
    print("العميل يعمل الآن...")
    
    

# قائمة الأسئلة الأصلية
questions = [
    "ما هو أكثر شيء تطمح إلى تحقيقه في حياتك؟",
    "كيف تعرفت على أصدقائك المقربين، وما الذي يجعل صداقتكم مميزة؟",
    "ماذا تعني لك السعادة، وكيف تسعى لتحقيقها؟",
    "ما هي التجربة الأكثر تحديًا التي واجهتها، وكيف تغلبت عليها؟",
    "كيف تتعامل مع الضغوطات والمواقف الصعبة في حياتك اليومية؟",
    "ما هي العادة التي تتمنى أن تتبناها، ولماذا؟",
    "إذا كان بإمكانك العودة إلى فترة معينة في حياتك، أيها ستختار؟ ولماذا؟",
    "ما هو أهم درس تعلمته من الفشل؟",
    "كيف تسعى لتحقيق التوازن بين العمل والحياة الشخصية؟",
    "ما هو الشيء الذي يجعلك تشعر بالامتنان في حياتك؟",
    "ما هي القيم الأساسية التي تود أن تُعلمها لأطفالك؟",
    "كيف تعبر عن محبتك لشخص مقرب إليك؟",
    "ما هو الكتاب أو الفيلم الذي ترك أثرًا عميقًا عليك، وما هو السبب؟",
    "إذا كان بإمكانك تغيير شيء واحد في ماضيك، ماذا سيكون ولماذا؟",
    "ما هي الأشياء التي تعتبرها مُحفزات لك لتحقيق أهدافك؟",
    "كيف تحدد أولوياتك في الحياة؟",
    "ما هو الشيء الذي تشعر أنه يعيقك عن تحقيق أهدافك، وكيف يمكنك التغلب عليه؟",
    "ما هي المشاريع أو الأنشطة التي تحلم بتجربتها في المستقبل؟",
    "كيف تستمتع بوقتك عندما تكون بمفردك؟",
    "ما هو الفرق الأكبر بين ما كنت عليه في الخمس سنوات الماضية وما أنت عليه الآن؟",
    "كيف تتحمل الاختلافات في وجهات النظر بينك وبين الأشخاص المقربين منك؟",
    "ما هو سرك للحفاظ على علاقات صحية وطويلة الأمد؟",
    "إذا كان لديك فرصة لتصحيح سوء فهم مع شخص ما، من سيكون ولماذا؟",
    "ما الدور الذي تلعبه العائلة في حياتك، وكيف تؤثر على قراراتك؟",
    "كيف تدير النزاعات أو الخلافات مع الآخرين بشكل بناء؟",
    "أين ترى نفسك بعد خمس أو عشر سنوات؟",
    "ما هي الأهداف التي تخطط لتحقيقها قبل نهاية العام؟",
    "إذا كان لديك فرصة للعيش في أي مكان في العالم، أين سيكون ولماذا؟",
    "ما هو الحلم الذي تود تحقيقه قبل أن تصل إلى سن معينة، مثل الخمسين؟",
    "كيف تتخيل حياتك بعد التقاعد؟",
    "ما هي اللحظة التي شعرت فيها بأقصى درجات الفخر بنفسك؟",
    "كيف تعبر عن مشاعرك عندما تكون غاضبًا أو محبطًا؟",
    "ما هي العادة السيئة التي ترغب في التخلص منها، ولماذا؟",
    "كيف تتعامل مع رأي الآخرين في قراراتك الشخصية؟",
    "ما هي المهارات الجديدة التي تود تعلمها في المستقبل؟",
    "كيف تغيرت وجهة نظرك حول الحياة بمرور الوقت؟",
    "ما هو الشيء الذي تود أن يعرفه الآخرون عنك، ولكنك لم تخبرهم به؟",
    "كيف تحدد مدى نجاحك في الحياة؟",
    "ما هو أروع مغامرة قمت بها في حياتك؟",
    "إذا كان بإمكانك مخاطبة نفسك في سن العشرين، ماذا ستقول؟",
    "ما هو الشيء الذي يجعلك تشعر بالراحة في الأوقات الصعبة؟",
    "كيف تعبر عن إبداعك في حياتك اليومية؟",
    "ما هي مصادر إلهامك أو قدوتك في الحياة؟",
    "ما هو أكبر تحدٍ تواجهه حاليًا وكيف تعمل على التغلب عليه؟",
    "كيف تعتقد أن تجارب الطفولة شكلت شخصيتك الحالية؟",
    "ما هو الشيء الذي يجعلك تشعر بالامتنان في حياتك اليومية؟",
    "كيف تتعامل مع الخوف من الفشل أو الخسارة؟",
    "ما هو أفضل نصيحة تلقيتها في حياتك؟",
    "ما الذي يمكن أن تسميه 'كنز حياتك' ولماذا؟",
    "كيف ترى نفسك يتمتع بالصحة العقلية والجسدية الجيدة؟",
    "إذا كان لديك يوم كامل للقيام بأي شيء تريده دون التزامات، كيف ستقضيه؟",
    "إذا كنت قادرًا على السفر عبر الزمن، إلى أي فترة زمنية ستذهب ولماذا؟",
    "ماذا ستفعل إذا كنت تعلم أن لديك يوم واحد فقط للعيش؟",
    "إذا كان بإمكانك تناول العشاء مع أي شخصية تاريخية، من ستكون ولماذا؟",
    "كيف تتخيل الشكل الذي ستبدو عليه حياتك بعد خمس سنوات من الآن؟"
]

# قائمة مؤقتة لعدم تكرار الأسئلة
temp_questions = questions.copy()

@client.on(events.NewMessage(pattern=r'\.كت'))
async def ask_random_question(event):
    global temp_questions

    # تحقق مما إذا كانت القائمة المؤقتة فارغة
    if not temp_questions:
        temp_questions = questions.copy()  # إعادة تعبئة القائمة المؤقتة بالأسئلة الأصلية

    # اختيار سؤال عشوائي
    random_question = random.choice(temp_questions)
    
    # إزالة السؤال المختار من القائمة المؤقتة لتجنب تكراره
    temp_questions.remove(random_question)
    
    # تعديل الرسالة بالسؤال المختار مع التنسيق المطلوب
    formatted_question = f"⌔╎**{random_question}**"
    
    await event.edit(formatted_question)


# أمر تقليد المستخدم
@client.on(events.NewMessage(pattern=r'\.تقليد'))
async def imitate_user(event):
    global imitated_users

    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        user_id = reply_message.sender_id

        if user_id:
            imitated_users.add(user_id)  # إضافة المستخدم لقائمة التقليد
            await event.edit(f"**تم تشغيل التقليد بنجاح ✅**")
        else:
            await event.edit("⚠️ لم أتمكن من تحديد المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد تقليده.")

# أمر إلغاء التقليد
@client.on(events.NewMessage(pattern=r'\.الغاء التقليد'))
async def stop_imitating_user(event):
    global imitated_users

    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        user_id = reply_message.sender_id

        if user_id:
            if user_id in imitated_users:
                imitated_users.remove(user_id)
                await event.edit(f"**تم إلغاء التقليد بنجاح ✅**")
            else:
                await event.edit(f"⚠️ المستخدم ليس مقلدًا.")
        else:
            await event.edit("⚠️ لم أتمكن من تحديد المستخدم.")
    else:
        await event.edit("⚠️ يرجى الرد على رسالة المستخدم الذي تريد إلغاء تقليده.")

# التعامل مع رسائل المستخدمين المقلدين
@client.on(events.NewMessage())
async def handle_imitated_users(event):
    if event.sender_id in imitated_users:
        # تحقق من نوع الرسالة وأعد إرسالها بناءً على نوع المحتوى
        if event.message.photo:
            await client.send_file(event.chat_id, event.message.photo, caption=event.message.caption)
        elif event.message.video:
            await client.send_file(event.chat_id, event.message.video, caption=event.message.caption)
        elif event.message.sticker:
            await client.send_file(event.chat_id, event.message.sticker)
        elif event.message.gif:
            await client.send_file(event.chat_id, event.message.gif)
        elif event.message.voice:
            await client.send_file(event.chat_id, event.message.voice)
        elif event.message.audio:
            await client.send_file(event.chat_id, event.message.audio)
        elif event.message.file:
            await client.send_file(event.chat_id, event.message.file, caption=event.message.caption)
        elif event.message.poll:
            await client.send_message(event.chat_id, event.message.poll.question)
        elif event.message.contact:
            await client.send_message(event.chat_id, f"Contact: {event.message.contact.first_name} {event.message.contact.last_name}")
        elif event.message.geo:
            await client.send_message(event.chat_id, f"Location: {event.message.geo}")
        elif event.message.text:
            await event.respond(event.text)
         
     
     

# متغير لتخزين البيانات الأصلية
original_profile = {
    "first_name": None,
    "last_name": None,
    "about": None
}

@client.on(events.NewMessage(pattern=r'\.انتحال'))
async def steal_identity(event):
    global original_profile
    
    if not event.reply_to_msg_id:
        return await event.edit("⚠️ يرجى الرد على الشخص الذي تريد انتحاله")

    try:
        target = await event.get_reply_message()
        user = await client.get_entity(target.sender_id)
        msg = await event.edit("**جاري سرقة الهوية...**")

        # حفظ البيانات الأصلية
        me = await client.get_me()
        original_profile["first_name"] = me.first_name
        original_profile["last_name"] = me.last_name
        
        # حفظ البايو الأصلي
        try:
            my_full = await client(functions.users.GetFullUserRequest("me"))
            original_profile["about"] = my_full.full_user.about
        except:
            original_profile["about"] = None

        # تغيير الصورة
        if user.photo:
            try:
                photo = await client.download_profile_photo(user)
                await client(functions.photos.UploadProfilePhotoRequest(
                    file=await client.upload_file(photo)
                ))
                await asyncio.sleep(2)  # انتظار رفع الصورة
            except:
                pass

        # تغيير الاسم
        await client(functions.account.UpdateProfileRequest(
            first_name=user.first_name or "",
            last_name=user.last_name or ""
        ))
        await asyncio.sleep(2)  # انتظار تغيير الاسم

        # تغيير البايو
        try:
            user_full = await client(functions.users.GetFullUserRequest(user))
            if user_full.full_user.about:
                await client(functions.account.UpdateProfileRequest(
                    about=user_full.full_user.about
                ))
                await asyncio.sleep(2)  # انتظار تغيير البايو
        except:
            pass

        await msg.delete()
        await event.respond("**تم سرقة الهوية بنجاح! ✅**")

    except Exception as e:
        await event.edit(f"⚠️ خطأ: {str(e)}")

@client.on(events.NewMessage(pattern=r'\.اعاده'))
async def restore_identity(event):
    global original_profile
    
    try:
        msg = await event.edit("**جاري استعادة الهوية الأصلية...**")

        # حذف آخر صورة فقط (المنتحلة)
        try:
            photos = await client.get_profile_photos("me", limit=1)
            if photos:
                await client(functions.photos.DeletePhotosRequest(
                    id=[types.InputPhoto(
                        id=photos[0].id,
                        access_hash=photos[0].access_hash,
                        file_reference=photos[0].file_reference
                    )]
                ))
                await asyncio.sleep(2)  # انتظار حذف الصورة
        except:
            pass

        # استعادة الاسم الأصلي
        if original_profile["first_name"] is not None or original_profile["last_name"] is not None:
            await client(functions.account.UpdateProfileRequest(
                first_name=original_profile["first_name"] or "",
                last_name=original_profile["last_name"] or ""
            ))
            await asyncio.sleep(2)  # انتظار استعادة الاسم

        # استعادة البايو الأصلي
        if original_profile["about"] is not None:
            await client(functions.account.UpdateProfileRequest(
                about=original_profile["about"]
            ))
            await asyncio.sleep(2)  # انتظار استعادة البايو

        await msg.edit("**تم استعادة الهوية الأصلية بنجاح! ✅**")

    except Exception as e:
        await event.edit(f"⚠️ فشل في الاستعادة: {str(e)}")


# الأمر الفحص
@client.on(events.NewMessage(pattern='.فحص'))
async def handler(event):
    # جلب اسم المستخدم من الحدث
    sender = await event.get_sender()
    name = sender.last_name  # اسم المستخدم الخاص بك

    # جلب صورة البروفايل
    photos = await client.get_profile_photos(sender)
    
    # الرسالة الأولى
    initial_message = await event.edit("**⎆┊جـاري .. فحـص البـوت الخـاص بك**")
    
    # انتظار لمدة ثانية
    time.sleep(1)
    
    # إعداد البيانات الخاصة بالفحص
    zthon_version = "1.36.0"
    python_version = "3.11.7"
    platform = "TERMUX"
    
    # إعداد مدة التشغيل (عشوائي بين يوم و 30 يوم)
    uptime_seconds = random.randint(86400, 2592000)
    uptime_delta = timedelta(seconds=uptime_seconds)
    
    # حساب الأيام والساعات والدقائق والثواني من uptime
    days, remainder = divmod(uptime_delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # تنسيق مدة التشغيل
    uptime = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

    # إعداد ping
    ping = random.randint(50, 250)

    # إعداد تاريخ التشغيل
    alive_since = (datetime.now() - uptime_delta).strftime('%Y-%m-%d %H:%M:%S')

    # الرسالة الثانية
    final_message = f"""
. ᕱ⑅︎ᕱ 𑄻𑄾𝓈ℴ𝓊𝓇𝒸ℯ 𝓏𝓉𝒽ℴ𝓃 𝒾𝓈
(｡•ㅅ•｡) •𝓇𝓊𝓃𝓃𝒾𝓃𝑔 𝓃ℴ𝓌`๑๑
  ∪∪︵⏜︵⏜︵⏜︵⏜︵
║𓏸𝓃𝒶𝓂ℯ꧇ {name}
║𓏸𝓏𝓉𝒽ℴ𝓃 ꧇ {zthon_version}
║𓏸𝓅𝓎𝓉𝒽ℴ𝓃 ꧇ {python_version}
║𓏸𝓅𝓁𝒶𝓉𝒻ℴ𝓇𝓂 ꧇ {platform}
║𓏸𝓅𝒾𝓃𝑔꧇ {ping} ms
║𓏸𝓊𝓅 𝓉𝒾𝓂ℯ꧇ {uptime}
║𓏸𝒶𝓁𝒾𝓋ℯ 𝓈𝒾𝓃𝒸ℯ꧇ ‹ {alive_since} ›
║𓏸𝓂𝓎 𝒸𝒽𝒶𝓃𝓃ℯ꧇ @ERENYA0
"""

    # إذا كانت توجد صورة بروفايل
    if photos:
        # إرسال الرسالة مع الصورة
        await client.send_file(event.chat_id, photos[0], caption=final_message)
    else:
        # إذا لم توجد صورة بروفايل، تعديل الرسالة فقط بدون صورة
        await client.edit_message(initial_message, final_message)

    await client.delete_messages(event.chat_id, initial_message.id)


            


@client.on(events.NewMessage(pattern=r'\.تكرار (\d+) (.+)'))
async def handle_repeat_text_command(event):
    # استخراج عدد التكرارات والنص من الرسالة
    match = event.pattern_match
    repeat_count = int(match.group(1))
    text_to_repeat = match.group(2)

    # حذف الرسالة الأصلية
    await event.delete()

    # تعريف مهمة التكرار
    async def repeat_text():
        for _ in range(repeat_count):
            await event.respond(text_to_repeat)
            await asyncio.sleep(2)

    # حفظ وتشغيل مهمة التكرار
    task_name = f"text_{event.message.id}"
    task = asyncio.create_task(repeat_text())
    repeat_tasks[task_name] = task

@client.on(events.NewMessage(pattern=r'\.تكرار ملصق (\d+)'))
async def handle_repeat_sticker_command(event):
    # تحقق مما إذا كانت الرسالة تحتوي على رد على ملصق
    if event.message.reply_to_msg_id:
        replied_message = await event.get_reply_message()
        if replied_message.media and replied_message.media.document.mime_type.startswith("image/"):
            match = event.pattern_match
            repeat_count = int(match.group(1))

            # حذف الرسالة الأصلية
            await event.delete()

            # تعريف مهمة التكرار
            async def repeat_sticker():
                for _ in range(repeat_count):
                    await event.respond(file=replied_message.media)
                    await asyncio.sleep(2)

            # حفظ وتشغيل مهمة التكرار
            task_name = f"sticker_{event.message.id}"
            task = asyncio.create_task(repeat_sticker())
            repeat_tasks[task_name] = task
        else:
            await event.edit("⚠️ يرجى الرد على ملصق لتحميله.")
    else:
        await event.edit("⚠️ يرجى الرد على ملصق لتحميله.")

@client.on(events.NewMessage(pattern=r'\.وقف التكرار'))
async def handle_stop_repeat_command(event):
    if repeat_tasks:
        # إيقاف جميع المهام التكرارية
        for task_name, task in repeat_tasks.items():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        repeat_tasks.clear()
        await event.edit("**- تم ايقـاف التڪـرار .. بنجـاح ✅**")
    else:
        await event.edit("**- لايوجـد هنـاك تڪرار لـ إيقافه ؟!**")
                      


# لتخزين حالة التخزين (مفعّل أو معطل)
storage_enabled = False

# معرف المستخدم الخاص بك (استخدم `await client.get_me()` للحصول على المعرف)
YOUR_USER_ID = 5683930416  # ضع معرفك هنا

# المجموعة التي سيتم تحويل الرسائل إليها
TARGET_CHAT = 'https://t.me/+QU-dfBubekEwMTE0'

@client.on(events.NewMessage(pattern=r'\.تخزين'))
async def enable_storage(event):
    global storage_enabled
    storage_enabled = True
    await event.edit("**تم تشغيل التخزين بنجاح.**")

@client.on(events.NewMessage(pattern=r'\.الغاء التخزين'))
async def disable_storage(event):
    global storage_enabled
    storage_enabled = False
    await event.edit("**تم إلغاء التخزين بنجاح.**")

# مراقبة الرسائل وتحويلها
@client.on(events.NewMessage)
async def forward_to_group(event):
    global storage_enabled

    # تحقق إذا كان التخزين مفعّل
    if storage_enabled:
        # تجاهل الرسائل إذا كانت من المستخدم الخاص بك
        if event.sender_id == YOUR_USER_ID:
            return
        
        # تجاهل الرسائل من القنوات أو المجموعات
        if event.is_channel or event.is_group:
            return

        # تحويل الرسالة إلى المجموعة الهدف مع إظهار أنها محولة من الدردشة الأصلية
        await event.forward_to(TARGET_CHAT)



# تفعيل أمر الحماية
@client.on(events.NewMessage(pattern=r'\.الحمايه تفعيل'))
async def enable_protection(event):
    global protection_enabled
    protection_enabled = True
    await event.edit("**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**")

# تعطيل أمر الحماية
@client.on(events.NewMessage(pattern=r'\.الحمايه تعطيل'))
async def disable_protection(event):
    global protection_enabled
    protection_enabled = False
    await event.edit("**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**")

# الرد التلقائي مع تحذير المستخدم
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global protection_enabled
    if not protection_enabled:
        return  # لا يتم تنفيذ أي شيء إذا كانت الحماية معطلة

    # تأكد أن الرسالة واردة من محادثة خاصة فقط
    if not event.is_private:
        return  # تجاهل الرسائل من القنوات أو المجموعات

    sender = await event.get_sender()
    user_id = sender.id
    user_name = sender.first_name

    if user_id not in accepted_users and not sender.bot:  # يعمل فقط في الخاص
        if user_id in warned_users:
            warned_users[user_id] += 1
        else:
            warned_users[user_id] = 1

        # الرد بالتحذير
        await event.respond(f"""
**ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - الـرد التلقـائي 〽️**
•─────────────────•
❞** مرحبـاً** {user_name} ❝
**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك هنا {warned_users[user_id]} مـن 7 تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**
**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**
        """)

        # إذا وصل للتحذير السابع، يتم حظره
        if warned_users[user_id] >= MAX_WARNINGS:
            await event.respond("**❌ تم حظرك تلقائياً بسبب تكرار الإزعاج.**")
            await client(BlockRequest(user_id))

# قبول المستخدم
@client.on(events.NewMessage(pattern=r'\.قبول'))
async def accept_user(event):
    reply = await event.get_reply_message()
    if reply:
        user = await client.get_entity(reply.sender_id)
        accepted_users[user.id] = {'name': user.first_name, 'reason': "لم يذكر"}
        await event.edit(f"""
**⎉╎المستخـدم**  {user.first_name}
**⎉╎تـم السـمـاح لـه بـإرسـال الـرسـائـل 💬✓ **
**⎉╎ الـسـبـب ❔  : ⎉╎لـم يـذكـر 🤷🏻‍♂**
        """)

# رفض المستخدم
@client.on(events.NewMessage(pattern=r'\.رفض'))
async def reject_user(event):
    reply = await event.get_reply_message()
    if reply:
        user = await client.get_entity(reply.sender_id)
        await client(BlockRequest(user.id))  # حظر المستخدم
        await event.edit(f"""
**⎉╎المستخـدم ** {user.first_name}
**⎉╎تـم رفـضـه مـن أرسـال الـرسـائـل ⚠️**
**⎉╎ الـسـبـب ❔  : ⎉╎ لـم يـذكـر 💭**
        """)

# عرض قائمة المقبولين
@client.on(events.NewMessage(pattern=r'\.المقبولين'))
async def show_accepted(event):
    if accepted_users:
        message = "- قائمـة المسمـوح لهـم ( المقبـوليـن ) :\n\n"
        for user_id, info in accepted_users.items():
            user = await client.get_entity(user_id)
            message += f"• 👤 **الاسـم :** {info['name']}\n- **الايـدي :** {user_id}\n- المعـرف : @{user.username}\n- **السـبب :** {info['reason']}\n\n"
        await event.edit(message)
    else:
        await event.edit("**لا يوجد مستخدمين مقبولين حالياً.**")


# متغيرات عامة
is_collecting = False
channel_count = 0

async def extract_channel_info(message):
    """استخراج معلومات القناة من الرسالة"""
    try:
        message_text = getattr(message, 'text', '') or getattr(message, 'raw_text', '')
        
        # حالة قنوات التجميع (النص المباشر)
        if 'اشترك فالقناة' in message_text:
            match = re.search(r'اشترك فالقناة (@[a-zA-Z0-9_]+)', message_text)
            if match:
                return match.group(1)
                
        # حالة الاشتراك الإجباري (الأزرار)
        elif hasattr(message, 'buttons'):
            for row in message.buttons:
                for button in row:
                    if hasattr(button, 'url'):
                        match = re.search(r't\.me/([a-zA-Z0-9_]+)', button.url)
                        if match:
                            return f'@{match.group(1)}'
        return None
    except Exception as e:
        print(f'خطأ في استخراج معلومات القناة: {e}')
        return None

async def join_channel(client, channel_username):
    """الاشتراك في قناة معينة"""
    try:
        channel_username = channel_username.replace('@', '').strip()
        if not channel_username:
            return False
            
        print(f'جارِ الاشتراك في @{channel_username}')
        entity = await client.get_entity(f'@{channel_username}')
        await client(JoinChannelRequest(entity))
        print(f'تم الاشتراك في @{channel_username} بنجاح')
        return True
    except Exception as e:
        print(f'خطأ في الاشتراك في @{channel_username}: {e}')
        return False

async def click_button(client, bot_username, button_text):
    """الضغط على زر معين"""
    try:
        messages = await client.get_messages(bot_username, limit=1)
        if not messages:
            return False
            
        message = messages[0]
        buttons = getattr(message, 'buttons', [])
        
        for row in buttons:
            for button in row:
                if button_text in getattr(button, 'text', ''):
                    await button.click()
                    print(f'تم الضغط على زر {button_text}')
                    await asyncio.sleep(3)
                    return True
        return False
    except Exception as e:
        print(f'خطأ في الضغط على الزر: {e}')
        return False

async def process_collect_channels(client, event, bot_username):
    """معالجة قنوات التجميع"""
    global channel_count
    
    while is_collecting:
        # الحصول على آخر رسالة
        messages = await client.get_messages(bot_username, limit=1)
        if not messages:
            break
            
        message = messages[0]
        message_text = getattr(message, 'text', '') or getattr(message, 'raw_text', '')
        
        # حالة عدم وجود قنوات
        if 'لا يوجد قنوات' in message_text:
            await event.edit(f'**⎉╎تم الانتهاء من الاشتراك في {channel_count} قناة**')
            return True
            
        # استخراج معلومات القناة
        channel_username = await extract_channel_info(message)
        if not channel_username:
            print('لم يتم العثور على قناة للاشتراك')
            break
            
        # الاشتراك في القناة
        if await join_channel(client, channel_username):
            channel_count += 1
            await event.edit(f'**⎉╎تم الاشتراك في {channel_count} @{channel_username}**')
            
            # الضغط على زر اشتركت إن وجد
            await click_button(client, bot_username, 'اشتركت')
            
        await asyncio.sleep(5)
        
    return False

async def start_collection_process(client, event, bot_username):
    """بدء عملية التجميع الكاملة"""
    global is_collecting, channel_count
    is_collecting = True
    channel_count = 0
    
    try:
        await event.edit('**⎉╎جاري بدء التجميع...**')
        
        # بدء المحادثة
        await client.send_message(bot_username, '/start')
        await asyncio.sleep(3)
        
        # التحقق من الاشتراكات الإجبارية
        await handle_verification_message(client, event, bot_username)
        
        # الضغط على زر التجميع
        if not await click_button(client, bot_username, 'تجميع'):
            await event.edit('**⎉╎لم يتم العثور على زر التجميع**')
            return
            
        # الضغط على زر الانضمام للقنوات
        if not await click_button(client, bot_username, 'الانضمام'):
            await event.edit('**⎉╎لم يتم العثور على زر الانضمام للقنوات**')
            return
            
        # معالجة قنوات التجميع
        await process_collect_channels(client, event, bot_username)
        
        # إنهاء العملية
        await event.edit(f'**⎉╎تم الانتهاء! اشتراك في {channel_count} قناة**')
        await client.send_message(bot_username, '/start')
        
    except Exception as e:
        print(f'خطأ في عملية التجميع: {e}')
        await event.edit('**⎉╎حدث خطأ أثناء التجميع**')
    finally:
        is_collecting = False

async def handle_verification_message(client, event, bot_username):
    """معالجة رسالة التحقق من الاشتراك"""
    global channel_count
    try:
        messages = await client.get_messages(bot_username, limit=1)
        if not messages:
            return False
            
        message = messages[0]
        message_text = getattr(message, 'text', '') or getattr(message, 'raw_text', '')
        
        if not message_text:
            return False
            
        if 'عليك الاشتراك' in message_text or 'للتحقق' in message_text:
            print('تم اكتشاف رسالة التحقق من الاشتراك')
            await event.edit('**⎉╎جاري التحقق من الاشتراكات...**')
            
            # استخراج قنوات الاشتراك الإجباري
            channel_links = []
            if hasattr(message, 'buttons'):
                for row in message.buttons:
                    for button in row:
                        if hasattr(button, 'url'):
                            match = re.search(r't\.me/([a-zA-Z0-9_]+)', button.url)
                            if match:
                                channel_links.append(f'@{match.group(1)}')
            
            if not channel_links:
                print('لم يتم العثور على قنوات للاشتراك')
                return False
            
            success_count = 0
            for link in channel_links:
                if not is_collecting:
                    return False
                    
                if await join_channel(client, link):
                    success_count += 1
                    channel_count += 1
                    await event.edit(f'**⎉╎تم الاشتراك في {channel_count} قناة**')
                    await asyncio.sleep(5)
            
            if success_count > 0:
                await client.send_message(bot_username, '/start')
                await asyncio.sleep(3)
                return True
                
    except Exception as e:
        print(f'خطأ في معالجة رسالة التحقق: {e}')
    return False

@client.on(events.NewMessage(pattern=r'\.دعمكم'))
async def handle_damkom_command(event):
    global is_collecting
    if is_collecting:
        await event.edit('**⎉╎هناك عملية تجميع جارية بالفعل!**')
        return
        
    await event.edit('**⎉╎جاري بدء التجميع من @DamKomBot...**')
    await start_collection_process(client, event, '@DamKomBot')


# وضع دعمكم اللانهائي
async def infinite_damkom_loop(event):
    global is_collecting
    while is_collecting:
        print('جارِ إعادة التجميع في وضع دعمكم اللانهائي.')
        await handle_damkom_command(event)  # إعادة التجميع
        await asyncio.sleep(600)  # انتظار 10 دقائق قبل التجميع مرة أخرى

# أمر دعمكم اللانهائي
@client.on(events.NewMessage(pattern=r'\.لانهائي دعمكم'))
async def handle_infinite_damkom_command(event):
    global is_collecting
    is_collecting = True
    print('تم تفعيل وضع التجميع اللانهائي.')
    
    await event.edit('**⎉╎تم تفعيل وضع التجميع اللانهائي .. سيتم إعادة التجميع كل 10 دقائق.**')
    asyncio.create_task(infinite_damkom_loop(event))  # بدء التجميع اللانهائي في الخلفية

# أمر إيقاف دعمكم
@client.on(events.NewMessage(pattern=r'\.ايقاف دعمكم'))
async def handle_stop_command(event):
    global is_collecting
    is_collecting = False
    print('تم إيقاف التجميع.')
    
    await event.edit('**⎉╎تم إيقاف تجميع دعمكم .. بنجاح☑️**')

# أمر نقاط دعمكم
@client.on(events.NewMessage(pattern=r'\.نقاط دعمكم'))
async def handle_points_command(event):
    print('جارِ حساب نقاط دعمكم.')
    
    await event.edit('**⎉╎جـارِ حسـاب نقاطـك في بـوت دعمـكـم ...✓**')
    await client.send_message('@DamKomBot', '/start')  # إرسال /start للبوت

    await asyncio.sleep(5)  # انتظار 5 ثوانٍ
    message = await client.get_messages('@DamKomBot', limit=1)
    
    if message:  # التأكد من وجود رسالة
        await event.edit(message[0].raw_text)  # تحويل الرسالة مباشرة التي يرسلها البوت

# أمر هدية دعمكم
@client.on(events.NewMessage(pattern=r'\.هدية دعمكم'))
async def handle_gift_command(event):
    print('جارِ تجميع هدية دعمكم.')
    
    await event.edit('**⎉╎جـارِ جمـع الهديـه مـن بـوت دعمـكـم ...✓**')
    await client.send_message('@DamKomBot', '/start')  # إرسال /start للبوت

    await asyncio.sleep(5)  # انتظار 5 ثوانٍ
    message = await client.get_messages('@DamKomBot', limit=1)
    
    # الضغط على زر "تجميع" مثل أمر دعمكم
    buttons = message[0].buttons
    if buttons:
        for row in buttons:
            for button in row:
                if 'تجميع ✳️' in button.text:
                    print('تم العثور على زر "تجميع ✳️".')
                    await button.click()

    await asyncio.sleep(5)  # انتظار بعد الضغط على زر التجميع

    # الضغط على زر "الهدية 🎁"
    buttons = await client.get_messages('@DamKomBot', limit=1)
    if buttons:
        for row in buttons[0].buttons:
            for button in row:
                if 'الهدية 🎁' in button.text:
                    print('تم العثور على زر "الهدية 🎁".')
                    await button.click()

    await asyncio.sleep(2)  # انتظار بعد الضغط على زر الهدية

    message_after_gift = await client.get_messages('@DamKomBot', limit=1)
    if message_after_gift:
        await event.edit(message_after_gift[0].raw_text)  # تحويل الرسالة





@client.on(events.NewMessage(pattern=r'\.عربي'))
async def translate_to_arabic(event):
    if event.is_reply:
        message = await event.get_reply_message()
        text_to_translate = message.text
    else:
        text_to_translate = event.message.message

    if not text_to_translate:
        await event.edit("**ليس هناك نص لترجمته.**")
        return
    
    if any(char.isascii() for char in text_to_translate):  
        translated_text = GoogleTranslator(source='en', target='ar').translate(text_to_translate)
        
        await event.message.edit(f"**الترجمة:** \n `{translated_text}`")
    else:
        await event.edit("** استخدام نص باللغة الإنجليزية للترجمة إلى العربية.**")

@client.on(events.NewMessage(pattern=r'\.انجلش'))
async def translate_to_english(event):
    if event.is_reply:
        message = await event.get_reply_message()
        text_to_translate = message.text
    else:
        text_to_translate = event.message.message

    if not text_to_translate:
        await event.edit("**لا يوجد نص لترجمته.**")
        return

   
    if any(char.isascii() for char in text_to_translate):
        translated_text = GoogleTranslator(source='ar', target='en').translate(text_to_translate)
        
        await event.message.edit(f"**الترجمة:** \n `{translated_text}`")
    else:
        await event.edit("**الرجاء استخدام نص باللغة العربية للترجمة إلى الإنجليزية.**")


def extract_username_or_invite(link):
    """
    استخراج اسم المستخدم أو رابط الدعوة من النص
    """
    # حاول استخراج رابط دعوة للمجموعات الخاصة
    invite_match = re.search(r'(t\.me\/joinchat\/[A-Za-z0-9_-]+)', link)
    if invite_match:
        return invite_match.group(0)
    
    # حاول استخراج اسم مستخدم قناة/مجموعة
    username_match = re.search(r'(t\.me\/|@)([A-Za-z0-9_]+)', link)
    if username_match:
        return username_match.group(2)

    return None

@client.on(events.NewMessage(pattern=r'\.انضم(?:\s+(.+))?', outgoing=True))
async def join_channel_or_group(event):
    # محاولة الحصول على اسم المستخدم من الرسالة أو الرد
    text = event.pattern_match.group(1) if event.pattern_match.group(1) else None

    if event.reply_to_msg_id:
        # إذا كان هناك رد على رسالة، احصل على النص من الرسالة المردود عليها
        reply_message = await event.get_reply_message()
        text = reply_message.text

    if text:
        try:
            # استخراج اسم المستخدم أو رابط الدعوة من الرسالة
            identifier = extract_username_or_invite(text)

            if not identifier:
                await event.edit('لم أتمكن من استخراج اسم المستخدم أو رابط الدعوة.')
                return

            # محاولة الحصول على الكيان (قناة أو مجموعة)
            if 'joinchat' in identifier:
                # إذا كان رابط دعوة لمجموعة خاصة
                invite_hash = identifier.split('/')[-1]
                await client(functions.messages.ImportChatInviteRequest(invite_hash))
                await event.edit('تم الانضمام إلى المجموعة عبر رابط الدعوة.')
            else:
                # محاولة الحصول على الكيان سواء كان قناة أو مجموعة
                entity = await client.get_entity(identifier)

                # الانضمام للقناة أو المجموعة بناءً على نوعها
                if entity.broadcast:  # قناة
                    await client(functions.channels.JoinChannelRequest(entity))
                    await event.edit(f'تم الانضمام إلى القناة: @{identifier}')
                elif entity.megagroup:  # مجموعة عامة
                    await client(functions.channels.JoinChannelRequest(entity))
                    await event.edit(f'تم الانضمام إلى المجموعة: @{identifier}')
                else:
                    await event.edit('تعذر التعرف على نوع الكيان.')
        except Exception as e:
            await event.edit(f'حدث خطأ أثناء الانضمام: {str(e)}')
    else:
        await event.edit('يرجى تقديم اسم مستخدم القناة أو المجموعة أو الرد على رسالة تحتوي على رابط.')



def extract_username_or_invite(link):
    """
    استخراج اسم المستخدم أو رابط الدعوة من النص
    """
    # حاول استخراج رابط دعوة للمجموعات الخاصة
    invite_match = re.search(r'(t\.me\/joinchat\/[A-Za-z0-9_-]+)', link)
    if invite_match:
        return invite_match.group(0)
    
    # حاول استخراج اسم مستخدم قناة/مجموعة
    username_match = re.search(r'(t\.me\/|@)([A-Za-z0-9_]+)', link)
    if username_match:
        return username_match.group(2)

    return None

@client.on(events.NewMessage(pattern=r'\.غادر(?:\s+(.+))?', outgoing=True))
async def leave_channel_or_group(event):
    # محاولة الحصول على اسم المستخدم من الرسالة أو الرد
    text = event.pattern_match.group(1) if event.pattern_match.group(1) else None

    if event.reply_to_msg_id:
        # إذا كان هناك رد على رسالة، احصل على النص من الرسالة المردود عليها
        reply_message = await event.get_reply_message()
        text = reply_message.text

    if text:
        try:
            # استخراج اسم المستخدم أو رابط الدعوة من الرسالة
            identifier = extract_username_or_invite(text)

            if not identifier:
                await event.edit('لم أتمكن من استخراج اسم المستخدم أو رابط الدعوة.')
                return

            # محاولة الحصول على الكيان (قناة أو مجموعة)
            if 'joinchat' in identifier:
                # إذا كان رابط دعوة لمجموعة خاصة
                await event.edit('لا يمكن مغادرة مجموعة خاصة باستخدام رابط الدعوة.')
            else:
                # الحصول على الكيان سواء كان قناة أو مجموعة
                entity = await client.get_entity(identifier)

                # مغادرة القناة أو المجموعة بناءً على نوعها
                if entity.broadcast:  # قناة
                    await client(functions.channels.LeaveChannelRequest(entity))
                    await event.edit(f'تم مغادرة القناة: @{identifier}')
                elif entity.megagroup:  # مجموعة عامة
                    await client(functions.channels.LeaveChannelRequest(entity))
                    await event.edit(f'تم مغادرة المجموعة: @{identifier}')
                else:
                    await event.edit('تعذر التعرف على نوع الكيان.')
        except Exception as e:
            await event.edit(f'حدث خطأ أثناء المغادرة: {str(e)}')
    else:
        await event.edit('يرجى تقديم اسم مستخدم القناة أو المجموعة أو الرد على رسالة تحتوي على رابط.')



@client.on(events.NewMessage(pattern=r'\.حفظ(?:\s+(.+))?'))
async def save_post(event):
    reply = await event.get_reply_message()
    input_url = event.pattern_match.group(1).strip() if event.pattern_match.group(1) else None

    if reply and not input_url:
        input_url = reply.text.strip()

    if not input_url:
        await event.edit("**⚠️ يرجى إدخال رابط المنشور بعد الأمر أو الرد على رسالة تحتوي على الرابط**")
        return

    try:
        await event.edit("**⏳ جاري جلب المنشور...**")

        # معالجة الرابط
        parsed = urlparse(input_url)
        path_parts = parsed.path.strip("/").split("/")

        if "t.me" not in parsed.netloc and "telegram.me" not in parsed.netloc:
            raise ValueError("رابط غير تابع لتليجرام")

        if path_parts[0] == "c" and len(path_parts) >= 3:
            channel_id = int("-100" + path_parts[1])
            post_id = int(path_parts[2])
            entity = await client.get_entity(channel_id)
            channel_name = entity.title
        elif len(path_parts) >= 2:
            channel_username = path_parts[0]
            post_id = int(path_parts[1])
            entity = await client.get_entity(channel_username)
            channel_name = f"@{channel_username}"
        else:
            raise ValueError("صيغة الرابط غير صحيحة")

        message = await client.get_messages(entity, ids=post_id)

        if not message:
            await event.edit("**⚠️ لم يتم العثور على المنشور. قد لا يكون لديك صلاحية الوصول**")
            return

        caption = f"**⎉╎تم جلب المنشور من:** {channel_name}\n\n"
        if message.text:
            caption += message.text

        file_path = None

        try:
            if message.gif:
                file_path = await message.download_media()
                await client.send_file(
                    event.chat_id,
                    file_path,
                    caption=caption,
                    parse_mode='md'
                )
            elif message.media:
                file_path = await message.download_media()
                await client.send_file(
                    event.chat_id,
                    file_path,
                    caption=caption,
                    parse_mode='md',
                    supports_streaming=True
                )
            elif message.text:
                await event.respond(caption)
            else:
                await event.respond("**⚠️ لا يمكن حفظ هذا النوع من المحتوى**")
        finally:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)

        await event.delete()

    except ValueError as ve:
        await event.edit(f"**⚠️ الرابط غير صالح: {ve}**")
    except ChannelPrivateError:
        await event.edit("**⚠️ لا يمكن الوصول إلى القناة/المجموعة. قد تكون خاصة أو محظورة**")
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ: {str(e)}**")





@client.on(events.NewMessage(pattern=r'\.p\s+(.+)'))
async def get_crypto_price(event):
    crypto_input = event.pattern_match.group(1).strip().lower()
    await event.edit(f"**⎉╎جـارِ البحث عن {crypto_input}...**")

    try:
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": CMC_API_KEY
        }

        # الحصول على قائمة العملات من CoinMarketCap
        search_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code != 200:
            await event.edit("⚠️ فشل في الاتصال بـ CoinMarketCap.")
            return

        search_data = search_response.json()["data"]

        # مطابقة دقيقة
        best_match = None
        for coin in search_data:
            if crypto_input == coin['symbol'].lower() or crypto_input == coin['name'].lower() or crypto_input == coin['slug'].lower():
                best_match = coin
                break

        # إذا لم توجد نتيجة، اقترح DexScreener
        if not best_match:
            search_term = urllib.parse.quote(crypto_input)
            dexscreener_url = f"https://dexscreener.com/search?q={search_term}"
            await event.edit(
                f"⚠️ العملة '{crypto_input}' غير موجودة على CoinMarketCap.\n\n"
                f"🔎 **جرب البحث عنها هنا:** [DexScreener]({dexscreener_url})"
            )
            return

        # الحصول على بيانات السعر
        coin_id = best_match['id']
        symbol = best_match['symbol']
        name = best_match['name']

        detail_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={coin_id}"
        detail_response = requests.get(detail_url, headers=headers)
        if detail_response.status_code != 200:
            await event.edit("⚠️ فشل في جلب بيانات العملة.")
            return

        data = detail_response.json()['data'][str(coin_id)]['quote']['USD']
        current_price = data['price']
        price_change_24h = data['percent_change_24h']
        market_cap = data['market_cap']
        volume_24h = data['volume_24h']

        # تنسيق الأرقام
        def format_number(num):
            if num is None:
                return "N/A"
            if num >= 1_000_000_000:
                return f"${num/1_000_000_000:.2f}B"
            elif num >= 1_000_000:
                return f"${num/1_000_000:.2f}M"
            elif num >= 1_000:
                return f"${num/1_000:.1f}K"
            return f"${num:,.2f}"

        message = (
            f"**{name} ({symbol})**\n"
            f"**USD ${current_price:,.5f}**\n"
            f"**24H Change:** {price_change_24h:+.2f}%\n"
            f"**Market Cap:** {format_number(market_cap)}\n"
            f"**24H Volume:** {format_number(volume_24h)}\n\n"
            f"**⎉╎المصدر:** CoinMarketCap"
        )

        await event.edit(message)

    except Exception as e:
        await event.edit(f"⚠️ حدث خطأ: {str(e)}")


@client.on(events.NewMessage(pattern=r'\.احصائيات'))
async def show_stats(event):
    try:
        start_time = time.time()
        msg = await event.edit("**⎉╎جـاري حساب الإحصائيات... 0%**")
        
        dialogs = await client.get_dialogs()
        total_dialogs = len(dialogs)
        processed = 0
        
        channels = []
        groups = []
        bots = []
        private_chats = []
        admin_channels = 0
        admin_groups = 0
        
        for dialog in dialogs:
            entity = dialog.entity
            if isinstance(entity, types.Channel):
                if entity.broadcast:
                    channels.append(entity)
                    # التحقق من الإشراف بشكل دقيق
                    try:
                        if dialog.is_admin:
                            admin_channels += 1
                    except:
                        pass
                else:
                    groups.append(entity)
                    # التحقق من الإشراف بشكل دقيق
                    try:
                        if dialog.is_admin:
                            admin_groups += 1
                    except:
                        pass
            elif isinstance(entity, types.User):
                if entity.bot:
                    bots.append(entity)
                else:
                    private_chats.append(entity)
            
            processed += 1
            progress = int((processed / total_dialogs) * 100)
            if progress % 10 == 0:  # تحديث كل 10%
                remaining_time = (time.time() - start_time) * (100 - progress) / max(progress, 1)
                await msg.edit(f"**⎉╎جـاري حساب الإحصائيات... {progress}%\n⏳ المتبقي: {int(remaining_time)} ثانية**")
        
        stats_message = f"""
╭━━━┳━━━━╮
**⎉╎إحصائيات حسابك ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
**✾╎عدد القنوات:** {len(channels)}
**✾╎عدد القنوات المشرف عليها:** {admin_channels}
**✾╎عدد المجموعات:** {len(groups)}
**✾╎عدد المجموعات المشرف عليها:** {admin_groups}
**✾╎عدد البوتات:** {len(bots)}
**✾╎عدد المحادثات الخاصة:** {len(private_chats)}
**✾╎إجمالي الدردشات:** {total_dialogs}
**✾╎الوقت المستغرق:** {int(time.time() - start_time)} ثانية
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
"""
        await msg.edit(stats_message)
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ أثناء حساب الإحصائيات:** {str(e)}")

@client.on(events.NewMessage(pattern=r'\.مغادرة القنوات'))
async def leave_all_channels(event):
    try:
        start_time = time.time()
        msg = await event.edit("**⎉╎جاري جمع معلومات القنوات...**")
        
        dialogs = await client.get_dialogs()
        channels = [dialog for dialog in dialogs if 
                   isinstance(dialog.entity, types.Channel) and 
                   dialog.entity.broadcast]
        
        EXCEPTION_CHANNEL = "EREN_PYTHON"
        remaining_channels = []
        left_count = 0
        admin_channels = 0

        await msg.edit(f"**⎉╎تم العثور على {len(channels)} قناة، جاري التحقق...**")

        for i, dialog in enumerate(channels):
            entity = dialog.entity
            try:
                # التحقق من القناة المحمية
                if hasattr(entity, 'username') and entity.username == EXCEPTION_CHANNEL:
                    remaining_channels.append(entity)
                    continue
                    
                # التحقق من صلاحية الإشراف بشكل دقيق
                try:
                    participant = await client(GetParticipantRequest(
                        entity,
                        await client.get_me()
                    ))
                    if isinstance(participant.participant, (types.ChannelParticipantCreator, 
                                                          types.ChannelParticipantAdmin)):
                        admin_channels += 1
                        remaining_channels.append(entity)
                        continue
                except Exception:
                    pass
                    
                await client(LeaveChannelRequest(entity))
                left_count += 1
                
                if i % 5 == 0 or i == len(channels)-1:
                    await msg.edit(
                        f"**⎉╎جاري مغادرة القنوات...\n\n"
                        f"✾╎تم مغادرة: {left_count}\n"
                        f"✾╎قنوات مشرف عليها: {admin_channels}\n"
                        f"✾╎المتبقي: {len(channels)-i-1}**"
                    )
                
                await asyncio.sleep(2)  # زيادة وقت الانتظار لتجنب الحظر
                
            except Exception as e:
                print(f"Error in channel {entity.id}: {str(e)}")
                remaining_channels.append(entity)
        
        result_message = f"""
╭━━━┳━━━━╮
**⎉╎نتيجة مغادرة القنوات ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
**✾╎عدد القنوات التي غادرتها:** {left_count}
**✾╎عدد القنوات المشرف عليها:** {admin_channels}
**✾╎عدد القنوات المتبقية:** {len(remaining_channels)}
**✾╎القناة المحمية:** @{EXCEPTION_CHANNEL}
**✾╎الوقت المستغرق:** {int(time.time() - start_time)} ثانية
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
"""
        await msg.edit(result_message)
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ أثناء مغادرة القنوات:** {str(e)}")

@client.on(events.NewMessage(pattern=r'\.مغادرة الجروبات'))
async def leave_all_groups(event):
    try:
        start_time = time.time()
        msg = await event.edit("**⎉╎جاري جمع معلومات الجروبات...**")
        
        dialogs = await client.get_dialogs()
        groups = [dialog for dialog in dialogs if 
                 isinstance(dialog.entity, types.Channel) and 
                 not dialog.entity.broadcast]
        
        left_count = 0
        remaining_groups = []
        admin_groups = 0

        await msg.edit(f"**⎉╎تم العثور على {len(groups)} مجموعة، جاري التحقق...**")

        for i, dialog in enumerate(groups):
            entity = dialog.entity
            try:
                # التحقق من صلاحية الإشراف بشكل دقيق
                try:
                    participant = await client(GetParticipantRequest(
                        entity,
                        await client.get_me()
                    ))
                    if isinstance(participant.participant, (types.ChannelParticipantCreator, 
                                                          types.ChannelParticipantAdmin)):
                        admin_groups += 1
                        remaining_groups.append(entity)
                        continue
                except Exception:
                    pass
                    
                await client(LeaveChannelRequest(entity))
                left_count += 1
                
                if i % 5 == 0 or i == len(groups)-1:
                    await msg.edit(
                        f"**⎉╎جاري مغادرة الجروبات...\n\n"
                        f"✾╎تم مغادرة: {left_count}\n"
                        f"✾╎جروبات مشرف عليها: {admin_groups}\n"
                        f"✾╎المتبقي: {len(groups)-i-1}**"
                    )
                
                await asyncio.sleep(2)  # زيادة وقت الانتظار لتجنب الحظر
                
            except Exception as e:
                print(f"Error in group {entity.id}: {str(e)}")
                remaining_groups.append(entity)
        
        result_message = f"""
╭━━━┳━━━━╮
**⎉╎نتيجة مغادرة الجروبات ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
**✾╎عدد الجروبات التي غادرتها:** {left_count}
**✾╎عدد الجروبات المشرف عليها:** {admin_groups}
**✾╎عدد الجروبات المتبقية:** {len(remaining_groups)}
**✾╎الوقت المستغرق:** {int(time.time() - start_time)} ثانية
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
"""
        await msg.edit(result_message)
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ أثناء مغادرة الجروبات:** {str(e)}")
 
@client.on(events.NewMessage(pattern=r'\.حذف البوتات'))
async def delete_all_bots(event):
    try:
        start_time = time.time()
        msg = await event.edit("**⎉╎جاري البحث عن البوتات...**")
        
        dialogs = await client.get_dialogs()
        bots = [dialog for dialog in dialogs 
               if isinstance(dialog.entity, User) 
               and dialog.entity.bot]
        
        deleted_count = 0
        failed_count = 0
        total_bots = len(bots)

        await msg.edit(f"**⎉╎تم العثور على {total_bots} بوت، جاري الحذف...**")

        for i, dialog in enumerate(bots):
            try:
                await client.delete_dialog(dialog.entity)
                deleted_count += 1
                
                if i % 5 == 0 or i == total_bots - 1:
                    progress = f"**⎉╎جاري حذف البوتات...\n\n"
                    progress += f"✾╎تم حذف: {deleted_count}/{total_bots}\n"
                    progress += f"✾╎فشل في حذف: {failed_count}\n"
                    progress += f"⏳ المتبقي: {total_bots - i - 1}**"
                    await msg.edit(progress)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error deleting bot {dialog.entity.id}: {str(e)}")
                failed_count += 1
                continue
        
        result_message = f"""
╭━━━┳━━━━╮
**⎉╎نتيجة حذف البوتات ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
**✾╎عدد البوتات التي تم حذفها:** {deleted_count}
**✾╎عدد البوتات التي فشل حذفها:** {failed_count}
**✾╎إجمالي البوتات المكتشفة:** {total_bots}
**✾╎الوقت المستغرق:** {int(time.time() - start_time)} ثانية
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
"""
        await msg.edit(result_message)
                
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ أثناء حذف البوتات:** {str(e)}") 
        



@client.on(events.NewMessage(pattern=r'\.ستوريات(?:\s+(.+))?$'))
async def download_stories(event):
    # الحصول على المعرف من الرسالة أو الرد
    input_arg = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message()
    
    if not input_arg and not reply_msg:
        await event.edit("**⚠️ يرجى تحديد المستخدم (معرف، آيدي، أو رابط) أو الرد على رسالة تحتوي عليها**")
        return
    
    # استخراج المعرف من المدخلات
    target = input_arg if input_arg else reply_msg.text
    target = target.strip()
    
    await event.edit("**🔍 جاري البحث عن المستخدم...**")
    
    try:
        # محاولة الحصول على كيان المستخدم
        if target.isdigit():
            user = await client.get_entity(InputPeerUser(int(target), 0))
        else:
            # إزالة @ من اليوزرنيم إن وجد
            if target.startswith('@'):
                target = target[1:]
            # استخراج اليوزرنيم من الروابط
            if 't.me/' in target:
                target = target.split('t.me/')[-1].split('/')[0]
            user = await client.get_entity(target)
            
        await event.edit(f"**📥 جاري جلب استوريات @{user.username}...**")
        
        # إنشاء مجلد لحفظ الاستوريات
        folder_name = f"stories_{user.id}_{datetime.now().strftime('%Y%m%d')}"
        os.makedirs(folder_name, exist_ok=True)
        
        # استرداد الاستوريات باستخدام GetStoriesArchiveRequest
        stories = await client(GetStoriesArchiveRequest(
            offset_id=0,
            limit=100,
            peer=user
        ))
        
        if not stories.stories:
            await event.edit("**❌ لا توجد استوريات متاحة لهذا المستخدم**")
            return
            
        total_stories = len(stories.stories)
        downloaded_count = 0
        failed_count = 0
        
        await event.edit(f"**⏳ جاري تحميل {total_stories} استوري...**")
        
        for i, story in enumerate(stories.stories, 1):
            try:
                if hasattr(story, 'media'):
                    file_ext = '.jpg' if isinstance(story.media, types.MessageMediaPhoto) else '.mp4'
                    file_name = f"{folder_name}/story_{story.id}_{i}{file_ext}"
                    await client.download_media(story.media, file=file_name)
                    downloaded_count += 1
                    
                if i % 5 == 0:
                    await event.edit(f"**📥 جاري التحميل... {i}/{total_stories}**")
                    
            except Exception as e:
                print(f"خطأ في تحميل الاستوري {story.id}: {str(e)}")
                failed_count += 1
                continue
        
        # النتيجة النهائية
        result_msg = f"""
✅ **تم الانتهاء من التحميل!**
📂 **المجلد:** `{folder_name}`
📊 **العدد الكلي:** {total_stories}
📥 **المحملة:** {downloaded_count}
❌ **الفاشلة:** {failed_count}
        """
        await event.edit(result_msg)
        
    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ: {str(e)}**")
        
def run_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        print("Serving on port 8000")
        httpd.serve_forever()

# تشغيل الخادم في خيط جديد
server_thread = threading.Thread(target=run_server)
server_thread.start()                
                                              
async def main():
    await start_client()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())