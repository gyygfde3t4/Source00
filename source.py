# ========== المكتبات القياسية ==========
import os
import re
import time
import html
import base64
import asyncio
import random
import logging
import traceback
import subprocess
import webbrowser
import urllib.parse
import json
import http.server
import socketserver
import threading
from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional
from urllib.parse import urlparse, quote
from difflib import SequenceMatcher
import io  
import subprocess
from PIL import Image
from pydub import AudioSegment
import hashlib

# ========== مكتبات HTTP وطلبات الويب ==========
import requests
import httpx
import aiohttp

# ========== مكتبات الجهات الخارجية ==========
import pytz
from PIL import Image, ImageDraw, ImageFont
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from googletrans import Translator
from deep_translator import GoogleTranslator

# ========== Telethon - استيراد رئيسي ==========
from telethon import TelegramClient, events, functions, types, Button
from telethon.sessions import StringSession
from telethon.tl.types import DocumentAttributeAnimated, DocumentAttributeAudio

# ========== Telethon - الأخطاء ==========
from telethon.errors import (
    SessionPasswordNeededError,
    ChannelPrivateError,
    FileReferenceExpiredError,
    RPCError
)

# ========== Telethon - دوال API ==========
from telethon.tl.functions import (
    account,
    photos,
    messages,
    contacts,
    channels
)
from telethon.tl.functions.channels import (
    JoinChannelRequest,
    LeaveChannelRequest,
    GetFullChannelRequest,
    GetParticipantRequest
)
from telethon.tl.functions.messages import (
    SendMessageRequest,
    SendMediaRequest,
    DeleteChatUserRequest,
    DeleteMessagesRequest
)
from telethon.tl.functions.contacts import BlockRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.stories import GetStoriesArchiveRequest
from telethon import functions, types, events
from telethon.tl.functions.phone import GetCallConfigRequest
from telethon.errors import UserPrivacyRestrictedError

# ========== Telethon - الأنواع ==========
from telethon.tl.types import (
    User,
    Channel,
    InputPeerSelf,
    InputPeerUser,
    InputPeerChannel,
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    MessageMediaPhoto,
    InputMediaPhoto,
    InputMediaDocument,
    MessageEntityBold,
    MessageEntityCode,
    MessageEntityItalic,
    MessageEntityPre,
    MessageEntityTextUrl,
    DocumentAttributeVideo
)


API_ID = int(os.getenv('API_ID')) # أدخل الـ API_ID الخاص بك
API_HASH = os.getenv('API_HASH') # أدخل الـ API_HASH الخاص بك

# ========== المستخدمون المصرح لهم ==========
AUTHORIZED_USERS = [
    int(uid.strip()) for uid in os.getenv("AUTHORIZED_USERS", "").split(",") if uid.strip().isdigit()
]

STRING_SESSION = os.getenv('STRING_SESSION') #اضف سيشن 

# ========== إعدادات البوت ==========
bot_username = os.getenv("bot_username")

# ========== مفاتيح Hugging Face ==========
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL")

# ========== إعدادات الذكاء الاصطناعي ==========
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GPT_MODEL = os.getenv("GPT_MODEL")

# --- إعدادات الأداء للذكاء الاصطناعي ---
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 60))  # عدد الثواني قبل انتهاء المهلة
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))           # عدد المحاولات في حال الفشل
DELAY_BETWEEN_RETRIES = int(os.getenv("DELAY_BETWEEN_RETRIES", 2))  # تأخير بين المحاولات (بالثواني)

# ========== مفتاح فحص الملفات (VirusTotal) ==========
VIRUSTOTAL_API = os.getenv("VIRUSTOTAL_API")

# ========== API الطقس (OpenWeatherMap) ==========
OPENWEATHER_API = os.getenv("OPENWEATHER_API")

# ========== مفتاح CoinMarketCap ==========
CMC_API_KEY = os.getenv("CMC_API_KEY")


# ========== حالات النظام ==========
protection_enabled = False  #حالة الحماية

is_auto_saving = False  # حالة الحفظ التلقائي

# ========== إعدادات عامة ==========
MAX_WARNINGS = 7  # الحد الأقصى لعدد التحذيرات قبل اتخاذ إجراء

# ========== قوائم الرقابة والإشراف ==========
accepted_users     = {}      # المستخدمون الذين تم قبولهم
warned_users       = {}      # المستخدمون الذين تم تحذيرهم
muted_users        = set()   # المستخدمون المكتومون

# ========== ألعاب الأرقام ==========
number_games             = {}     # تخزين جلسات ألعاب الأرقام
number_character_pool    = []     # قائمة شخصيات الأرقام
current_number_pool_index = 0     # مؤشر الدور الحالي في قائمة شخصيات الأرقام

# ========== ألعاب الأنمي ==========
anime_games           = {}     # جلسات ألعاب تخمين الأنمي
used_characters       = set()  # الشخصيات التي تم استخدامها لتجنب التكرار
character_pool        = []     # مجموعة الشخصيات المتاحة
current_pool_index    = 0      # مؤشر الدور الحالي في مجموعة الشخصيات
message_locks = defaultdict(asyncio.Lock)  # إضافة locks لمنع race conditions
processing_messages = set()  # تتبع الرسائل قيد المعالجة

# ========== ألعاب الألغاز ==========
riddle_games = {}  # تخزين جلسات ألعاب الألغاز

# ========== إدارة الأدوار والمؤقتات ==========
games             = {}     # تخزين معلومات جميع الألعاب الجارية
waiting_for_range = {}     # المستخدمون الذين في انتظار تحديد النطاق
turn_timers       = {}     # مؤقتات الأدوار
active_games      = {}     # الألعاب النشطة حاليًا

# ========== المترجم ==========
translator = Translator()  # تهيئة المترجم (من مكتبة googletrans أو مشابه)

monitored_channels = {}  # {channel_id: {'username': str, 'keywords': [str], 'name': str}}
target_users = []  # قائمة المستهدفين
monitoring_active = False
current_calls = {}
MAX_TARGETS = 5  # الحد الأقصى للمستهدفين

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


@client.on(events.NewMessage(pattern=r'^\.اوامري$'))
async def show_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهلاً بك فـي قـائمة الأوامـر الـخاصة بسـورس إيــريــن** ⎚
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.م1` - **أوامر الحساب** ☆
2- ☆ `.م2` - **أوامر الاسم الوقتي** ☆
3- ☆ `.م3` - **أوامر البحث والتحميل** ☆
4- ☆ `.م4` - **أوامر الألعاب والفكاهية** ☆
5- ☆ `.م5` - **أوامر الذكاء الاصطناعي** ☆
6- ☆ `.م6` - **أوامر الذاتية** ☆
7- ☆ `.م7` - **أوامر الميديا والصيغ** ☆
8- ☆ `.م8` - **أوامر الحماية والتحكم** ☆
9- ☆ `.م9` - **أوامر القنوات والمجموعات** ☆
10- ☆ `.م10` - **أوامر التخزين والترجمة** ☆
11- ☆ `.م11` - **أوامر إضافية** ☆
12- ☆ `.م12` - **أوامر العملات والتحليل** ☆
13- ☆ `.م13` - **أوامر بوت دعمكم** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م1$'))
async def show_account_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهـلاً بك فـي قـائمة الحساب الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.ايدي` - **عرض معلومات المستخدم** ☆
2- ☆ `.تلجراف` - **رفع الصور إلى تلجراف** ☆
3- ☆ `.كتم` - **كتم المستخدم** ☆
4- ☆ `.الغاء كتم` - **إلغاء كتم المستخدم** ☆
5- ☆ `.المكتومين` - **عرض قائمة المكتومين** ☆
6- ☆ `.بلوك` - **حظر المستخدم** ☆
7- ☆ `.لصوره` - **تحويل ملصق إلى صورة** ☆
8- ☆ `.فحص` - **فحص البوت** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م2$'))
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

@client.on(events.NewMessage(pattern=r'^\.م3$'))
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

@client.on(events.NewMessage(pattern=r'^\.م4$'))
async def show_games_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الألعاب والفكاهية الـخاصة بسـورس إيــريــن ⎚**
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
9- ☆ `.تخمين رقم` - **لعبة تخمين الرقم** ☆
10- ☆ `.لغز` - **لعبة الألغاز** ☆
11- ☆ `.تخمين انمي` - **لعبة تخمين شخصية الأنمي** ☆
12- ☆ `.قتل` + اسم - **لعبة قتل (فكاهي)** ☆
13- ☆ `.قاتل` + اسم - **لعبة قتل متقدمة (فكاهي)** ☆
14- ☆ `.تهكير` - **محاكاة عملية تهكير (فكاهي)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م5$'))
async def show_ai_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الذكاء الاصطناعي الـخاصة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.س` + سؤال - **سؤال الذكاء الاصطناعي** ☆
2- ☆ `.إنشاء صورة` + وصف - **إنشاء صورة بالذكاء الاصطناعي** ☆
3- ☆ `.تعديل صورة` + وصف - **تعديل الصورة بالرد (بالذكاء الاصطناعي)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م6$'))
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

@client.on(events.NewMessage(pattern=r'^\.م7$'))
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
5- ☆ `.ستوريات` - **تحميل استوريات مستخدم (بالرد أو معرف)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م8$'))
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
8- ☆ `.احصائيات` - **عرض إحصائيات الحساب** ☆
9- ☆ `.حذف البوتات` - **حذف جميع محادثات البوتات** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م9$'))
async def show_channels_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة إدارة القنـوات والمجموعات ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.انضم` + رابط - **الانضمام لقناة/مجموعة** ☆
2- ☆ `.غادر` + رابط - **مغادرة قناة/مجموعة** ☆
3- ☆ `.مغادرة القنوات` - **مغادرة جميع القنوات** ☆
4- ☆ `.مغادرة الجروبات` - **مغادرة جميع المجموعات** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م10$'))
async def show_storage_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة التخزين والترجمة ⎚**
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

@client.on(events.NewMessage(pattern=r'^\.م11$'))
async def show_additional_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة الأوامـر الإضافيـة بسـورس إيــريــن ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.مدينة` - **رسم مدينة** ☆
2- ☆ `.حفظ` - **حفظ منشور من قناة/مجموعة (بالرد على الرابط)** ☆
3- ☆ `.انمي` - **عرض شخصية أنمي عشوائية** ☆
4- ☆ `.معرفة الانمي` - **التعرف على مشهد أنمي (بالرد على صورة)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م12$'))
async def show_crypto_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة العملات والتحليل ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.p` + عملة - **عرض سعر العملة الرقمية** ☆
2- ☆ `.فلور` + رابط - **تحليل NFT من تيليجرام** ☆
3- ☆ `.تحليل` + رابط - **فحص الرابط على VirusTotal** ☆
4- ☆ `.طقس` + مدينة - **عرض حالة الطقس** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    await event.edit(commands_message)

@client.on(events.NewMessage(pattern=r'^\.م13$'))
async def show_daamkom_commands(event):
    commands_message = """
╭━━━┳━━━━╮
**أهــلاً بك فـي قـائمة أوامـر بوت دعمكـم ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
1- ☆ `.دعمكم` - **تجميع نقاط بوت دعمكم** ☆
2- ☆ `.ايقاف دعمكم` - **إيقاف التجميع** ☆
3- ☆ `.لانهائي دعمكم` - **تجميع لانهائي** ☆
4- ☆ `.نقاط دعمكم` - **عرض النقاط** ☆
5- ☆ `.هدية دعمكم` - **تجميع الهدية** ☆
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
@client.on(events.NewMessage(pattern=r'^\.الاسم التلقائي$'))
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
           
@client.on(events.NewMessage(pattern=r'^\.وقتيه1$'))
async def activate_style1(event):
    await activate_style(event, 'style1', '𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡')

@client.on(events.NewMessage(pattern=r'^\.وقتيه2$'))
async def activate_style2(event):
    await activate_style(event, 'style2', '⓪➀➁➂➃➄➅➆➇➈')

@client.on(events.NewMessage(pattern=r'^\.وقتيه3$'))
async def activate_style3(event):
    await activate_style(event, 'style3', '⓿➊➋➌➍➎➏➐➑➒')

# الأمر لإيقاف الاسم التلقائي
@client.on(events.NewMessage(pattern=r'^\.ايقاف الاسم التلقائي$'))
async def stop_timed_update(event):
    global timed_update_running
    if timed_update_running:
        timed_update_running = False
        await event.edit("⛔ تم إيقاف الاسم التلقائي بنجاح.")
    else:
        await event.edit("**⚠️ لا يوجد تحديث تلقائي للاسم مفعّل.**")
  	    

@client.on(events.NewMessage(pattern=r'^\.ايدي$'))
async def show_user_info(event):
    if event.reply_to_msg_id:
        reply_message = await client.get_messages(event.chat_id, ids=event.reply_to_msg_id)
        if reply_message.sender_id:
            user = await client.get_entity(reply_message.sender_id)

            await event.edit("**جاري عرض المعلومات . . .**")

            user_photo_path = 'user_photo.jpg'
            
            # تحميل صورة البروفايل
            await client.download_profile_photo(user.id, file=user_photo_path)
            
            # جمع المعلومات الأساسية
            user_id = user.id
            username = user.username if user.username else "غير متوفر"
            user_name = user.first_name or "غير متوفر"

            # إصلاح مشكلة البايو
            bio = "لا يوجد"
            try:
                from telethon.tl import functions
                user_full = await client(functions.users.GetFullUserRequest(user.id))
                if user_full.full_user.about:
                    bio = user_full.full_user.about
            except:
                bio = "لا يوجد"

            # تحديد الرتبة
            if user_id == 5683930416:
                rank = "مطـور السـورس 𓄂"
            else:
                rank = "مميز"

            # فحص البريميوم
            account_type = "بريميوم" if getattr(user, 'premium', False) else "عادي"

            # عدد الصور
            try:
                photos = await client(GetUserPhotosRequest(user.id, offset=0, max_id=0, limit=100))
                num_photos = len(photos.photos)
            except:
                num_photos = "غير معروف"

            # الهدايا والمقتنيات
            gifts = "غير معروف"
            collectibles = "غير معروف"

            # حساب عدد الرسائل بدقة - طرق متعددة للحصول على العدد الصحيح
            messages_count = 0
            try:
                # الطريقة الأولى: استخدام البحث للحصول على العدد الإجمالي
                from telethon.tl.functions.messages import SearchRequest
                from telethon.tl.types import InputMessagesFilterEmpty
                
                search_result = await client(SearchRequest(
                    peer=event.chat_id,
                    q='',
                    from_id=user.id,
                    filter=InputMessagesFilterEmpty(),
                    min_date=None,
                    max_date=None,
                    offset_id=0,
                    add_offset=0,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                
                if hasattr(search_result, 'count'):
                    messages_count = search_result.count
                else:
                    raise Exception("البحث لم يعطي عدد")
                    
            except:
                try:
                    # الطريقة الثانية: العد التدريجي
                    messages_count = 0
                    last_id = 0
                    
                    while True:
                        messages = await client.get_messages(
                            event.chat_id, 
                            from_user=user.id, 
                            limit=100,
                            max_id=last_id if last_id > 0 else None
                        )
                        
                        if not messages:
                            break
                            
                        messages_count += len(messages)
                        
                        # إذا حصلنا على أقل من 100 رسالة، فهذا يعني أننا وصلنا للنهاية
                        if len(messages) < 100:
                            break
                            
                        last_id = messages[-1].id
                        
                        # حد أقصى لتجنب التأخير الطويل
                        if messages_count > 10000:
                            messages_count = f"{messages_count}+"
                            break
                            
                except:
                    # الطريقة الثالثة: تقدير بسيط
                    try:
                        recent_messages = await client.get_messages(event.chat_id, from_user=user.id, limit=100)
                        messages_count = len(recent_messages)
                        if messages_count == 100:
                            messages_count = "100+"
                    except:
                        messages_count = 0

            # تحديد التفاعل
            if isinstance(messages_count, int):
                interaction = "نار وشرار" if messages_count >= 1000 else "ضعيف"
            elif isinstance(messages_count, str) and "+" in messages_count:
                interaction = "نار وشرار"
            else:
                interaction = "ضعيف"

            # إصلاح مشكلة تاريخ الإنشاء - استخدام seed ثابت لنفس المستخدم
            import random
            random.seed(user_id)  # استخدام معرف المستخدم كـ seed لضمان نفس النتيجة دائماً
            
            try:
                if user_id < 10000:
                    year = "2013"
                    month = random.randint(1, 6)
                    day = random.randint(1, 28)
                elif user_id < 100000:
                    year = "2014"
                    month = random.randint(1, 8)
                    day = random.randint(1, 28)
                elif user_id < 1000000:
                    year = "2015"
                    month = random.randint(1, 10)
                    day = random.randint(1, 28)
                elif user_id < 10000000:
                    year = "2016"
                    month = random.randint(2, 12)
                    day = random.randint(1, 28)
                elif user_id < 100000000:
                    year = "2017"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 500000000:
                    year = "2018"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 1000000000:
                    year = "2019"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 1500000000:
                    year = "2020"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 2000000000:
                    year = "2021"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 5000000000:
                    year = "2022"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                elif user_id < 6000000000:
                    year = "2023"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                else:
                    year = "2024"
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                
                creation_date = f"{day}/{month}/{year}"
            except:
                creation_date = "غير معروف"

            # تكوين رسالة المعلومات بالكليشة الجديدة مع تنسيق الاقتباس
            user_info_message = (
                f"> •⎚• مـعلومـات المسـتخـدم سـورس إيــريــن\n"
                f"> ٴ⋆┄─┄─┄─┄─┄─┄─┄─┄─┄─┄⋆\n"
                f"> ✦ الاســم    ⤎ `{user_name}`\n"
                f"> ✦ اليـوزر    ⤎ @{username}\n"
                f"> ✦ الايـدي    ⤎ `{user_id}`\n"
                f"> ✦ الرتبــه    ⤎ {rank}\n"
                f"> ✦ الحساب  ⤎ {account_type}\n"
                f"> ✦ الصـور    ⤎ {num_photos}\n"
                f"> ✦ الهدايا    ⤎ {gifts}\n"
                f"> ✦ مقتنيات ⤎ {collectibles}\n"
                f"> ✦ الرسائل  ⤎ {messages_count}\n"
                f"> ✦ التفاعل  ⤎ {interaction}\n"
                f"> ✦ الإنشـاء  ⤎ {creation_date}\n"
                f"> ✦ البايـو     ⤎ {bio}\n"
                f"> ٴ⋆┄─┄─┄─┄─┄─┄─┄─┄─┄─┄⋆"
            )

            await client.send_file(event.chat_id, user_photo_path, caption=user_info_message)
            await event.delete()
            
            # حذف الصورة بأمان
            try:
                import os
                os.remove(user_photo_path)
            except:
                pass
        else:
            await event.edit("**⚠️ لم أتمكن من العثور على معلومات عن هذا المستخدم.**")
    else:
        await event.edit("**⚠️ يرجى الرد على رسالة المستخدم للحصول على معلوماته.**")

async def upload_to_telegraph(image_path):
    try:
        response = telegraph.upload_file(image_path)
        return 'https://telegra.ph' + response[0]
    except Exception as e:
        print(f"خطأ أثناء رفع الصورة: {e}")
        return None
        
# إضافة أمر .بل
@client.on(events.NewMessage(pattern=r'^\.بلوك$'))
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
        

@client.on(events.NewMessage(pattern=r'^\.حذف$'))
async def delete_message(event):
    if event.reply_to_msg_id:
        await client.delete_messages(event.chat_id, message_ids=[event.reply_to_msg_id])
        await event.delete()
    else:
        await event.edit("⚠️ يرجى الرد على الرسالة التي تريد حذفها.")

@client.on(events.NewMessage(pattern=r'^\.التوقيت$'))
async def show_timezones(event):
    timezone_message = (
        "**🌍 قائمة التوقيتات:**\n\n"
        "1. `.وقت مصر` 🇪🇬 - تفعيل التوقيت الخاص بمصر.\n"
        "2. `.وقت سوريا` 🇸🇾 - تفعيل التوقيت الخاص بسوريا.\n"
        "3. `.وقت العراق` 🇮🇶 - تفعيل التوقيت الخاص بالعراق.\n"
        "4. `.وقت اليمن` 🇾🇪 - تفعيل التوقيت الخاص باليمن.\n"
    )
    
    await event.edit(timezone_message)

@client.on(events.NewMessage(pattern=r'^\.وقت مصر$'))
async def set_time_egypt(event):
    global current_timezone
    current_timezone = 'Africa/Cairo'
    await event.edit("تم تفعيل وقت مصر بنجاح ✅")

@client.on(events.NewMessage(pattern=r'^\.وقت سوريا$'))
async def set_time_syria(event):
    global current_timezone
    current_timezone = 'Asia/Damascus'
    await event.edit("تم تفعيل وقت سوريا بنجاح ✅")

@client.on(events.NewMessage(pattern=r'^\.وقت العراق$'))
async def set_time_iraq(event):
    global current_timezone
    current_timezone = 'Asia/Baghdad'
    await event.edit("تم تفعيل وقت العراق بنجاح ✅")

@client.on(events.NewMessage(pattern=r'^\.وقت اليمن$'))
async def set_time_yemen(event):
    global current_timezone
    current_timezone = 'Asia/Aden'
    await event.edit("تم تفعيل وقت اليمن بنجاح ✅")
    
@client.on(events.NewMessage(pattern=r'^\.تسلية$'))
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
   


@client.on(events.NewMessage(pattern=r'^\.مسدس$'))
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

@client.on(events.NewMessage(pattern=r'^\.كلب$'))
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

@client.on(events.NewMessage(pattern=r'^\.سبونج بوب$'))
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

@client.on(events.NewMessage(pattern=r'^\.إبرة$'))
async def draw_needle(event):
    needle_art = (
        "────▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀█─█\n"
        "▀▀▀▀▄─█─█─█─█─█─█──█▀█\n"
        "─────▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀─▀\n"
        "\n🚹 ╎ تنح واخذ الابره عزيزي 👨🏻‍⚕🤭😂"
    )
    await event.edit(needle_art)

@client.on(events.NewMessage(pattern=r'^\.وحش$'))
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

@client.on(events.NewMessage(pattern=r'^\.مدينة$'))
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

@client.on(events.NewMessage(pattern=r'^\.مروحية$'))
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

                                                                            
# أمر كتم المستخدم
@client.on(events.NewMessage(pattern=r'^\.كتم$'))
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
@client.on(events.NewMessage(pattern=r'^\.الغاء الكتم$'))
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
@client.on(events.NewMessage(pattern=r'^\.المكتومين$'))
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




async def get_ai_response(client: httpx.AsyncClient, prompt: str) -> Optional[str]:
    """الحصول على رد من OpenRouter API مع الحفاظ على التنسيق"""
    if not prompt.strip():
        return None
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/YourBotName",
        "X-Title": "AI Telegram Bot",
    }
    
    messages = [{"role": "user", "content": prompt}]
    
    payload = {
        "model": GPT_MODEL,
        "messages": messages,
        "temperature": 0.7,
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = await client.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", "Unknown error")
                if attempt == MAX_RETRIES - 1:
                    return f"❌ خطأ من OpenRouter (كود {response.status_code}): {error_msg}"
                await asyncio.sleep(DELAY_BETWEEN_RETRIES)
                
        except httpx.ReadTimeout:
            if attempt == MAX_RETRIES - 1:
                return "⌛ انتهى وقت الانتظار. الخادم يستغرق وقتًا أطول من المعتاد."
            await asyncio.sleep(DELAY_BETWEEN_RETRIES)
            
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                return f"⚠️ خطأ غير متوقع: {str(e)}"
            await asyncio.sleep(DELAY_BETWEEN_RETRIES)
    
    return "❌ فشلت جميع محاولات الاتصال بالخادم."

async def parse_markdown_to_entities(text: str):
    """تحويل Markdown إلى كيانات تليجرام (للتنسيق)"""
    entities = []
    stack = []
    i = 0
    n = len(text)
    
    while i < n:
        if text.startswith('**', i):
            if stack and stack[-1] == 'bold':
                start = stack.pop()
                entities.append(MessageEntityBold(i - 2, 2))
            else:
                stack.append('bold')
                entities.append(MessageEntityBold(i, 2))
            i += 2
        elif text.startswith('*', i) and not text.startswith('**', i):
            if stack and stack[-1] == 'italic':
                start = stack.pop()
                entities.append(MessageEntityItalic(i - 1, 1))
            else:
                stack.append('italic')
                entities.append(MessageEntityItalic(i, 1))
            i += 1
        elif text.startswith('`', i):
            if stack and stack[-1] == 'code':
                start = stack.pop()
                entities.append(MessageEntityCode(i - 1, 1))
            else:
                stack.append('code')
                entities.append(MessageEntityCode(i, 1))
            i += 1
        else:
            i += 1
    
    return entities

@client.on(events.NewMessage(pattern=r'^\.س\s+(.+)$'))
async def handle_ai_command(event):
    parts = event.message.text.split(maxsplit=1)
    if len(parts) < 2:
        await event.reply("⚠️ يرجى إدخال السؤال بعد الأمر .س")
        return

    question = parts[1]

    # إرسال رسالة "⏳ GPT-4o يعمل على طلبك. يرجى الانتظار لحظة . . ."
    processing_message = await event.edit("**⏳ D𝑒𝑒𝑝S𝑒𝑒𝑘 يعمل على طلبك. يرجى الانتظار لحظة. . .**")

    try:
        async with httpx.AsyncClient() as client:
            response = await get_ai_response(client, question)
            
            if response:
                await processing_message.delete()
                
                # تحويل التنسيق Markdown إلى كيانات تليجرام
                try:
                    entities = await parse_markdown_to_entities(response)
                    await event.reply(response, formatting_entities=entities)
                except Exception as e:
                    print(f"Error parsing markdown: {e}")
                    # إذا فشل التحليل، إرسال الرسالة بدون تنسيق
                    await event.reply(f"الإجابة:\n{response}")
            else:
                await processing_message.edit("⚠️ لم أستطع الحصول على رد. يرجى المحاولة مرة أخرى.")
                
    except Exception as e:
        await processing_message.delete()
        await event.reply(f"⚠️ حدث خطأ: {str(e)}")

@client.on(events.NewMessage(pattern=r'^\.تلجراف$'))
async def handle_telegraph_command(event):
    # تحقق من وجود رد على رسالة
    if not event.is_reply:
        await event.edit("⚠️ يرجى الرد على صورة لتحميلها.")
        return

    replied_message = await event.get_reply_message()

    # تحقق من أن الرسالة تحتوي على وسائط
    if not replied_message.media:
        await event.edit("⚠️ يرجى الرد على صورة فقط.")
        return

    # إرسال رسالة معالجة مؤقتة
    processing_message = await event.edit("⏳ جاري معالجة الصورة...")

    file_path = 'temp_image.jpg'

    try:
        # تنزيل الصورة
        await replied_message.download_media(file_path)

        # رفع الصورة إلى Catbox
        with open(file_path, "rb") as img_file:
            response = requests.post(
                "https://catbox.moe/user/api.php",
                data={"reqtype": "fileupload"},
                files={"fileToUpload": img_file}
            )

        # حذف رسالة المعالجة
        await processing_message.delete()

        # التحقق من نجاح الرفع
        if response.status_code == 200 and "catbox.moe" in response.text:
            catbox_url = response.text.strip()
            await event.reply(f"✅ تم رفع الصورة بنجاح!\n📎 الرابط: {catbox_url}")
        else:
            await event.edit("⚠️ فشل في رفع الصورة. حاول لاحقًا.")

    except Exception as e:
        await processing_message.delete()
        await event.edit(f"⚠️ حدث خطأ أثناء المعالجة:\n`{str(e)}`")

    finally:
        # حذف الملف المؤقت إذا كان موجودًا
        if os.path.exists(file_path):
            os.remove(file_path)  


# ✅ أمر يدوي لحفظ وسائط ذاتية عبر الرد
@client.on(events.NewMessage(pattern=r'^\.ذاتيه$', func=lambda e: e.is_reply))
async def manual_self_destruct_save(event):
    reply = await event.get_reply_message()

    # تحقق من أن الوسائط ذاتية التدمير
    if not reply or not reply.media or not getattr(reply.media, 'ttl_seconds', None):
        await event.respond("⚠️ يجب الرد على صورة أو فيديو ذاتي التدمير فقط.")
        return

    try:
        # حذف أمر المستخدم أولاً
        await event.delete()
        
        # تحميل الملف
        file = await client.download_media(reply, file="temp_media_file")
        me = await client.get_me()

        # إرسال الملف المحفوظ
        await client.send_file(
            "me",
            file,
            caption="✅ تم حفظ الوسائط ذاتية التدمير بنجاح.\n\n⚠️ يُرجى استخدامها بشكل مسؤول."
        )

    except FileReferenceExpiredError:
        await event.respond("⚠️ الوسائط منتهية الصلاحية ولا يمكن تحميلها.")
    except RPCError as e:
        await event.respond(f"❌ خطأ أثناء الحفظ:\n{e}")
    except Exception as e:
        await event.respond(f"❌ حدث خطأ غير متوقع:\n{e}")
    finally:
        if os.path.exists("temp_media_file"):
            os.remove("temp_media_file")


# ✅ تشغيل الحفظ التلقائي
@client.on(events.NewMessage(pattern=r'^\.الذاتيه تشغيل$'))
async def enable_auto_saving(event):
    global is_auto_saving
    is_auto_saving = True
    msg = await event.edit("✅ تم تفعيل الحفظ التلقائي للوسائط الذاتية.")
    await asyncio.sleep(3)
    await msg.delete()


# ✅ إيقاف الحفظ التلقائي
@client.on(events.NewMessage(pattern=r'^\.الذاتيه ايقاف$'))
async def disable_auto_saving(event):
    global is_auto_saving
    is_auto_saving = False
    msg = await event.edit("❌ تم إيقاف الحفظ التلقائي.")
    await asyncio.sleep(3)
    await msg.delete()


# ✅ الحفظ التلقائي للوسائط الذاتية في الخاص فقط
@client.on(events.NewMessage(func=lambda e: is_auto_saving and e.is_private and not e.out and e.media))
async def auto_save_self_destruct_media(event):
    # تجاهل الملصقات والوسائط غير ذاتية التدمير
    if event.sticker or not getattr(event.media, 'ttl_seconds', None):
        return

    try:
        file = await client.download_media(event.media, file="temp_media_file")
        me = await client.get_me()

        await client.send_file(
            "me",
            file,
            caption="✅ تم حفظ الوسائط ذاتية التدمير تلقائيًا.\n\n📌 يُرجى عدم إساءة استخدامها."
        )

    except FileReferenceExpiredError:
        pass  # تجاهل الوسائط منتهية الصلاحية
    except RPCError as e:
        print(f"[ذاتيه تلقائي] خطأ أثناء الحفظ: {e}")
    except Exception as e:
        print(f"[ذاتيه تلقائي] خطأ غير متوقع: {e}")
    finally:
        if os.path.exists("temp_media_file"):
            os.remove("temp_media_file")

    
    

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

@client.on(events.NewMessage(pattern=r'^\.كت$'))
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



@client.on(events.NewMessage(pattern=r'^\.انتحال$'))
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

@client.on(events.NewMessage(pattern=r'^\.اعاده$'))
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
@client.on(events.NewMessage(pattern=r'^\.فحص$'))
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
                      
# متغير لحفظ معرفات الرسائل التلقائية لكل مستخدم
user_auto_messages = {}

# تفعيل أمر الحماية
@client.on(events.NewMessage(pattern=r'^\.الحمايه تفعيل$'))
async def enable_protection(event):
    global protection_enabled
    protection_enabled = True
    await event.edit("**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**")

# تعطيل أمر الحماية
@client.on(events.NewMessage(pattern=r'^\.الحمايه تعطيل$'))
async def disable_protection(event):
    global protection_enabled
    protection_enabled = False
    await event.edit("**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**")

# الرد التلقائي مع تحذير المستخدم
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global protection_enabled, user_auto_messages
    if not protection_enabled:
        return  # لا يتم تنفيذ أي شيء إذا كانت الحماية معطلة

    # تأكد أن الرسالة واردة من محادثة خاصة فقط
    if not event.is_private:
        return  # تجاهل الرسائل من القنوات أو المجموعات

    sender = await event.get_sender()
    user_id = sender.id
    user_name = sender.first_name

    if user_id not in accepted_users and not sender.bot:  # يعمل فقط في الخاص
        # حذف الرسالة التلقائية السابقة إذا كانت موجودة
        if user_id in user_auto_messages:
            try:
                await client.delete_messages(event.chat_id, user_auto_messages[user_id])
            except:
                pass  # تجاهل الأخطاء في حالة عدم وجود الرسالة

        if user_id in warned_users:
            warned_users[user_id] += 1
        else:
            warned_users[user_id] = 1

        # الرد بالتحذير وحفظ معرف الرسالة
        reply_message = await event.respond(f"""
**ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - الـرد التلقـائي 〽️**
•─────────────────•
❞** مرحبـاً** {user_name} ❝
**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك هنا {warned_users[user_id]} مـن 7 تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**
**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**
        """)
        
        # حفظ معرف الرسالة التلقائية
        user_auto_messages[user_id] = reply_message.id

        # إذا وصل للتحذير السابع، يتم حظره
        if warned_users[user_id] >= MAX_WARNINGS:
            await event.respond("**❌ تم حظرك تلقائياً بسبب تكرار الإزعاج.**")
            await client(BlockRequest(user_id))
            # حذف معرف الرسالة من القاموس بعد الحظر
            if user_id in user_auto_messages:
                del user_auto_messages[user_id]

# قبول المستخدم
@client.on(events.NewMessage(pattern=r'^\.قبول$'))
async def accept_user(event):
    reply = await event.get_reply_message()
    if reply:
        user = await client.get_entity(reply.sender_id)
        accepted_users[user.id] = {'name': user.first_name, 'reason': "لم يذكر"}
        
        # حذف الرسالة التلقائية إذا كانت موجودة
        if user.id in user_auto_messages:
            try:
                await client.delete_messages(event.chat_id, user_auto_messages[user.id])
                del user_auto_messages[user.id]
            except:
                pass
        
        await event.edit(f"""
**⎉╎المستخـدم**  {user.first_name}
**⎉╎تـم السـمـاح لـه بـإرسـال الـرسـائـل 💬✓ **
**⎉╎ الـسـبـب ❔  : ⎉╎لـم يـذكـر 🤷🏻‍♂**
        """)

# رفض المستخدم
@client.on(events.NewMessage(pattern=r'^\.رفض$'))
async def reject_user(event):
    reply = await event.get_reply_message()
    if reply:
        user = await client.get_entity(reply.sender_id)
        await client(BlockRequest(user.id))  # حظر المستخدم
        
        # حذف الرسالة التلقائية إذا كانت موجودة
        if user.id in user_auto_messages:
            try:
                await client.delete_messages(event.chat_id, user_auto_messages[user.id])
                del user_auto_messages[user.id]
            except:
                pass
        
        await event.edit(f"""
**⎉╎المستخـدم ** {user.first_name}
**⎉╎تـم رفـضـه مـن أرسـال الـرسـائـل ⚠️**
**⎉╎ الـسـبـب ❔  : ⎉╎ لـم يـذكـر 💭**
        """)

# عرض قائمة المقبولين
@client.on(events.NewMessage(pattern=r'^\.المقبولين$'))
async def show_accepted(event):
    if accepted_users:
        message = "- قائمـة المسمـوح لهـم ( المقبـوليـن ) :\n\n"
        for user_id, info in accepted_users.items():
            user = await client.get_entity(user_id)
            message += f"• 👤 **الاسـم :** {info['name']}\n- **الايـدي :** {user_id}\n- المعـرف : @{user.username}\n- **السـبب :** {info['reason']}\n\n"
        await event.edit(message)
    else:
        await event.edit("**لا يوجد مستخدمين مقبولين حالياً.**")


# متغيرات تجميع في بوت دعمكم
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

@client.on(events.NewMessage(pattern=r'^\.دعمكم$'))
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
@client.on(events.NewMessage(pattern=r'^\.لانهائي دعمكم$'))
async def handle_infinite_damkom_command(event):
    global is_collecting
    is_collecting = True
    print('تم تفعيل وضع التجميع اللانهائي.')
    
    await event.edit('**⎉╎تم تفعيل وضع التجميع اللانهائي .. سيتم إعادة التجميع كل 10 دقائق.**')
    asyncio.create_task(infinite_damkom_loop(event))  # بدء التجميع اللانهائي في الخلفية

# أمر إيقاف دعمكم
@client.on(events.NewMessage(pattern=r'^\.ايقاف دعمكم$'))
async def handle_stop_command(event):
    global is_collecting
    is_collecting = False
    print('تم إيقاف التجميع.')
    
    await event.edit('**⎉╎تم إيقاف تجميع دعمكم .. بنجاح☑️**')

# أمر نقاط دعمكم
@client.on(events.NewMessage(pattern=r'^\.نقاط دعمكم$'))
async def handle_points_command(event):
    print('جارِ حساب نقاط دعمكم.')
    
    await event.edit('**⎉╎جـارِ حسـاب نقاطـك في بـوت دعمـكـم ...✓**')
    await client.send_message('@DamKomBot', '/start')  # إرسال /start للبوت

    await asyncio.sleep(5)  # انتظار 5 ثوانٍ
    message = await client.get_messages('@DamKomBot', limit=1)
    
    if message:  # التأكد من وجود رسالة
        await event.edit(message[0].raw_text)  # تحويل الرسالة مباشرة التي يرسلها البوت

# أمر هدية دعمكم
@client.on(events.NewMessage(pattern=r'^\.هدية دعمكم$'))
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

@client.on(events.NewMessage(pattern=r'^\.عربي$'))
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

@client.on(events.NewMessage(pattern=r'^\.انجلش$'))
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

@client.on(events.NewMessage(pattern=r'^\.انضم(?:\s+(.+))?', outgoing=True))
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

@client.on(events.NewMessage(pattern=r'^\.غادر(?:\s+(.+))?', outgoing=True))
async def leave_channel_or_group(event):
    
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


@client.on(events.NewMessage(pattern=r'^\.حفظ(?:\s+(.+))?'))
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


@client.on(events.NewMessage(pattern=r'^\.احصائيات'))

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

@client.on(events.NewMessage(pattern=r'^\.مغادرة القنوات$'))

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

@client.on(events.NewMessage(pattern=r'^\.مغادرة الجروبات$'))

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
 
@client.on(events.NewMessage(pattern=r'^\.حذف البوتات$'))
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
        



@client.on(events.NewMessage(pattern=r'^\.ستوريات(?:\s+(.+))?'))
async def download_stories(event):
    # الحصول على المعرف من الرسالة أو الرد
    input_arg = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message()
    
    if not input_arg and not reply_msg:
        await event.edit("**⚠️ يرجى تحديد المستخدم (معرف، آيدي، أو رابط) أو الرد على رسالة تحتوي عليها**")
        return
    
    target = input_arg if input_arg else reply_msg.text
    target = target.strip()
    
    await event.edit("**🔍 جاري البحث عن المستخدم...**")
    
    try:
        # الحصول على الكيان مع معالجة أنواع Peer المختلفة
        try:
            if target.isdigit():
                user = await client.get_entity(int(target))
            else:
                if target.startswith('@'):
                    target = target[1:]
                if 't.me/' in target:
                    target = target.split('t.me/')[-1].split('/')[0]
                user = await client.get_entity(target)
        except Exception as e:
            await event.edit(f"**⚠️ لا يمكن العثور على المستخدم: {str(e)}**")
            return
        
        # إنشاء Peer صالح للطلب
        if hasattr(user, 'user_id'):
            peer = InputPeerUser(user.user_id, user.access_hash)
        elif hasattr(user, 'channel_id'):
            peer = InputPeerChannel(user.channel_id, user.access_hash)
        else:
            await event.edit("**⚠️ نوع الحساب غير مدعوم**")
            return
        
        await event.edit(f"**📥 جاري جلب استوريات @{getattr(user, 'username', '')}...**")
        
        # إنشاء مجلد لحفظ الاستوريات
        folder_name = f"stories_{user.id}_{datetime.now().strftime('%Y%m%d')}"
        os.makedirs(folder_name, exist_ok=True)
        
        # استرداد الاستوريات
        try:
            stories = await client(GetStoriesArchiveRequest(
                offset_id=0,
                limit=100,
                peer=peer
            ))
        except Exception as e:
            await event.edit(f"**⚠️ لا يمكن جلب الستوريات: {str(e)}**")
            return
        
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
        await event.edit(f"**⚠️ حدث خطأ غير متوقع: {str(e)}**")

@client.on(events.NewMessage(pattern=r'^\.إنشاء صورة (.+)'))
async def generate_ai_image(event):
    try:
        description = event.pattern_match.group(1).strip()
        if not description:
            await event.edit("**⚠️ يرجى كتابة وصف للصورة**\nمثال: `.إنشاء صورة منظر طبيعي مع شروق الشمس`")
            return

        msg = await event.edit("**🎨 جاري إنشاء صورتك...**")
        
        # ترجمة الوصف للإنجليزية
        translated = GoogleTranslator(source='auto', target='en').translate(description)
        
        # طلب إنشاء الصورة
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"},
            json={"inputs": translated},
            timeout=30
        )

        if response.status_code == 200:
            with open("ai_image.jpg", "wb") as f:
                f.write(response.content)
            
            await client.send_file(
                event.chat_id,
                "ai_image.jpg",
                caption=f"**الصورة المطلوبة:**\n`{description}`\n\n**الوصف المترجم:**\n`{translated}`",
                reply_to=event.message.id
            )
            await msg.delete()
            os.remove("ai_image.jpg")
        else:
            error = response.json().get("error", response.text)
            await msg.edit(f"**❌ خطأ في الإنشاء:**\n`{error}`")

    except Exception as e:
        await event.edit(f"**⚠️ حدث خطأ:**\n`{str(e)}`")

@client.on(events.NewMessage(pattern=r'^\.معرفة الانمي$'))
async def anime_search(event):
    if not event.is_reply:
        await event.respond("⚠️ يرجى الرد على صورة من الأنمي")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg.media:
        await event.respond("⚠️ يجب الرد على صورة فقط")
        return

    try:
        # إرسال رسالة الانتظاب بخط عريض وكبير
        processing_msg = await event.edit(
            "**⏳ انتظر قليلًا...**",
            parse_mode='md'
        )

        # تحميل الصورة
        photo_data = await reply_msg.download_media(file=bytes)

        # طلب API للتعرف على الأنمي
        async with httpx.AsyncClient(timeout=30) as http_client:
            response = await http_client.post(
                "https://api.trace.moe/search?anilistInfo",
                files={"image": photo_data}
            )

        if response.status_code != 200:
            await processing_msg.edit("❌ الخدمة غير متاحة حالياً، حاول لاحقاً")
            return

        data = response.json()
        results = data.get("result", [])
        if not results:
            await processing_msg.edit("❌ لم يتم التعرف على الأنمي")
            return

        best = results[0]
        titles = best.get("anilist", {}).get("title", {})
        native = titles.get("native", "غير معروف")
        romaji = titles.get("romaji", "غير معروف")
        english = titles.get("english", "غير معروف")
        episode = best.get("episode", "غير معروف")
        similarity = f"{best['similarity'] * 100:.1f}%"
        time_min = int(best["from"]) // 60
        time_sec = int(best["from"]) % 60
        time_str = f"{time_min:02}:{time_sec:02}"

        # تنسيق الرسالة النصية بشكل أجمل
        caption = (
    "**🎌 تم التعرف على الأنمي بنجاح!**\n\n"
    "├─ **📌 المعلومات الأساسية:**\n"
    f"│   ├─ **🇯🇵 الاسم الياباني:** `{native}`\n"
    f"│   ├─ **✨ الاسم الروماجي:** `{romaji}`\n"
    f"│   └─ **🇬🇧 الاسم الإنجليزي:** `{english}`\n\n"
    "├─ **📺 تفاصيل المشهد:**\n"
    f"│   ├─ **الحلقة:** `{episode}`\n"
    f"│   ├─ **الوقت:** `{time_str}`\n"
    f"│   └─ **مطابقة المشهد:** `{similarity}`\n"

        )

        video_url = best.get("video")
        if video_url:
            # تحسين رابط الفيديو للحصول على أعلى جودة
            video_url += "?size=l" if "?" not in video_url else "&size=l"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "video/mp4,video/*;q=0.9,*/*;q=0.8",
                "Referer": "https://trace.moe/"
            }

            try:
                # التحقق من حجم الفيديو قبل التحميل
                async with httpx.AsyncClient(headers=headers) as http_client:
                    head = await http_client.head(video_url)
                    size = int(head.headers.get("Content-Length", 0))

                    if size > 50 * 1024 * 1024:  # 50MB الحد الأقصى لتليجرام
                        await processing_msg.delete()
                        await event.respond(f"{caption}\n\n❌ الفيديو كبير جداً للإرسال")
                        return

                    # تحميل الفيديو
                    response = await http_client.get(video_url, timeout=60)
                    response.raise_for_status()

                # حفظ الفيديو مؤقتاً
                video_path = "anime_scene.mp4"
                with open(video_path, "wb") as f:
                    f.write(response.content)

                # إرسال الفيديو مع خيارات متقدمة
                await client.send_file(
                    event.chat_id,
                    file=video_path,
                    caption=caption,
                    reply_to=reply_msg.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=int(best["to"] - best["from"]),
                            w=640,
                            h=360,
                            supports_streaming=True
                        )
                    ],
                    supports_streaming=True,
                    video_note=False
                )

                # حذف الملف المؤقت ورسالة الانتظار
                os.remove(video_path)
                await processing_msg.delete()

            except httpx.TimeoutException:
                await processing_msg.edit("**⏱ انتهت مهلة الاتصال**\n\nيرجى المحاولة مرة أخرى", parse_mode='md')
            except Exception as e:
                await processing_msg.delete()
                await event.respond(f"{caption}\n\n❌ حدث خطأ في إرسال الفيديو")
        else:
            await processing_msg.delete()
            await event.respond(caption)

    except httpx.TimeoutException:
        await event.respond("**⏱ انتهت مهلة الاتصال**\n\nيرجى المحاولة مرة أخرى", parse_mode='md')
    except Exception as e:
        await event.respond("**❌ حدث خطأ غير متوقع**\n\nيرجى المحاولة لاحقاً", parse_mode='md')
                
@client.on(events.NewMessage(pattern=r'^\.فلور\s+(t\.me/nft/\S+)', outgoing=True))
async def handle_floor(event):
    url = event.pattern_match.group(1)

    await event.edit("**انتظر قليلًا . . . ⏳**")

    bot = await client.get_entity(bot_username)
    async with client.conversation(bot) as conv:
        try:
            await conv.send_message("/start")
            await asyncio.sleep(5)

            await conv.send_message(url)
            await asyncio.sleep(2)

            # الحصول على الرد مع الأزرار
            response = await conv.get_response()

            if response.buttons:
                for row in response.buttons:
                    for button in row:
                        if '🎁 Gift information' in button.text:
                            await button.click()
                            await asyncio.sleep(2)
                            final_response = await conv.get_response()

                            # حذف رسالة الانتظار
                            await event.delete()
                            
                            # إرسال الرسالة بنفس التنسيق الأصلي
                            await client.send_message(
                                event.chat_id,
                                final_response.message,
                                formatting_entities=final_response.entities,
                                buttons=final_response.buttons,
                                link_preview=False
                            )
                            return

            await event.edit("❌ لم يتم العثور على زر 'Gift information'.")

        except Exception as e:
            await event.edit(f"❌ حدث خطأ: {str(e)}") 
               
@client.on(events.NewMessage(pattern=r'^\.(?:تحليل|VT)(?:\s+(http[s]?://\S+))?'))
async def virus_total_handler(event):
    url_match = event.pattern_match.group(1)

    async def wait_for_completion(analysis_id, max_retries=10, delay=15):
        for _ in range(max_retries):
            report = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
                headers={"x-apikey": VIRUSTOTAL_API}
            ).json()
            
            status = report.get("data", {}).get("attributes", {}).get("status")
            if status == "completed":
                return report
            await asyncio.sleep(delay)
        return None

    # ====== 🔗 فحص الرابط ======
    if url_match:
        url = url_match.strip()
        await event.edit("**⏳ جاري فحص الرابط... (قد يستغرق دقيقة)**")
        try:
            response = requests.post(
                "https://www.virustotal.com/api/v3/urls",
                headers={"x-apikey": VIRUSTOTAL_API},
                data={"url": url}
            )
            data = response.json()

            if "error" in data:
                return await event.edit(f"**❌ خطأ:** {data['error']['message']}")

            analysis_id = data["data"]["id"]
            encoded_url = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            report_url = f"https://www.virustotal.com/gui/url/{encoded_url}"

            report = await wait_for_completion(analysis_id)
            
            if not report:
                return await event.edit(
                    f"**⏳ التقرير لم يكتمل بعد**\n"
                    f"يمكنك مراجعة التقرير يدوياً: [اضغط هنا]({report_url})\n"
                    f"(عادة ما يستغرق 1-2 دقيقة)"
                )

            final_report = requests.get(
                f"https://www.virustotal.com/api/v3/urls/{encoded_url}",
                headers={"x-apikey": VIRUSTOTAL_API}
            ).json()

            stats = final_report["data"]["attributes"]["last_analysis_stats"]
            total_engines = sum(stats.values())
            
            result_text = (
                f"**🔍 نتائج فحص الرابط:**\n"
                f"• ⚠️ ضار: {stats.get('malicious', 0)}/{total_engines}\n"
                f"• ✅ نظيف: {stats.get('harmless', 0)}/{total_engines}\n"
                f"• 🟡 مشبوه: {stats.get('suspicious', 0)}/{total_engines}\n"
                f"• ⏳ غير محدد: {stats.get('undetected', 0)}/{total_engines}\n"
                f"• 🔗 رابط التقرير: [اضغط هنا]({report_url})\n"
                f"• 📊 تم الفحص بواسطة {total_engines} محرك تحليل"
            )

            await event.edit(result_text)

        except Exception as e:
            await event.edit(f"**⚠️ حدث خطأ أثناء فحص الرابط:** {str(e)}")

    # ====== 📁 فحص الملف - الإصدار المحسن ======
@client.on(events.NewMessage(pattern=r'^\.(?:تحليل|vt)(?:\s+(.+))?', outgoing=True))
async def virus_total_handler(event):
    # فحص الملفات فقط
    if not event.is_reply:
        return await event.edit("**⚠️ يرجى الرد على الملف المراد فحصه**")
    
    reply_msg = await event.get_reply_message()
    if not reply_msg.media:
        return await event.edit("**⚠️ يجب الرد على ملف حقيقي**")

    try:
        # تحميل الملف
        await event.edit("**⏳ جاري تحميل الملف...**")
        file_path = await reply_msg.download_media()
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # الحجم بالميجابايت
        
        # التحقق من حجم الملف
        if file_size > 32:
            os.remove(file_path)
            return await event.edit("**❌ يتجاوز حجم الملف الحد المسموح (32MB)**")

        # إرسال الملف لـ VirusTotal
        await event.edit("**🔍 جاري فحص الملف على VirusTotal...**")
        with open(file_path, 'rb') as file:
            response = requests.post(
                'https://www.virustotal.com/api/v3/files',
                headers={'x-apikey': VIRUSTOTAL_API},
                files={'file': (os.path.basename(file_path), file)},
                timeout=60
            )
        
        data = response.json()
        
        if response.status_code != 200:
            error_msg = data.get('error', {}).get('message', 'خطأ غير معروف')
            os.remove(file_path)
            return await event.edit(
                "**⚠️ عذرًا، خدمة فحص الملفات غير متاحة حاليًا**\n"
                f"السبب: {error_msg}\n\n"
                "يرجى المحاولة في وقت لاحق أو استخدام الموقع الرسمي:\n"
                "https://www.virustotal.com"
            )

        analysis_id = data['data']['id']
        report_url = f"https://www.virustotal.com/gui/file/{analysis_id}"

        # انتظار اكتمال التحليل
        await event.edit("**⏳ جاري تحليل الملف... (قد يستغرق 3-5 دقائق)**")
        for _ in range(15):  # 15 محاولة كل 20 ثانية
            await asyncio.sleep(20)
            analysis_report = requests.get(
                f'https://www.virustotal.com/api/v3/analyses/{analysis_id}',
                headers={'x-apikey': VIRUSTOTAL_API}
            ).json()
            
            if analysis_report.get('data', {}).get('attributes', {}).get('status') == 'completed':
                break
        else:
            os.remove(file_path)
            return await event.edit(
                "**⚠️ عذرًا، خدمة فحص الملفات غير متاحة حاليًا**\n"
                "السبب: تجاوز وقت الانتظار\n\n"
                f"يمكنك التحقق لاحقاً من الرابط:\n{report_url}"
            )

        # جلب النتائج النهائية
        final_report = requests.get(
            f'https://www.virustotal.com/api/v3/files/{analysis_id}',
            headers={'x-apikey': VIRUSTOTAL_API}
        ).json()

        if 'error' in final_report:
            os.remove(file_path)
            return await event.edit(
                "**⚠️ عذرًا، خدمة فحص الملفات غير متاحة حاليًا**\n"
                f"السبب: {final_report['error']['message']}\n\n"
                "يرجى المحاولة في وقت لاحق أو استخدام الموقع الرسمي:\n"
                "https://www.virustotal.com"
            )

        stats = final_report['data']['attributes']['last_analysis_stats']
        result_text = (
            f"**📊 نتائج فحص الملف:**\n"
            f"• 🗂️ الملف: `{os.path.basename(file_path)}`\n"
            f"• 📦 الحجم: {file_size:.2f} MB\n"
            f"• ⚠️ ضار: {stats['malicious']}\n"
            f"• ✅ نظيف: {stats['harmless']}\n"
            f"• 🔗 التقرير الكامل: [اضغط هنا]({report_url})"
        )

        await event.edit(result_text)
        os.remove(file_path)

    except Exception as e:
        error_msg = (
            "**⚠️ عذرًا، خدمة فحص الملفات غير متاحة حاليًا**\n"
            "السبب المحتمل:\n"
            f"- {str(e)}\n\n"
            "يرجى المحاولة في وقت لاحق أو استخدام الموقع الرسمي:\n"
            "https://www.virustotal.com"
        )
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        await event.edit(error_msg)


async def is_authorized(user_id):
    me = await client.get_me()
    return user_id == me.id or user_id in AUTHORIZED_USERS

@client.on(events.NewMessage(pattern=r'^\.تخمين رقم(?:\s+(\d+))?$'))
async def number_guess_game(event):
    if not await is_authorized(event.sender_id):
        return
    
    try:
        player_count = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 1
        if player_count < 1 or player_count > 10:
            raise ValueError
    except:
        await event.reply("⚠️ يرجى إدخال عدد صحيح بين 1 و 10")
        return

    chat_id = event.chat_id
    sender = await event.get_sender()
    
    if chat_id in number_games:
        game = number_games[chat_id]
        if game["status"] == "registering":
            await event.reply("🔄 جاري تسجيل اللاعبين... اكتب `انا` للانضمام!")
        else:
            await event.edit("⏳ هناك لعبة نشطة بالفعل! استخدموا المحاولات المتاحة.")
        return

    registration_msg = await event.edit(
        "🎮 **لعبة تخمين الرقم - وضع الجماعي**\n\n"
        f"👥 عدد اللاعبين المطلوب: {player_count}\n"
        f"🖊️ اللاعب 1: {sender.first_name}\n\n"
        "📝 للإنضمام اكتب: `انا`\n"
        "⏳ انتظار اللاعبين... (اكتب `.انهاء تخمين` لإلغاء اللعبة)"
    )
    
    number_games[chat_id] = {
        "status": "registering",
        "players": {str(event.sender_id): {"name": sender, "attempts": 0, "guessed": False}},
        "required_players": player_count,
        "registered": 1,
        "registration_message": registration_msg,
        "countdown_message": None,
        "game_messages": [],
        "start_time": time.time()
    }

    if player_count == 1:
        await start_number_game(chat_id)

@client.on(events.NewMessage(pattern='^انا$'))
async def register_number_player(event):
    if event.chat_id not in number_games:
        return
    
    game = number_games[event.chat_id]
    
    if event.date.timestamp() < game["start_time"]:
        return
    
    if game["status"] != "registering":
        return
    
    player_id = str(event.sender_id)
    if player_id in game["players"]:
        await event.reply("✅ أنت مسجل بالفعل في اللعبة!")
        return
    
    sender = await event.get_sender()
    game["players"][player_id] = {"name": sender, "attempts": 0, "guessed": False}
    game["registered"] += 1
    
    players_list = "\n".join(
        f"{i+1}. {p['name'].first_name}" 
        for i, p in enumerate(game["players"].values()))

    if game.get("countdown_message"):
        try:
            await game["countdown_message"].delete()
        except:
            pass
    
    countdown_msg = await event.reply(
        "🎮 **لعبة تخمين الرقم - وضع الجماعي**\n\n"
        f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
        f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
        f"{players_list}\n\n"
        "⏳ سيتم بدأ اللعبة بعد 10 ثوان..."
    )
    
    game["countdown_message"] = countdown_msg
    game["game_messages"].append(countdown_msg)
    
    if game["registered"] >= game["required_players"]:
        for i in range(9, 0, -1):
            await asyncio.sleep(1)
            try:
                await countdown_msg.edit(
                    "🎮 **لعبة تخمين الرقم - وضع الجماعي**\n\n"
                    f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
                    f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
                    f"{players_list}\n\n"
                    f"⏳ سيتم بدأ اللعبة بعد {i} ثوان..."
                )
            except:
                pass
        
        await countdown_msg.edit(
            "🎮 **لعبة تخمين الرقم - وضع الجماعي**\n\n"
            f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
            f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
            f"{players_list}\n\n"
            "⏳ **سيتم بدأ اللعبة بعد قليل...**"
        )
        await asyncio.sleep(2)
        
        await start_number_game(event.chat_id)

async def start_number_game(chat_id):
    try:
        game = number_games[chat_id]
        
        bot_message = await client.send_message(
            chat_id,
            "**🔢 من أي رقم إلى أي رقم تريد أن تلعب؟**\nمثال: اكتب `1:100` أو `50:500`"
        )
        
        game.update({
            "status": "waiting_range",
            "bot_message": bot_message,
            "game_start_time": time.time(),
            "game_messages": [bot_message]
        })
        
    except Exception as e:
        if chat_id in number_games:
            del number_games[chat_id]
        await client.send_message(chat_id, f"❌ فشل في بدء اللعبة: {str(e)}\n⚠️ يرجى المحاولة لاحقا")

@client.on(events.NewMessage())
async def handle_range_input(event):
    chat_id = event.chat_id
    if chat_id not in number_games:
        return
    
    game = number_games[chat_id]
    
    if game["status"] != "waiting_range":
        return
    
    # تجاهل الرسائل القديمة
    if event.date.timestamp() < game["game_start_time"]:
        return
    
    # التأكد من أن المرسل هو أحد اللاعبين
    player_id = str(event.sender_id)
    if player_id not in game["players"]:
        return
    
    if not re.match(r'^\d+:\d+$', event.text):
        # إرسال رسالة جديدة بدلاً من الرد على الرسالة القديمة
        error_msg = await event.reply("**⚠️ الصيغة غير صحيحة! استخدم رقم مثل: 1:100**")
        game["game_messages"].append(error_msg)
        return

    try:
        min_num, max_num = map(int, event.text.split(':'))
    except:
        error_msg = await event.reply("**⚠️ يجب أن تكون الأرقام صحيحة!**")
        game["game_messages"].append(error_msg)
        return

    if min_num >= max_num:
        error_msg = await event.reply("**⚠️ الرقم الأول يجب أن يكون أصغر من الثاني!**")
        game["game_messages"].append(error_msg)
        return

    secret = random.randint(min_num, max_num)
    players_list = "\n".join(
        f"{i+1}. {p['name'].first_name}" 
        for i, p in enumerate(game["players"].values()))
    
    game.update({
        "status": "playing",
        "secret": secret,
        "range": (min_num, max_num),
        "remaining_attempts": 10 * game["required_players"],
        "current_player": 0,
        "player_ids": list(game["players"].keys())
    })

    await game["bot_message"].reply(
        "🎮 **لعبة تخمين الرقم - وضع الجماعي**\n\n"
        f"👥 **اللاعبون:**\n{players_list}\n\n"
        f"🔢 **النطاق:** من {min_num} إلى {max_num}\n"
        f"💡 **لديكم {game['remaining_attempts']} محاولات مشتركة**\n\n"
        f"🎯 **الدور لـ {game['players'][game['player_ids'][0]]['name'].first_name}**"
    )

@client.on(events.NewMessage())
async def handle_number_guess(event):
    chat_id = event.chat_id
    if chat_id not in number_games:
        return
    
    game = number_games[chat_id]
    
    if game["status"] != "playing":
        return
    
    # تجاهل الرسائل القديمة
    if event.date.timestamp() < game["game_start_time"]:
        return
    
    player_id = str(event.sender_id)
    
    if player_id not in game["players"]:
        return
    
    # التحقق من أن اللاعب الحالي هو الذي يرسل التخمين
    if player_id != game["player_ids"][game["current_player"]]:
        current_player_name = game["players"][game["player_ids"][game["current_player"]]]["name"].first_name
        await event.reply(f"⏳ ليس دورك الآن! الدور لـ {current_player_name}")
        return
    
    try:
        guess = int(event.text)
    except:
        return

    min_num, max_num = game["range"]
    if guess < min_num or guess > max_num:
        error_msg = await event.reply(f"⚠️ الرقم يجب أن يكون بين {min_num} و {max_num}")
        game["game_messages"].append(error_msg)
        return

    game["remaining_attempts"] -= 1
    game["players"][player_id]["attempts"] += 1

    if guess == game["secret"]:
        winner = game["players"][player_id]["name"]
        attempts = game["players"][player_id]["attempts"]
        
        await event.reply(
            f"✨ **تهانينا! لقد فاز {winner.first_name}** ✨\n\n"
            f"🎯 **الرقم الصحيح:** {guess}\n"
            f"📊 **عدد المحاولات:** {attempts}\n\n"
            f"🏆 **مبروك للفائز!**"
        )
        del number_games[chat_id]
        return
    
    if game["remaining_attempts"] <= 0:
        await event.reply(
            f"💔 **انتهت جميع المحاولات!**\n\n"
            f"🔎 **الرقم الصحيح كان:** {game['secret']}\n\n"
            f"🏁 **انتهت اللعبة!**"
        )
        del number_games[chat_id]
        return
    
    # تغيير الدور للاعب التالي
    game["current_player"] = (game["current_player"] + 1) % len(game["player_ids"])
    next_player = game["players"][game["player_ids"][game["current_player"]]]["name"].first_name
    
    hint = "⬆️ أعلى!" if guess < game["secret"] else "⬇️ أقل!"
    
    reply_msg = await event.reply(
        f"❌ **تخمين خاطئ!**\n"
        f"{hint}\n\n"
        f"📊 **المحاولات المتبقية:** {game['remaining_attempts']}\n"
        f"🎯 **الدور التالي لـ {next_player}**"
    )
    game["game_messages"].append(reply_msg)

@client.on(events.NewMessage(pattern=r'^\.انهاء تخمين$'))
async def end_number_game(event):
    chat_id = event.chat_id
    if chat_id not in number_games:
        await event.edit("⚠️ لا يوجد لعبة نشطة لإنهائها")
        return
    
    game = number_games[chat_id]
    
    if game["status"] == "registering":
        await event.edit("✅ تم إلغاء لعبة التخمين أثناء التسجيل")
        del number_games[chat_id]
        return
    
    if "secret" in game:
        message = (
            "🛑 **تم إنهاء اللعبة!**\n\n"
            f"🔎 **الرقم الصحيح كان:** {game['secret']}\n\n"
            "🏁 **انتهت اللعبة!**"
        )
    else:
        message = "🛑 **تم إلغاء لعبة التخمين!**"
    
    await event.reply(message)
    del number_games[chat_id]

    await event.reply(response)
async def is_authorized(user_id):
    me = await client.get_me()
    return user_id == me.id or user_id in AUTHORIZED_USERS

@client.on(events.NewMessage(pattern=r'^\.(طقس|wt)(?:\s+(.+))?$'))
async def weather_command(event):
    # التحقق من أن المرسل مصرح له
    if not await is_authorized(event.sender_id):
        return
    
    command = event.pattern_match.group(1)
    location = event.pattern_match.group(2)
    
    # إنشاء رسالة البوت أولاً
    bot_message = await event.edit("⏳ جاري المعالجة..." if command == "طقس" else "⏳ Processing...")
    
    if not location:
        example = "القاهرة" if command == "طقس" else "london"
        response_msg = f"""
**⚠️ يرجى تحديد الموقع**
استخدم: `.{command} {example}`
مثال: `.{command} {example}`
        """
        await bot_message.edit(response_msg)
        return

    try:
        loading_msg = "⏳ جاري جلب بيانات الطقس..." if command == "طقس" else "⏳ Fetching weather data..."
        await bot_message.edit(loading_msg)
        
        # رابط API مع إعدادات اللغة العربية والوحدات المترية
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API}&units=metric&lang={'ar' if command == 'طقس' else 'en'}"
        response = requests.get(url, timeout=10).json()
        
        if str(response.get("cod")) != "200":
            error_msg = {
                "401": "مفتاح API غير صالح" if command == "طقس" else "Invalid API key",
                "404": "المدينة غير موجودة" if command == "طقس" else "City not found",
                "429": "تم تجاوز الحد المسموح" if command == "طقس" else "Too many requests"
            }.get(str(response.get("cod")), response.get("message", "خطأ غير معروف" if command == "طقس" else "Unknown error"))
            
            suggestion = "جرب كتابة اسم المدينة بالإنجليزية" if command == "طقس" else "Try using the main city name"
            error_response = f"""
**⚠️ {error_msg}**
- الموقع: {location}
- {suggestion}
            """
            await bot_message.edit(error_response)
            return

        # استخراج البيانات
        weather_data = {
            "city": response["name"],
            "country": response["sys"]["country"],
            "temp": round(response["main"]["temp"], 1),
            "feels_like": round(response["main"]["feels_like"], 1),
            "humidity": response["main"]["humidity"],
            "wind": round(response["wind"]["speed"], 1),
            "description": response["weather"][0]["description"].capitalize(),
            "sunrise": datetime.fromtimestamp(response["sys"]["sunrise"]).strftime('%H:%M'),
            "sunset": datetime.fromtimestamp(response["sys"]["sunset"]).strftime('%H:%M'),
            "icon": response["weather"][0]["icon"]
        }

        # رموز تعبيرية حسب حالة الطقس
        weather_icons = {
            "01": "☀️", "02": "⛅", "03": "☁️", "04": "☁️☁️",
            "09": "🌧️", "10": "🌦️", "11": "⛈️", "13": "❄️", "50": "🌫️"
        }
        icon_code = weather_data["icon"][:2]
        weather_emoji = weather_icons.get(icon_code, "🌤️")

        # رابط البحث عن المدينة
        city_search_url = f"https://openweathermap.org/find?q={quote(location)}"

        # تنسيق الرسالة
        if command == "طقس":
            weather_report = f"""
{weather_emoji} **تقرير الطقس لـ {weather_data['city']}, {weather_data['country']}** {weather_emoji}
─────────────────
**🌡 الحرارة:** {weather_data['temp']}°C (تشعر بـ {weather_data['feels_like']}°C)
**📊 الحالة:** {weather_data['description']}
**💧 الرطوبة:** {weather_data['humidity']}%
**🌬 الرياح:** {weather_data['wind']} م/ث
**🌅 الشروق:** {weather_data['sunrise']}
**🌇 الغروب:** {weather_data['sunset']}
─────────────────
📎 [عرض التقرير على الموقع]({city_search_url})
            """
        else:
            weather_report = f"""
{weather_emoji} **Weather in {weather_data['city']}, {weather_data['country']}** {weather_emoji}
─────────────────
**🌡 Temp:** {weather_data['temp']}°C (Feels like {weather_data['feels_like']}°C)
**📊 Condition:** {weather_data['description']}
**💧 Humidity:** {weather_data['humidity']}%
**🌬 Wind:** {weather_data['wind']} m/s
**🌅 Sunrise:** {weather_data['sunrise']}
**🌇 Sunset:** {weather_data['sunset']}
─────────────────
📎 [View full report]({city_search_url})
            """
        
        # تعديل رسالة البوت
        await bot_message.edit(weather_report, link_preview=False)
        
    except requests.exceptions.Timeout:
        error_msg = "انتهى وقت الاتصال" if command == "طقس" else "Request timeout"
        await bot_message.edit(f"**⚠️ {error_msg}**\nيرجى المحاولة لاحقاً")
    except requests.exceptions.RequestException:
        error_msg = "خطأ في الاتصال" if command == "طقس" else "Connection error"
        await bot_message.edit(f"**⚠️ {error_msg}**\nتأكد من اتصالك بالإنترنت")
    except Exception as e:
        error_msg = "حدث خطأ غير متوقع" if command == "طقس" else "Unexpected error"
        await bot_message.edit(f"**⚠️ {error_msg}**\n{str(e)}")


# قائمة الألغاز
riddles = {
    # ألغاز كلاسيكية
    "ما الشيء الذي كلما أخذت منه كبر؟": "الحفرة",
    "ما هو الشيء الذي يمشي بلا رجلين ويبكي بلا عينين؟": "السحاب",
    "ما الشيء الذي له أسنان ولا يعض؟": "المشط",
    "ما هو الشيء الذي يكتب ولكنه لا يقرأ؟": "القلم",
    "ما الشيء الذي يحملك وتحمله في نفس الوقت؟": "الحذاء",
    "ما الشيء الذي يدور حول البيت دون أن يتحرك؟": "الجدار",
    "ما الشيء الذي يخترق الزجاج ولا يكسره؟": "الضوء",
    "ما الشيء الذي له رأس ولا عينين؟": "الدبوس",
    
    # ألغاز ذكاء
    "ما الشيء الذي يكون أخضر في الأرض وأسود في السوق وأحمر في البيت؟": "الشاي",
    "ما الشيء الذي ينام ولا يقوم؟": "الليل",
    "ما الشيء الذي لا يدخل إلا إذا ضربته على رأسه؟": "المسمار",
    "ما الشيء الذي كلما زاد نقص؟": "العمر",
    "ما الشيء الذي لا يمكن كسره؟": "الماء",
    "ما الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟": "الهاتف",
    "ما الشيء الذي له أربع أرجل ولا يمشي؟": "الكرسي",
    
    # ألغاز مضحكة
    "ما الشيء الذي له عين واحدة ولا يرى؟": "الإبرة",
    "ما الشيء الذي يمكنك كسره دون أن تلمسه؟": "الوعد",
    "ما الشيء الذي يذهب ولا يعود؟": "الدخان",
    "ما الشيء الذي يطير بلا أجنحة؟": "الوقت",
    "ما الشيء الذي كلما طال قصر؟": "العمر",
    
    # ألغاز طبيعية
    "ما الشيء الذي يولد كل شهر ويموت كل أسبوع؟": "القمر",
    "ما الشيء الذي يظهر في الليل ويختفي في النهار؟": "النجوم",
    "ما الشيء الذي يأكل ولا يشبع؟": "النار",
    "ما الشيء الذي لا يبتل حتى لو دخل الماء؟": "الظل",
    
    # ألغاز متنوعة
    "ما الشيء الذي يملك الكثير من المفاتيح لكن لا يفتح أي باب؟": "البيانو",
    "ما الشيء الذي يمكنك حمله في يدك اليمنى ولكن لا يمكنك حمله في يدك اليسرى؟": "اليد اليسرى",
    "ما الشيء الذي يمتلك عنقًا ولكن لا يمتلك رأسًا؟": "الزجاجة",
    "ما الشيء الذي يمكنك أن ترميه كلما احتجت إليه؟": "المرساة",
    
    # ألغاز إبداعية
    "ما الشيء الذي يمكنه السفر حول العالم وهو باقٍ في زاويته؟": "الطابع البريدي",
    "ما الشيء الذي يمتلك مدنًا بلا منازل، وغابات بلا أشجار، وأنهارًا بلا ماء؟": "الخريطة",
    "ما الشيء الذي يمكنه ملء الغرفة لكنه لا يشغل أي مساحة؟": "الضوء",
    "ما الشيء الذي يمكنك كسره دون أن تلمسه؟": "الصمت",
    
    # ألغاز عملية
    "ما الشيء الذي يمتلك يدًا ولكن لا يمتلك ذراعًا؟": "الساعة",
    "ما الشيء الذي يمتلك وجهًا واحدًا ويدين ولكن لا يمتلك أرجلًا؟": "الساعة",
    "ما الشيء الذي يمتلك أسنانًا ولكن لا يعض؟": "المشط",
    "ما الشيء الذي يمتلك فرعًا ولكن لا يمتلك جذعًا ولا أوراقًا ولا فروعًا؟": "البنك",
    
    # ألغاز تاريخية
    "ما الشيء الذي كان غدًا وسيكون أمس؟": "اليوم",
    "ما الشيء الذي يسبقك دائمًا ولكنك لا تستطيع اللحاق به؟": "المستقبل",
    "ما الشيء الذي يمكنك أن تمسكه ولكن لا يمكنك أن تلمسه؟": "الأنفاس",
    
    # ألغاز رياضية
    "ما الشيء الذي يزيد عندما تأخذ منه؟": "الحفرة",
    "ما الشيء الذي يمكنك أن تضيف إليه ولكن يصبح أصغر؟": "الثقب",
    "ما الشيء الذي يمكنك أن تضربه وتقسمه ولكن لا يمكنك أن تراه أو تلمسه؟": "العدد",
    
    # ألغاز يومية
    "ما الشيء الذي تراه في الصباح وفي الظهر وفي المساء ولكنك لا تراه في الليل؟": "الشمس",
    "ما الشيء الذي يمكنك أن ترميه عندما تريد استخدامه وتلتقطه عندما لا تريد استخدامه؟": "صنارة الصيد",
    "ما الشيء الذي يمكنك أن تمسكه بيدك اليمنى ولكن لا يمكنك أن تمسكه بيدك اليسرى؟": "الكوع الأيسر",
    
    # ألغاز خيالية
    "ما الشيء الذي يمكنه أن يملأ أي غرفة في ثانية واحدة؟": "الظلام",
    "ما الشيء الذي يمكنه أن يسافر حول العالم وهو باقٍ في مكانه؟": "الطوابع البريدية",
    "ما الشيء الذي يمكنه أن يكون أمامك وخلفك في نفس الوقت؟": "المستقبل والماضي",
    
    # ألغاز علمية
    "ما الشيء الذي يمكنه أن يكون سائلًا وصلبًا وغازيًا في نفس الوقت؟": "الماء",
    "ما الشيء الذي يمكنه أن يمر عبر الزجاج دون أن يكسره؟": "الضوء",
    "ما الشيء الذي يمكنه أن يكون موجودًا في كل مكان وفي نفس الوقت لا يكون في أي مكان؟": "الظل",
    
    # ألغاز ثقافية
    "ما الشيء الذي يمكنه أن يكون أبيض وأسود وأحمر وأزرق في نفس الوقت؟": "الكتاب",
    "ما الشيء الذي يمكنه أن يكون في السماء وفي الأرض وفي الماء في نفس الوقت؟": "الحرف 'ن'",
    "ما الشيء الذي يمكنه أن يكون في كل مكان وفي نفس الوقت لا يكون في أي مكان؟": "الفكرة",
    
    # ألغاز فلسفية
    "ما الشيء الذي يمكنك أن تعطيه ولكن لا يمكنك أن تأخذه؟": "الوعد",
    "ما الشيء الذي يمكنك أن تخسره ولكن لا يمكنك أن تكسبه؟": "الوقت",
    "ما الشيء الذي يمكنك أن تمتلكه ولكن لا يمكنك أن تلمسه؟": "الاسم",
    
    # ألغاز إسلامية
    "ما الشيء الذي خلقه الله ثم أنكره؟": "الكذب",
    "ما الشيء الذي خلقه الله واستعظمه؟": "الكبر",
    "ما الشيء الذي خلقه الله وأمرنا بإماتته؟": "الهوى",
    
    # ألغاز للأطفال
    "ما الشيء الذي له عين واحدة ولا يرى؟": "الإبرة",
    "ما الشيء الذي ينام ولا يقوم؟": "النهر",
    "ما الشيء الذي يطير بلا أجنحة؟": "السحاب",
    
    # ألغاز صعبة
    "ما الشيء الذي يمكنك أن تراه في الماء ولكن لا يمكنك أن تلمسه؟": "الانعكاس",
    "ما الشيء الذي يمكنك أن تسمعه ولكن لا يمكنك أن تراه أو تلمسه؟": "الصوت",
    "ما الشيء الذي يمكنك أن تشعر به ولكن لا يمكنك أن تراه أو تلمسه؟": "الهواء",
    
}

@client.on(events.NewMessage(pattern=r'^\.لغز(?:\s+(\d+))?$'))
async def start_riddle_game(event):
    chat_id = event.chat_id
    
    try:
        player_count = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 1
        if player_count < 1 or player_count > 10:
            raise ValueError
    except:
        await event.reply("⚠️ يرجى إدخال عدد صحيح بين 1 و 10")
        return

    if chat_id in riddle_games:
        game = riddle_games[chat_id]
        if game["status"] == "registering":
            await event.reply("🔄 جاري تسجيل اللاعبين... اكتب `انا` للانضمام!")
        else:
            await event.edit("⏳ هناك لعبة نشطة بالفعل! استخدموا المحاولات المتاحة.")
        return

    sender = await event.get_sender()
    registration_msg = await event.edit(
        "🧩 **لعبة الألغاز - وضع الجماعي**\n\n"
        f"👥 عدد اللاعبين المطلوب: {player_count}\n"
        f"🖊️ اللاعب 1: {sender.first_name}\n\n"
        "📝 للإنضمام اكتب: `انا`\n"
        "⏳ انتظار اللاعبين... (اكتب `.لغز ايقاف` لإلغاء اللعبة)"
    )
    
    riddle_games[chat_id] = {
        "status": "registering",
        "players": {str(event.sender_id): {"name": sender, "guessed": False}},
        "required_players": player_count,
        "registered": 1,
        "registration_message": registration_msg,
        "countdown_message": None,
        "game_messages": [],
        "start_time": time.time()
    }

    if player_count == 1:
        await start_riddle_round(chat_id)

@client.on(events.NewMessage(pattern='^انا$'))
async def register_riddle_player(event):
    if event.chat_id not in riddle_games:
        return
    
    game = riddle_games[event.chat_id]
    
    if event.date.timestamp() < game["start_time"]:
        return
    
    if game["status"] != "registering":
        return
    
    player_id = str(event.sender_id)
    if player_id in game["players"]:
        await event.reply("✅ أنت مسجل بالفعل في اللعبة!")
        return
    
    sender = await event.get_sender()
    game["players"][player_id] = {"name": sender, "guessed": False}
    game["registered"] += 1
    
    players_list = "\n".join(
        f"{i+1}. {p['name'].first_name}" 
        for i, p in enumerate(game["players"].values()))

    if game.get("countdown_message"):
        try:
            await game["countdown_message"].delete()
        except:
            pass
    
    countdown_msg = await event.reply(
        "🧩 **لعبة الألغاز - وضع الجماعي**\n\n"
        f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
        f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
        f"{players_list}\n\n"
        "⏳ سيتم بدأ اللعبة بعد 10 ثوان..."
    )
    
    game["countdown_message"] = countdown_msg
    game["game_messages"].append(countdown_msg)
    
    if game["registered"] >= game["required_players"]:
        for i in range(9, 0, -1):
            await asyncio.sleep(1)
            try:
                await countdown_msg.edit(
                    "🧩 **لعبة الألغاز - وضع الجماعي**\n\n"
                    f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
                    f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
                    f"{players_list}\n\n"
                    f"⏳ سيتم بدأ اللعبة بعد {i} ثوان..."
                )
            except:
                pass
        
        await countdown_msg.edit(
            "🧩 **لعبة الألغاز - وضع الجماعي**\n\n"
            f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
            f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
            f"{players_list}\n\n"
            "⏳ **سيتم بدأ اللعبة بعد قليل...**"
        )
        await asyncio.sleep(2)
        
        await start_riddle_round(event.chat_id)

async def start_riddle_round(chat_id):
    try:
        game = riddle_games[chat_id]
        question, answer = random.choice(list(riddles.items()))
        
        players_list = "\n".join(
            f"{i+1}. {p['name'].first_name}" 
            for i, p in enumerate(game["players"].values()))
        
        riddle_msg = await client.send_message(
            chat_id,
            "🧩 **لعبة الألغاز - وضع الجماعي**\n\n"
            f"👥 **اللاعبون:**\n{players_list}\n\n"
            f"❓ **اللغز:**\n{question}\n\n"
            "💡 أول إجابة صحيحة تفوز!"
        )
        
        game.update({
            "status": "playing",
            "question": question,
            "answer": answer.lower(),
            "riddle_message": riddle_msg,
            "game_start_time": time.time()
        })
        
    except Exception as e:
        if chat_id in riddle_games:
            del riddle_games[chat_id]
        await client.send_message(chat_id, f"❌ فشل في بدء اللعبة: {str(e)}\n⚠️ يرجى المحاولة لاحقا")

@client.on(events.NewMessage())
async def handle_riddle_answer(event):
    chat_id = event.chat_id
    if chat_id not in riddle_games:
        return
    
    game = riddle_games[chat_id]
    
    if game["status"] != "playing":
        return
    
    # تجاهل الرسائل القديمة
    if event.date.timestamp() < game["game_start_time"]:
        return
    
    player_id = str(event.sender_id)
    if player_id not in game["players"]:
        return
    
    if game["players"][player_id]["guessed"]:
        return
    
    user_answer = event.text.strip().lower()
    if user_answer == game["answer"]:
        game["players"][player_id]["guessed"] = True
        winner = game["players"][player_id]["name"]
        
        await event.reply(
            f"✨ **تهانينا! لقد فاز {winner.first_name}** ✨\n\n"
            f"🎯 **الإجابة الصحيحة:** {game['answer']}\n\n"
            f"🏆 **مبروك للفائز!**"
        )
        del riddle_games[chat_id]

@client.on(events.NewMessage(pattern=r'^\.لغز ايقاف$'))
async def stop_riddle_game(event):
    chat_id = event.chat_id
    if chat_id not in riddle_games:
        await event.edit("⚠️ لا يوجد لعبة نشطة لإنهائها")
        return
    
    game = riddle_games[chat_id]
    
    if game["status"] == "registering":
        await event.reply("✅ تم إلغاء لعبة الألغاز أثناء التسجيل")
        del riddle_games[chat_id]
        return
    
    if "answer" in game:
        message = (
            "🛑 **تم إنهاء اللعبة!**\n\n"
            f"🔎 **الإجابة الصحيحة كانت:** {game['answer']}\n\n"
            "🏁 **انتهت اللعبة!**"
        )
    else:
        message = "🛑 **تم إلغاء لعبة الألغاز!**"
    
    await event.reply(message)
    del riddle_games[chat_id]

@client.on(events.NewMessage(pattern=r'^\.انمي$'))
async def anime_command(event):
    try:
        # جلب شخصية عشوائية
        character = get_random_anime_character()
        
        # إرسال الصورة مع المعلومات
        await client.send_file(
            event.chat_id,
            character["image"],
            caption=f"🎌 **معلومات شخصية الأنمي**\n\n"
                    f"🏷 **الاسم الإنجليزي:** {character['name']}\n"
                    f"🌐 **الاسم الياباني:** {character.get('name_kanji', 'غير متوفر')}\n"
                    f"📺 **الأنمي:** {character.get('anime', 'غير معروف')}\n\n"
                    f"❓ هل تعرف هذه الشخصية؟"
        )
        
    except Exception as e:
        await event.reply(f"❌ حدث خطأ أثناء جلب البيانات: {str(e)}")

def get_random_anime_character():
    # جلب قائمة أشهر 25 شخصية
    url = "https://api.jikan.moe/v4/top/characters?limit=25"
    response = requests.get(url).json()
    characters = response["data"]
    
    # اختيار شخصية عشوائية
    character = random.choice(characters)
    
    # استخراج معلومات الأنمي (أول أنمي ظهرت فيه)
    anime_info = ""
    if character.get('anime'):
        anime_info = character['anime'][0]['anime']['title'] if character['anime'] else 'غير معروف'
    
    # تفاصيل الشخصية
    return {
        "name": character["name"],
        "name_kanji": character.get("name_kanji", "غير متوفر"),
        "anime": anime_info,
        "image": character["images"]["jpg"]["image_url"]
    }
    

def similar(a, b):
    """تقارن التشابه بين نصين مع دعم العربية"""
    if not a or not b or len(str(a).strip()) < 3 or len(str(b).strip()) < 3:
        return False
        
    try:
        a = str(a).lower().strip()
        b = str(b).lower().strip()
        
        similarity = SequenceMatcher(None, a, b).ratio()
        if similarity > 0.7:
            return True
            
        if (len(a) >= 3 and a in b) or (len(b) >= 3 and b in a):
            return True
            
        return False
    except Exception:
        return False

async def get_unique_character():
    """جلب شخصية مع الترجمة العربية"""
    try:
        url = "https://api.jikan.moe/v4/top/characters"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("data"):
            raise ValueError("لا توجد بيانات متاحة من API")
            
        characters = [c for c in data["data"] if c.get("mal_id") not in used_characters]
        
        if not characters:
            used_characters.clear()
            characters = data["data"]
        
        character = random.choice(characters)
        used_characters.add(character["mal_id"])
        
        anime_info = character.get("anime", [{}])
        anime_title = anime_info[0].get("anime", {}).get("title", "غير معروف") if anime_info else "غير معروف"
        
        try:
            name_ar = translator.translate(character["name"], dest='ar').text
        except:
            name_ar = character["name"]
        
        return {
            "id": character["mal_id"],
            "name": character.get("name", "غير معروف"),
            "name_ar": name_ar,
            "name_kanji": character.get("name_kanji", ""),
            "anime": anime_title,
            "image": character.get("images", {}).get("jpg", {}).get("image_url", ""),
            "nicknames": character.get("nicknames", []),
            "url": character.get("url", "")
        }
        
    except Exception as e:
        raise Exception(f"خطأ في جلب البيانات: {str(e)}")

ANILIST_QUERY = '''
query ($page: Int, $perPage: Int) {
    Page(page: $page, perPage: $perPage) {
        characters(sort: FAVOURITES_DESC) {
            id
            name {
                full
                native
                alternative
            }
            image {
                large
            }
            media(sort: POPULARITY_DESC, type: ANIME) {
                nodes {
                    title {
                        romaji
                        english
                        native
                    }
                }
            }
            siteUrl
        }
    }
}
'''

async def fetch_anilist_characters():
    """جلب شخصيات شهيرة من AniList"""
    try:
        variables = {
            'page': random.randint(2, 5),
            'perPage': 1000
        }
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: requests.post(
                'https://graphql.anilist.co',
                json={'query': ANILIST_QUERY, 'variables': variables},
                timeout=10
            )
        )
        
        data = response.json()
        characters = data['data']['Page']['characters']
        random.shuffle(characters)
        return characters[:1000]
        
    except Exception as e:
        print(f"خطأ في جلب البيانات من AniList: {e}")
        return []

async def get_next_character():
    """الحصول على الشخصية التالية من المجموعة"""
    global current_pool_index, character_pool
    
    if not character_pool or current_pool_index >= len(character_pool):
        character_pool = await fetch_anilist_characters()
        current_pool_index = 0
        if not character_pool:
            raise Exception("لا يمكن جلب بيانات الشخصيات")
    
    character = character_pool[current_pool_index]
    current_pool_index += 1
    
    anime_title = "غير معروف"
    if character['media']['nodes']:
        anime = character['media']['nodes'][0]['title']
        anime_title = anime.get('romaji') or anime.get('english') or anime.get('native') or "غير معروف"
    
    alternative_names = []
    if character['name']['alternative']:
        alternative_names.extend(character['name']['alternative'])
    
    return {
        "id": character['id'],
        "name": character['name']['full'],
        "name_native": character['name']['native'],
        "anime": anime_title,
        "image": character['image']['large'],
        "nicknames": alternative_names,
        "url": character['siteUrl']
    }

@client.on(events.NewMessage(pattern=r'^\.تخمين انمي(?: (\d+))?'))
async def start_anime_game(event):
    # استخدام lock لمنع إنشاء عدة ألعاب
    async with message_locks[event.chat_id]:
        if event.chat_id in anime_games:
            game = anime_games[event.chat_id]
            if game["status"] == "registering":
                await event.reply("🔄 جاري تسجيل اللاعبين... اكتب `انا` للانضمام!")
            else:
                await event.reply("⏳ هناك لعبة نشطة بالفعل! استخدموا المحاولات المتاحة.")
            return
        
        try:
            player_count = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 1
            if player_count < 1 or player_count > 10:
                raise ValueError
        except:
            await event.reply("⚠️ يرجى إدخال عدد صحيح بين 1 و 10")
            return

        sender = await event.get_sender()
        rules_text = """
💡 <b>القواعد:</b>
- يمكن التخمين بالإنجليزية/اليابانية (العربية قريباً) 
- إذا خمنت الاسم بنسبة تطابق 70% ستفوز
- أول إجابة صحيحة تفوز!
- لديكم {} محاولات مشتركة
- للإنضمام اكتب: <code>انا</code>
""".format(5 * player_count)

        registration_msg = await event.edit(
            "🎮 <b>لعبة تخمين الأنمي - وضع الجماعي</b>\n\n"
            f"👥 <b>عدد اللاعبين المطلوب:</b> {player_count}\n"
            f"🖊️ <b>اللاعب 1:</b> {sender.first_name}\n\n"
            f"{rules_text}\n"
            "⏳ <b>انتظار اللاعبين . . .</b>\n"
            "(اكتب <code>.انهاء تخمين</code> لإلغاء اللعبة)",
            parse_mode='html'
        )
        
        anime_games[event.chat_id] = {
            "status": "registering",
            "players": {str(event.sender_id): {"name": sender, "attempts": 0, "guessed": False}},
            "required_players": player_count,
            "registered": 1,
            "registration_message": registration_msg,
            "countdown_message": None,
            "game_messages": [],
            "start_time": time.time(),
            "last_guess_time": {},  # تتبع آخر محاولة لكل لاعب
            "processing_guess": False,  # منع معالجة عدة تخمينات في نفس الوقت
            "game_ended": False
        }

        if player_count == 1:
            await start_game(event.chat_id)

@client.on(events.NewMessage(pattern='^انا$'))
async def register_player(event):
    if event.chat_id not in anime_games:
        return
    
    # استخدام lock لمنع التسجيل المزدوج
    async with message_locks[event.chat_id]:
        if event.chat_id not in anime_games:
            return
            
        game = anime_games[event.chat_id]
        
        if event.date.timestamp() < game["start_time"]:
            return
        
        if game["status"] != "registering":
            return
        
        player_id = str(event.sender_id)
        if player_id in game["players"]:
            await event.reply("✅ أنت مسجل بالفعل في اللعبة!")
            return
        
        sender = await event.get_sender()
        game["players"][player_id] = {"name": sender, "attempts": 0, "guessed": False}
        game["registered"] += 1
        
        players_list = "\n".join(
            f"{i+1}. {p['name'].first_name}" 
            for i, p in enumerate(game["players"].values()))

        if game.get("countdown_message"):
            try:
                await game["countdown_message"].delete()
                game["countdown_message"] = None
            except:
                pass
        
        countdown_msg = await event.reply(
            "🎮 <b>لعبة تخمين الأنمي - وضع الجماعي</b>\n\n"
            f"👥 <b>عدد اللاعبين المطلوب:</b> {game['required_players']}\n"
            f"🖊️ <b>اللاعبون المسجلون ({game['registered']}/{game['required_players']}):</b>\n"
            f"{players_list}\n\n"
            "⏳ <b>سيتم بدأ اللعبة بعد 10 ثوان...</b>",
            parse_mode='html'
        )
        
        game["countdown_message"] = countdown_msg
        game["game_messages"].append(countdown_msg)
        
        if game["registered"] >= game["required_players"]:
            for i in range(9, 0, -1):
                await asyncio.sleep(1)
                try:
                    await countdown_msg.edit(
                        "🎮 <b>لعبة تخمين الأنمي - وضع الجماعي</b>\n\n"
                        f"👥 <b>عدد اللاعبين المطلوب:</b> {game['required_players']}\n"
                        f"🖊️ <b>اللاعبون المسجلون ({game['registered']}/{game['required_players']}):</b>\n"
                        f"{players_list}\n\n"
                        f"⏳ <b>سيتم بدأ اللعبة بعد {i} ثوان...</b>",
                        parse_mode='html'
                    )
                except:
                    pass
            
            await countdown_msg.edit(
                "🎮 <b>لعبة تخمين الأنمي - وضع الجماعي</b>\n\n"
                f"👥 <b>عدد اللاعبين المطلوب:</b> {game['required_players']}\n"
                f"🖊️ <b>اللاعبون المسجلون ({game['registered']}/{game['required_players']}):</b>\n"
                f"{players_list}\n\n"
                "⏳ <b>سيتم بدأ اللعبة بعد قليل...</b>",
                parse_mode='html'
            )
            await asyncio.sleep(2)
            
            await start_game(event.chat_id)

async def start_game(chat_id):
    try:
        if chat_id not in anime_games:
            return
            
        character = await get_next_character()
        
        if not character or not character.get("image"):
            raise Exception("لا يمكن جلب بيانات الشخصية")
            
        game = anime_games[chat_id]
        game.update({
            "status": "playing",
            "character": character,
            "remaining_attempts": 5 * game["required_players"],
            "started": True,
            "game_start_time": time.time()
        })
        
        players_list = "\n".join(
            f"{i+1}. {p['name'].first_name}" 
            for i, p in enumerate(game["players"].values()))
        
        if game.get("countdown_message"):
            try:
                await game["countdown_message"].edit(
                    "🎮 <b>لعبة تخمين الأنمي - وضع الجماعي</b>\n\n"
                    f"👥 <b>عدد اللاعبين المطلوب:</b> {game['required_players']}\n"
                    f"🖊️ <b>اللاعبون المسجلون ({game['registered']}/{game['required_players']}):</b>\n"
                    f"{players_list}\n\n"
                    "✅ <b>لقد بدأت اللعبة!</b>",
                    parse_mode='html'
                )
            except:
                pass
        
        caption = (
            "🎌 <b>بدأت لعبة تخمين الأنمي!</b>\n\n"
            f"👥 <b>اللاعبون:</b>\n{players_list}\n\n"
        )
        
        try:
            sent_msg = await client.send_file(chat_id, character["image"], caption=caption, parse_mode='html')
            game["game_messages"].append(sent_msg)
        except:
            sent_msg = await client.send_message(chat_id, caption + f"\n🖼️ [اضغط هنا لرؤية الصورة]({character['image']})", parse_mode='html')
            game["game_messages"].append(sent_msg)

    except Exception as e:
        if chat_id in anime_games:
            del anime_games[chat_id]
        await client.send_message(chat_id, f"❌ فشل في بدء اللعبة: {str(e)}\n⚠️ يرجى المحاولة لاحقا")

@client.on(events.NewMessage())
async def handle_guesses(event):
    chat_id = event.chat_id
    
    if chat_id not in anime_games:
        return
    
    # استخدام lock لتجنب race conditions
    async with message_locks[chat_id]:
        # فحص مزدوج للتأكد
        if chat_id not in anime_games:
            return
        
        game = anime_games[chat_id]
        
        if event.date.timestamp() < game.get("game_start_time", 0):
            return
        
        if game["status"] != "playing" or game.get("game_ended", False):
            return
        
        if event.text and event.text.startswith('.'):
            return
        
        if event.sticker or event.media:
            return
        
        if not event.text or len(event.text.strip()) < 3:
            return
        
        player_id = str(event.sender_id)
        
        if player_id not in game["players"]:
            return
        
        if game["players"][player_id]["guessed"]:
            return
        
        # منع الرسائل المتتالية السريعة (حماية من السبام)
        current_time = time.time()
        last_guess = game["last_guess_time"].get(player_id, 0)
        if current_time - last_guess < 0.5:  # نصف ثانية على الأقل بين المحاولات
            return
        
        game["last_guess_time"][player_id] = current_time
        
        # فحص إذا كان هناك تخمين قيد المعالجة
        if game.get("processing_guess", False):
            return
        
        game["processing_guess"] = True
        
        try:
            guess = event.text.strip()
            character = game["character"]
            
            game["remaining_attempts"] -= 1
            game["players"][player_id]["attempts"] += 1
            
            correct_names = [
                character["name"],
                character["name_native"]
            ] + character["nicknames"]
            
            is_correct = any(
                similar(guess, name)
                for name in correct_names
                if name and isinstance(name, str)
            )
            
            if is_correct:
                game["players"][player_id]["guessed"] = True
                game["game_ended"] = True
                winner = game["players"][player_id]["name"]
                
                message = (
                    "✨ <b>تهانينا! لقد فاز {winner_name}</b> ✨\n\n"
                    "🎯 <b>التخمين الصحيح:</b>\n"
                    f"🏷️ <b>الاسم:</b> {character['name']} ({character['name_native']})\n"
                    f"📺 <b>الأنمي:</b> {character['anime']}\n\n"
                    f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
                ).format(winner_name=winner.first_name)
                
                await event.reply(message, link_preview=False, parse_mode='html')
                del anime_games[event.chat_id]
                return
            
            if game["remaining_attempts"] <= 0:
                game["game_ended"] = True
                message = (
                    "💔 <b>انتهت جميع المحاولات!</b>\n\n"
                    "🔎 <b>الإجابة الصحيحة كانت:</b>\n"
                    f"🏷️ <b>الاسم:</b> {character['name']} ({character['name_native']})\n"
                    f"📺 <b>الأنمي:</b> {character['anime']}\n\n"
                    f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
                )
                await event.reply(message, link_preview=False, parse_mode='html')
                del anime_games[event.chat_id]
            else:
                remaining = game["remaining_attempts"]
                attempts_word = "محاولة" if remaining == 1 else "محاولات"
                reply_msg = await event.reply(
                    f"❌ <b>تخمين خاطئ!</b>\n"
                    f"📊 تبقى لديكم {remaining} {attempts_word}",
                    parse_mode='html'
                )
                game["game_messages"].append(reply_msg)
        
        except Exception as e:
            print(f"خطأ في معالجة التخمين: {e}")
        
        finally:
            # إلغاء حالة المعالجة
            game["processing_guess"] = False

@client.on(events.NewMessage(pattern=r'^\.انهاء تخمين$'))
async def end_game(event):
    if event.chat_id not in anime_games:
        await event.reply("**تم انهاء اللعبة **")
        return
    
    async with message_locks[event.chat_id]:
        if event.chat_id not in anime_games:
            await event.reply("**تم انهاء اللعبة **")
            return
            
        game = anime_games[event.chat_id]
        
        character = game.get("character")
        
        if character:
            message = (
                "🛑 <b>تم إنهاء اللعبة!</b>\n\n"
                "🔎 <b>الإجابة الصحيحة كانت:</b>\n"
                f"🏷️ <b>الاسم:</b> {character['name']} ({character['name_native']})\n"
                f"📺 <b>الأنمي:</b> {character['anime']}\n\n"
                f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
            )
        else:
            message = "✅ تم إلغاء لعبة التخمين أثناء التسجيل"
        
        await event.reply(message, link_preview=False, parse_mode='html')
        del anime_games[event.chat_id]

# دالة تنظيف دورية للألعاب المعلقة
async def cleanup_stale_games():
    """تنظيف الألعاب القديمة المعلقة"""
    while True:
        try:
            current_time = time.time()
            stale_games = []
            
            for chat_id, game in anime_games.items():

           #اذا مر 5 دقائق دون تخمين توقف اللعبة او اثناء التسجيل 
           
                if current_time - game["start_time"] > 300:
                    stale_games.append(chat_id)                    
                elif game.get("game_start_time") and current_time - game["game_start_time"] > 300:
                    stale_games.append(chat_id)
            
            for chat_id in stale_games:
                try:
                    await client.send_message(
                        chat_id, 
                        "⏰ تم إنهاء اللعبة تلقائياً بسبب عدم النشاط"
                    )
                except:
                    pass
                
                if chat_id in anime_games:
                    del anime_games[chat_id]
            
            await asyncio.sleep(60)  # فحص كل دقيقة
            
        except Exception as e:
            print(f"خطأ في تنظيف الألعاب: {e}")
            await asyncio.sleep(60)
            


# متغيرات التخزين (في الذاكرة)
monitored_channels = {}  # {channel_id: {'username': str, 'keywords': [str], 'name': str}}
target_user = None  # المستخدم المستهدف للرنين
monitoring_active = True  # حالة المراقبة
current_calls = {}  # المكالمات النشطة

class ChannelMonitoringSystem:
    def __init__(self, client):
        self.client = client
        
    async def add_channel(self, channel_input):
        """إضافة قناة للمراقبة"""
        try:
            # تنظيف المدخل
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            # الحصول على كيان القناة
            entity = await self.client.get_entity(channel_input)
            
            # التحقق من أنها قناة وليس مستخدم
            if not hasattr(entity, 'broadcast') or not entity.broadcast:
                return False, "هذا ليس قناة صالحة"
            
            # التحقق من الحد الأقصى للقنوات
            if len(monitored_channels) >= 3:
                return False, "تم الوصول للحد الأقصى (3 قنوات)"
            
            # إضافة القناة
            monitored_channels[entity.id] = {
                'username': entity.username or str(entity.id),
                'keywords': [],
                'name': entity.title
            }
            
            return True, f"تم إضافة قناة: {entity.title}"
            
        except Exception as e:
            return False, f"خطأ في إضافة القناة: {str(e)}"
    
    async def remove_channel(self, channel_input):
        """إزالة قناة من المراقبة"""
        try:
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            entity = await self.client.get_entity(channel_input)
            
            if entity.id in monitored_channels:
                channel_name = monitored_channels[entity.id]['name']
                del monitored_channels[entity.id]
                return True, f"تم حذف قناة: {channel_name}"
            else:
                return False, "هذه القناة غير مراقبة"
                
        except Exception as e:
            return False, f"خطأ في حذف القناة: {str(e)}"
    
    async def add_keywords(self, channel_input, keywords):
        """إضافة كلمات مفتاحية لقناة"""
        try:
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            entity = await self.client.get_entity(channel_input)
            
            if entity.id in monitored_channels:
                monitored_channels[entity.id]['keywords'] = keywords
                return True, f"تم تحديث كلمات البحث لقناة: {monitored_channels[entity.id]['name']}"
            else:
                return False, "هذه القناة غير مراقبة"
                
        except Exception as e:
            return False, f"خطأ: {str(e)}"
    
    async def make_extended_call(self, user_id):
        """إجراء مكالمة ممتدة"""
        try:
            if user_id in current_calls:
                return False, "مكالمة نشطة بالفعل"
            
            # الحصول على إعدادات المكالمة
            call_config = await self.client(GetCallConfigRequest())
            config_data = call_config.data if hasattr(call_config, 'data') else call_config
            
            min_layer = getattr(config_data, 'min_layer', 65)
            max_layer = getattr(config_data, 'max_layer', 92)
            udp_p2p = getattr(config_data, 'udp_p2p', True)
            udp_reflector = getattr(config_data, 'udp_reflector', True)
            
            # إنشاء معاملات DH
            g_a = os.urandom(256)
            g_a_hash = hashlib.sha256(g_a).digest()
            
            # بدء المكالمة
            call = await self.client(functions.phone.RequestCallRequest(
                user_id=user_id,
                random_id=random.randint(-2147483648, 2147483647),
                g_a_hash=g_a_hash,
                protocol=types.PhoneCallProtocol(
                    min_layer=min_layer,
                    max_layer=max_layer,
                    udp_p2p=udp_p2p,
                    udp_reflector=udp_reflector,
                    library_versions=[]
                )
            ))
            
            # تخزين معلومات المكالمة
            current_calls[user_id] = {
                'call_id': call.phone_call.id,
                'access_hash': call.phone_call.access_hash,
                'start_time': asyncio.get_event_loop().time()
            }
            
            # إنهاء المكالمة بعد 30 ثانية (أو عند الرفض)
            asyncio.create_task(self._auto_end_call(user_id, 30))
            
            return True, "تم بدء المكالمة"
            
        except Exception as e:
            return False, f"خطأ في المكالمة: {str(e)}"
    
    async def _auto_end_call(self, user_id, duration):
        """إنهاء المكالمة تلقائياً بعد مدة معينة"""
        await asyncio.sleep(duration)
        
        if user_id in current_calls:
            try:
                call_info = current_calls[user_id]
                await self.client(functions.phone.DiscardCallRequest(
                    peer=types.InputPhoneCall(
                        id=call_info['call_id'],
                        access_hash=call_info['access_hash']
                    ),
                    duration=duration,
                    reason=types.PhoneCallDiscardReasonHangup(),
                    connection_id=0
                ))
                del current_calls[user_id]
            except:
                pass
    
    async def check_message_for_keywords(self, message, channel_id):
        """فحص الرسالة للكلمات المفتاحية"""
        if not monitoring_active or channel_id not in monitored_channels:
            return False
        
        keywords = monitored_channels[channel_id]['keywords']
        if not keywords:
            return False
        
        message_text = message.message.lower() if message.message else ""
        
        for keyword in keywords:
            if keyword.lower() in message_text:
                return True
        
        return False

# إنشاء نظام المراقبة
monitor_system = ChannelMonitoringSystem(client)

# الأوامر

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.مراقبة (.+)$'))
async def add_channel_command(event):
    """إضافة قناة للمراقبة"""
    channel_input = event.pattern_match.group(1).strip()
    
    await event.edit("**جاري إضافة القناة...**")
    
    success, message = await monitor_system.add_channel(channel_input)
    
    if success:
        await event.edit(f"✅ **{message}**")
    else:
        await event.edit(f"❌ **{message}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.حذف_مراقبة (.+)$'))
async def remove_channel_command(event):
    """حذف قناة من المراقبة"""
    channel_input = event.pattern_match.group(1).strip()
    
    success, message = await monitor_system.remove_channel(channel_input)
    
    if success:
        await event.edit(f"✅ **{message}**")
    else:
        await event.edit(f"❌ **{message}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.المراقبين$'))
async def list_channels_command(event):
    """عرض القنوات المراقبة"""
    if not monitored_channels:
        await event.edit("**📭 لا توجد قنوات مراقبة**")
        return
    
    text = "**📋 القنوات المراقبة:**\n\n"
    
    for channel_id, info in monitored_channels.items():
        status = "🟢 نشط" if monitoring_active else "🔴 متوقف"
        keywords_text = ", ".join(info['keywords']) if info['keywords'] else "لا توجد كلمات"
        
        text += f"**📺 {info['name']}**\n"
        text += f"└ المعرف: @{info['username']}\n"
        text += f"└ الحالة: {status}\n"
        text += f"└ الكلمات: {keywords_text}\n\n"
    
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.كلمات (.+?) (.+)$'))
async def add_keywords_command(event):
    """إضافة كلمات مفتاحية لقناة"""
    channel_input = event.pattern_match.group(1).strip()
    keywords_input = event.pattern_match.group(2).strip()
    
    keywords = [k.strip() for k in keywords_input.split(',')]
    
    success, message = await monitor_system.add_keywords(channel_input, keywords)
    
    if success:
        await event.edit(f"✅ **{message}**\n**الكلمات:** {', '.join(keywords)}")
    else:
        await event.edit(f"❌ **{message}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.مستهدف (.+)$'))
async def set_target_command(event):
    """تحديد المستخدم المستهدف"""
    global target_user
    
    user_input = event.pattern_match.group(1).strip()
    
    if user_input.startswith('@'):
        user_input = user_input[1:]
    
    try:
        if user_input.isdigit():
            user = await client.get_entity(int(user_input))
        else:
            user = await client.get_entity(user_input)
        
        if getattr(user, 'bot', False):
            await event.edit("❌ **لا يمكن استهداف البوتات**")
            return
        
        target_user = user.id
        user_name = getattr(user, 'first_name', 'المستخدم')
        await event.edit(f"✅ **تم تحديد المستهدف:** {user_name}")
        
    except Exception as e:
        await event.edit(f"❌ **خطأ في تحديد المستهدف:** {str(e)}")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.إيقاف_مراقبة$'))
async def pause_monitoring_command(event):
    """إيقاف المراقبة مؤقتاً"""
    global monitoring_active
    monitoring_active = False
    await event.edit("⏸️ **تم إيقاف المراقبة مؤقتاً**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.تشغيل_مراقبة$'))
async def resume_monitoring_command(event):
    """تشغيل المراقبة"""
    global monitoring_active
    monitoring_active = True
    await event.edit("▶️ **تم تشغيل المراقبة**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.رن (.+)$'))
async def manual_ring_command(event):
    """رنين يدوي"""
    user_input = event.pattern_match.group(1).strip()
    
    if user_input.startswith('@'):
        user_input = user_input[1:]
    
    try:
        if user_input.isdigit():
            user = await client.get_entity(int(user_input))
        else:
            user = await client.get_entity(user_input)
        
        await event.edit("**📞 جاري الاتصال...**")
        
        success, message = await monitor_system.make_extended_call(user.id)
        
        if success:
            user_name = getattr(user, 'first_name', 'المستخدم')
            await event.edit(f"✅ **تم الاتصال بـ {user_name}**")
        else:
            await event.edit(f"❌ **{message}**")
            
    except Exception as e:
        await event.edit(f"❌ **خطأ: {str(e)}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.شرح_المراقبة$'))
async def help_command(event):
    """شرح جميع الأوامر"""
    help_text = """**📖 شرح أوامر نظام المراقبة:**

**🔧 إعداد المراقبة:**
• `.مراقبة [قناة]` - إضافة قناة للمراقبة
  مثال: `.مراقبة @hhjaiw`

• `.حذف_مراقبة [قناة]` - حذف قناة من المراقبة

• `.كلمات [قناة] [كلمات]` - إضافة كلمات بحث
  مثال: `.كلمات @hhjaiw مرحبا,أهلا,السلام`

• `.مستهدف [مستخدم]` - تحديد من سيتم الاتصال به
  مثال: `.مستهدف @username`

**⚙️ التحكم:**
• `.إيقاف_مراقبة` - إيقاف المراقبة مؤقتاً
• `.تشغيل_مراقبة` - تشغيل المراقبة
• `.المراقبين` - عرض القنوات المراقبة

**📞 الاتصال:**
• `.رن [مستخدم]` - اتصال يدوي
• `.شرح_المراقبة` - عرض هذا الشرح

**📝 ملاحظات:**
• الحد الأقصى: 3 قنوات
• مدة المكالمة: 30 ثانية
• يمكن فصل الكلمات بالفاصلة (,)"""

    await event.edit(help_text)

# مراقب الرسائل الجديدة في القنوات
@client.on(events.NewMessage)
async def monitor_channels(event):
    """مراقبة الرسائل في القنوات المحددة"""
    if not monitoring_active or not target_user:
        return
    
    # التحقق من أن الرسالة من قناة مراقبة
    if event.chat_id not in monitored_channels:
        return
    
    # فحص الكلمات المفتاحية
    if await monitor_system.check_message_for_keywords(event, event.chat_id):
        channel_name = monitored_channels[event.chat_id]['name']
        
        # إجراء المكالمة
        success, message = await monitor_system.make_extended_call(target_user)
        
        if success:
            # إرسال تنبيه للحساب الشخصي
            try:
                me = await client.get_me()
                await client.send_message(me.id, 
                    f"🚨 **تم العثور على كلمة مفتاحية!**\n"
                    f"📺 القناة: {channel_name}\n"
                    f"💬 الرسالة: {event.message[:100]}...\n"
                    f"📞 تم الاتصال بالمستهدف")
            except:
                pass


@client.on(events.NewMessage(pattern=r'\.لصوره'))
async def sticker_to_photo(event):
    # تحقق من وجود رد على رسالة تحتوي على ملصق
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()

        if reply_message and reply_message.sticker:
            # أرسل رسالة جاري التحويل
            processing_message = await event.edit("**جاري التحويل لصورة...**")

            # تحميل الملصق
            sticker = await reply_message.download_media(file=bytes)

            try:
                # فتح الملصق باستخدام PIL للتعامل مع صيغ .webp أو غيرها
                image = Image.open(io.BytesIO(sticker))

                # في حال كان الملصق متحركًا (مثل .webp)، خذ أول إطار
                if image.is_animated:
                    image = image.convert("RGBA")  # قم بتحويل الصورة إلى صيغة RGBA لضمان شفافية صحيحة
                    frame = image.seek(0)  # اختيار الإطار الأول
                else:
                    image = image.convert("RGBA")  # تحويل أي صورة إلى صيغة RGBA إذا كانت غير متحركة

                # تحويل الصورة إلى JPEG
                output_image = io.BytesIO()
                image.convert("RGB").save(output_image, format="JPEG")
                output_image.name = "sticker.jpg"
                output_image.seek(0)

                # حذف رسالة "جاري التحويل لصورة..."
                await processing_message.delete()

                # إرسال الصورة
                await client.send_file(event.chat_id, output_image, caption="**تم التحويل بنجاح ✅**")

            except Exception as e:
                await processing_message.delete()
                await event.edit(f"⚠️ حدث خطأ أثناء التحويل: {e}")
        else:
            await event.edit("⚠️ يرجى الرد على ملصق لتحويله إلى صورة.")
    else:
        await event.edit("⚠️ يرجى الرد على ملصق لتحويله إلى صورة.")

@client.on(events.NewMessage(pattern=r'\.حول بصمه'))
async def handler(event):
    # التحقق من وجود رسالة رد تحتوي على فيديو
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        
        if reply_message.video:
            # إرسال رسالة "جاري التحويل..." والاحتفاظ بمعرف الرسالة
            processing_message = await event.edit("**جاري التحويل...**")
            # تحميل الفيديو
            video_path = await reply_message.download_media()

            # استخراج الصوت من الفيديو باستخدام pydub
            audio_path = video_path.split('.')[0] + ".mp3"
            try:
                # تحويل الفيديو إلى صوت باستخدام ffmpeg
                video = AudioSegment.from_file(video_path)
                video.export(audio_path, format="mp3")
                
                # إرسال الصوت كبصمة صوتية
                await client.send_file(event.chat_id, audio_path, voice_note=True)
                
            except Exception as e:
                await event.edit(f"حدث خطأ أثناء التحويل: {str(e)}")
            
            finally:
                # حذف رسالة "جاري التحويل..." بعد إرسال البصمة
                await client.delete_messages(event.chat_id, processing_message)

                # حذف الرسالة الأصلية
                await event.delete()

                # حذف الملفات المؤقتة
                if os.path.exists(video_path):
                    os.remove(video_path)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                
        else:
            await event.edit("**يرجى الرد على فيديو للتحويل.**")
    else:
        await event.edit("**يرجى الرد على فيديو.**")


@client.on(events.NewMessage(pattern=r'\.حول صوت'))
async def handler(event):
    # التحقق من وجود رسالة رد تحتوي على فيديو
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        
        if reply_message.video:
            # إرسال رسالة "جاري التحويل..." والاحتفاظ بمعرف الرسالة
            processing_message = await event.edit("**جاري التحويل...**")

            # تحميل الفيديو
            video_path = await reply_message.download_media()

            # استخراج الصوت من الفيديو باستخدام pydub
            audio_path = video_path.split('.')[0] + ".mp3"
            try:
                # تحويل الفيديو إلى صوت باستخدام ffmpeg
                video = AudioSegment.from_file(video_path)
                video.export(audio_path, format="mp3")
            except Exception as e:
                await event.edit(f"**حدث خطأ أثناء التحويل**: {str(e)}")
                return
            
            # إرسال الصوت كملف صوت MP3
            await client.send_file(event.chat_id, audio_path)

            # حذف رسالة "جاري التحويل..." بعد إرسال الملف الصوتي
            await client.delete_messages(event.chat_id, processing_message)

            # حذف الرسالة الأصلية
            await event.delete()
            
            # حذف الملفات المؤقتة
            os.remove(video_path)
            os.remove(audio_path)
        else:
            await event.edit("**يرجى الرد على فيديو للتحويل.**")
    else:
        await event.edit("**يرجى الرد على فيديو.**")

@client.on(events.NewMessage(pattern=r'\.لمتحرك'))
async def handler(event):
    # التحقق من وجود رسالة رد تحتوي على صورة أو ملصق
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        
        if reply_message.photo or reply_message.sticker:  # التحقق مما إذا كانت الرسالة تحتوي على صورة أو ملصق
            # إرسال رسالة "جاري التحويل..." والاحتفاظ بمعرف الرسالة
            processing_message = await event.edit("**جاري التحويل...**")

            # تحميل الصورة أو الملصق
            file_path = await reply_message.download_media()

            # تحديد مسار GIF النهائي
            gif_path = file_path.split('.')[0] + ".gif"
            try:
                # تحويل الصورة أو الملصق إلى GIF باستخدام ffmpeg
                subprocess.run([
                    'ffmpeg', 
                    '-i', file_path,  # إدخال الملف
                    '-vf', 'fps=24,scale=512:-1:flags=lanczos',  # تحسين عدد الإطارات والدقة
                    '-t', '5',  # تحديد مدة الـ GIF (يمكنك تعديل المدة إذا لزم الأمر)
                    '-y',  # السماح بالكتابة فوق الملف إذا كان موجوداً
                    gif_path
                ], check=True)
            except Exception as e:
                await event.edit(f"**حدث خطأ أثناء التحويل**: {str(e)}")
                return
            
            # إرسال GIF
            await client.send_file(event.chat_id, gif_path)

            # حذف رسالة "جاري التحويل..." بعد إرسال GIF
            await client.delete_messages(event.chat_id, processing_message)

            # حذف الملفات المؤقتة
            os.remove(file_path)
            os.remove(gif_path)
        else:
            await event.edit("**يرجى الرد على صورة أو ملصق للتحويل.**")
    else:
        await event.edit("**يرجى الرد على صورة أو ملصق.**")


@client.on(events.NewMessage(pattern=r'\.لمتحركه'))
async def handler(event):
    # التحقق من وجود رسالة رد تحتوي على فيديو
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()

        if reply_message.video:
            # إرسال رسالة "جاري التحويل..." والاحتفاظ بها
            processing_message = await event.edit("**جاري التحويل...**")

            # تحميل الفيديو
            file_path = await reply_message.download_media()

            # تحديد مسار GIF النهائي
            gif_path = file_path.split('.')[0] + ".gif"
            
            try:
                # الحصول على معلومات الفيديو لاستخراج FPS الأصلي
                probe_cmd = [
                    'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                    '-show_streams', file_path
                ]
                result = subprocess.run(probe_cmd, capture_output=True, text=True)
                
                # استخدام FPS افتراضي إذا فشل في الحصول على معلومات الفيديو
                original_fps = 30
                try:
                    import json
                    video_info = json.loads(result.stdout)
                    for stream in video_info['streams']:
                        if stream['codec_type'] == 'video':
                            fps_str = stream.get('r_frame_rate', '30/1')
                            if '/' in fps_str:
                                num, den = fps_str.split('/')
                                original_fps = int(float(num) / float(den))
                            break
                except:
                    original_fps = 30
                
                # استخدام FPS أعلى للحصول على GIF أكثر سلاسة
                target_fps = min(original_fps, 25)  # الحد الأقصى 25 fps
                
                # تحويل الفيديو إلى GIF مع تحسينات أفضل
                subprocess.run([
                    'ffmpeg',
                    '-i', file_path,
                    '-vf', f'fps={target_fps},scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
                    '-t', '10',  # زيادة المدة إلى 10 ثوان
                    '-y',  # الكتابة فوق الملف إذا كان موجوداً
                    gif_path
                ], check=True, capture_output=True)
                
            except Exception as e:
                await event.edit(f"**حدث خطأ أثناء التحويل:** {e}")
                return

            # التحقق من حجم الملف
            file_size = os.path.getsize(gif_path)
            max_size = 8 * 1024 * 1024  # 8 MB حد أقصى لتيليجرام
            
            if file_size > max_size:
                # إعادة التحويل بجودة أقل إذا كان الملف كبيراً
                try:
                    subprocess.run([
                        'ffmpeg',
                        '-i', file_path,
                        '-vf', f'fps={min(target_fps, 15)},scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
                        '-t', '8',
                        '-y',
                        gif_path
                    ], check=True, capture_output=True)
                except Exception as e:
                    await event.edit(f"**حدث خطأ في تقليل الحجم:** {e}")
                    return

            # إرسال GIF
            await client.send_file(event.chat_id, gif_path, caption="**تم التحويل بنجاح! 🎬**")

            # حذف رسالة "جاري التحويل..." بعد إرسال GIF
            await processing_message.delete()

            # حذف الرسالة الأصلية
            await event.delete()

            # حذف الملفات المؤقتة
            try:
                os.remove(file_path)
                os.remove(gif_path)
            except:
                pass  # تجاهل الأخطاء في حذف الملفات
                
        else:
            await event.edit("**يرجى الرد على فيديو.**")
    else:
        await event.edit("**يرجى الرد على فيديو.**")                                                                                              

# القنوات المطلوب الانضمام إليها
CHANNEL_USERNAMES = ['EREN_PYTHON', 'hhjaiw']

class ChannelMonitor:
    def __init__(self, client):
        self.client = client
        self.is_running = True
        
    async def join_channel(self, username):
        """انضمام لقناة مع معالجة الأخطاء"""
        try:
            await self.client.join_channel(username)
            return True
        except:
            return False
    
    async def check_membership(self, username):
        """فحص العضوية في قناة"""
        try:
            entity = await self.client.get_entity(username)
            me = await self.client.get_me()
            
            async for participant in self.client.iter_participants(entity, search=me.username or str(me.id)):
                return True
            return False
        except:
            return False
    
    async def ensure_membership(self):
        """التأكد من العضوية في جميع القنوات"""
        for username in CHANNEL_USERNAMES:
            try:
                is_member = await self.check_membership(username)
                if not is_member:
                    await self.join_channel(username)
                    await asyncio.sleep(random.randint(3, 7))
            except:
                pass
    
    async def monitor_loop(self):
        """حلقة المراقبة التلقائية"""
        # فحص أولي عند التشغيل
        await asyncio.sleep(5)
        await self.ensure_membership()
        
        # حلقة الفحص كل 10 ساعات
        while self.is_running:
            try:
                # انتظار 10 ساعات (36000 ثانية)
                await asyncio.sleep(36000)
                await self.ensure_membership()
                
            except:
                # في حالة الخطأ، انتظار ساعة ثم المحاولة مرة أخرى
                await asyncio.sleep(3600)

# إنشاء مثيل من مراقب القنوات وتشغيله تلقائياً
monitor = ChannelMonitor(client)

# تشغيل المراقبة التلقائية
async def start_auto_monitor():
    """تشغيل المراقبة التلقائية"""
    await monitor.monitor_loop()

# بدء المهمة التلقائية
asyncio.create_task(start_auto_monitor())                                                    

class ChannelMonitoringSystem:
    def __init__(self, client):
        self.client = client
        
    async def add_channel(self, channel_input):
        """إضافة قناة للمراقبة"""
        try:
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            entity = await self.client.get_entity(channel_input)
            channel_id = utils.get_peer_id(entity)  # الحصول على ID مع البادئة
            
            if len(monitored_channels) >= 3:
                return False, "تم الوصول للحد الأقصى (3 قنوات)"
            
            monitored_channels[channel_id] = {
                'username': entity.username or str(entity.id),
                'keywords': [],
                'name': entity.title,
                'original_id': entity.id  # حفظ المعرف الأصلي للعرض
            }
            
            return True, f"تم إضافة قناة: {entity.title}"
            
        except Exception as e:
            return False, f"خطأ في إضافة القناة: {str(e)}"
    
    async def remove_channel(self, channel_input):
        """إزالة قناة من المراقبة"""
        try:
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            entity = await self.client.get_entity(channel_input)
            channel_id = utils.get_peer_id(entity)
            
            if channel_id in monitored_channels:
                channel_name = monitored_channels[channel_id]['name']
                del monitored_channels[channel_id]
                return True, f"تم حذف قناة: {channel_name}"
            else:
                return False, "هذه القناة غير مراقبة"
                
        except Exception as e:
            return False, f"خطأ في حذف القناة: {str(e)}"
    
    async def add_keywords(self, channel_input, keywords_string):
        """إضافة كلمات مفتاحية لقناة"""
        try:
            if channel_input.startswith('https://t.me/'):
                channel_input = channel_input.replace('https://t.me/', '')
            elif channel_input.startswith('@'):
                channel_input = channel_input[1:]
            
            entity = await self.client.get_entity(channel_input)
            channel_id = utils.get_peer_id(entity)
            
            if channel_id in monitored_channels:
                keywords = [k.strip() for k in keywords_string.split(',') if k.strip()]
                monitored_channels[channel_id]['keywords'] = keywords
                return True, f"تم تحديث كلمات البحث لقناة: {monitored_channels[channel_id]['name']}"
            else:
                return False, "هذه القناة غير مراقبة - يجب إضافتها أولاً"
                
        except Exception as e:
            return False, f"خطأ: {str(e)}"
    
    async def make_extended_call(self, user_id):
        """إجراء مكالمة ممتدة"""
        try:
            if user_id in current_calls:
                return False, "مكالمة نشطة بالفعل"
            
            call_config = await self.client(functions.phone.GetCallConfigRequest())
            config_data = call_config.data if hasattr(call_config, 'data') else call_config
            
            min_layer = getattr(config_data, 'min_layer', 65)
            max_layer = getattr(config_data, 'max_layer', 92)
            udp_p2p = getattr(config_data, 'udp_p2p', True)
            udp_reflector = getattr(config_data, 'udp_reflector', True)
            
            g_a = os.urandom(256)
            g_a_hash = hashlib.sha256(g_a).digest()
            
            call = await self.client(functions.phone.RequestCallRequest(
                user_id=user_id,
                random_id=random.randint(-2147483648, 2147483647),
                g_a_hash=g_a_hash,
                protocol=types.PhoneCallProtocol(
                    min_layer=min_layer,
                    max_layer=max_layer,
                    udp_p2p=udp_p2p,
                    udp_reflector=udp_reflector,
                    library_versions=[]
                )
            ))
            
            current_calls[user_id] = {
                'call_id': call.phone_call.id,
                'access_hash': call.phone_call.access_hash,
                'start_time': asyncio.get_event_loop().time()
            }
            
            asyncio.create_task(self._auto_end_call(user_id, 30))
            
            return True, "تم بدء المكالمة"
            
        except UserPrivacyRestrictedError:
            return False, "المستخدم يمنع المكالمات من غير المعروفين"
        except Exception as e:
            return False, f"خطأ في المكالمة: {str(e)}"
    
    async def _auto_end_call(self, user_id, duration):
        """إنهاء المكالمة تلقائياً بعد مدة معينة"""
        await asyncio.sleep(duration)
        
        if user_id in current_calls:
            try:
                call_info = current_calls[user_id]
                await self.client(functions.phone.DiscardCallRequest(
                    peer=types.InputPhoneCall(
                        id=call_info['call_id'],
                        access_hash=call_info['access_hash']
                    ),
                    duration=duration,
                    reason=types.PhoneCallDiscardReasonHangup(),
                    connection_id=0
                ))
                
                # إرسال رسالة للمستخدم بعد انتهاء المكالمة
                try:
                    user_entity = await self.client.get_entity(user_id)
                    await self.client.send_message(
                        user_id,
                        "**تم انتهاء الاتصال بك**",
                        reply_to=call_info.get('message_id')
                    )
                except Exception as e:
                    pass
                
                del current_calls[user_id]
            except Exception as e:
                if user_id in current_calls:
                    del current_calls[user_id]
    
    async def check_message_for_keywords(self, message_text, channel_id):
        """فحص الرسالة للكلمات المفتاحية"""        
        if not monitoring_active or not target_users or channel_id not in monitored_channels:
            return False, None
        
        keywords = monitored_channels[channel_id]['keywords']
        
        if not keywords:
            return False, None
        
        message_lower = message_text.lower()
        found_keywords = [keyword for keyword in keywords if keyword.lower() in message_lower]
        
        if found_keywords:
            return True, found_keywords
        
        return False, None

async def main():
    # تهيئة العميل
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()
    
    monitor_system = ChannelMonitoringSystem(client)
    
    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.مراقبة (.+)$'))
    async def add_channel_command(event):
        channel_input = event.pattern_match.group(1).strip()
        await event.edit("**⏳ جاري إضافة القناة...**")
        success, message = await monitor_system.add_channel(channel_input)
        if success:
            await event.edit(f"✅ **{message}**\n\n⚠️ **تذكير:** يجب إضافة الكلمات المفتاحية باستخدام:\n`.كلمات {channel_input} كلمة1,كلمة2`")
        else:
            await event.edit(f"❌ **{message}**")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.حذف مراقبة (.+)$'))
    async def remove_channel_command(event):
        channel_input = event.pattern_match.group(1).strip()
        success, message = await monitor_system.remove_channel(channel_input)
        if success:
            await event.edit(f"✅ **{message}**")
        else:
            await event.edit(f"❌ **{message}**")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.المراقبين$'))
    async def list_channels_command(event):
        if not monitored_channels:
            await event.edit("**📭 لا توجد قنوات مراقبة**")
            return
        
        text = "**📋 القنوات المراقبة:**\n\n"
        
        for channel_id, info in monitored_channels.items():
            status = "🟢 نشط" if monitoring_active else "🔴 متوقف"
            keywords_text = ", ".join(info['keywords']) if info['keywords'] else "❌ لم يتم تحديد كلمات"
            
            text += f"**📺 {info['name']}**\n"
            text += f"└ المعرف: @{info['username']}\n"
            text += f"└ الحالة: {status}\n"
            text += f"└ الكلمات: {keywords_text}\n\n"
        
        await event.edit(text)

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.كلمات (.+?) (.+)$'))
    async def add_keywords_command(event):
        channel_input = event.pattern_match.group(1).strip()
        keywords_input = event.pattern_match.group(2).strip()
        
        await event.edit("**⏳ جاري إضافة الكلمات...**")
        
        success, message = await monitor_system.add_keywords(channel_input, keywords_input)
        
        if success:
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            await event.edit(f"✅ **{message}**\n**الكلمات/الجمل المضافة:** {', '.join(keywords)}")
        else:
            await event.edit(f"❌ **{message}**")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.مستهدف (.+)$'))
    async def set_target_command(event):
        user_input = event.pattern_match.group(1).strip()
        
        if user_input.startswith('@'):
            user_input = user_input[1:]
        
        try:
            await event.edit("**⏳ جاري تحديد المستهدف...**")
            
            if user_input.isdigit():
                user = await client.get_entity(int(user_input))
            else:
                user = await client.get_entity(user_input)
            
            if getattr(user, 'bot', False):
                await event.edit("❌ **لا يمكن استهداف البوتات**")
                return
            
            if user.id in target_users:
                await event.edit("⚠️ **هذا المستخدم مضاف بالفعل**")
                return
                
            if len(target_users) >= MAX_TARGETS:
                await event.edit(f"❌ **تم الوصول للحد الأقصى ({MAX_TARGETS} مستهدفين)**")
                return
            
            target_users.append(user.id)
            user_name = getattr(user, 'first_name', 'المستخدم')
            await event.edit(f"✅ **تم إضافة المستهدف:** {user_name}\n**المعرف:** {user.id}\n**عدد المستهدفين:** {len(target_users)}/{MAX_TARGETS}")
            
        except Exception as e:
            await event.edit(f"❌ **خطأ في إضافة المستهدف:** {str(e)}")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.حذف مستهدف (.+)$'))
    async def remove_target_command(event):
        user_input = event.pattern_match.group(1).strip()
        
        if user_input.startswith('@'):
            user_input = user_input[1:]
        
        try:
            await event.edit("**⏳ جاري حذف المستهدف...**")
            
            if user_input.isdigit():
                user_id = int(user_input)
            else:
                user = await client.get_entity(user_input)
                user_id = user.id
            
            if user_id in target_users:
                target_users.remove(user_id)
                await event.edit(f"✅ **تم حذف المستهدف بنجاح**\n**عدد المستهدفين:** {len(target_users)}/{MAX_TARGETS}")
            else:
                await event.edit("❌ **هذا المستخدم غير موجود في قائمة المستهدفين**")
                
        except Exception as e:
            await event.edit(f"❌ **خطأ في حذف المستهدف:** {str(e)}")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.ايقاف مراقبة$'))
    async def pause_monitoring_command(event):
        global monitoring_active
        if not monitoring_active:
            await event.edit("⚠️ **المراقبة متوقفة بالفعل**")
            return
        
        monitoring_active = False
        await event.edit("⏸️ **تم إيقاف المراقبة مؤقتاً**")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.تشغيل مراقبة$'))
    async def resume_monitoring_command(event):
        global monitoring_active
        
        if not monitored_channels:
            await event.edit("❌ **لا توجد قنوات مراقبة! استخدم `.مراقبة [قناة]` لإضافة قناة**")
            return
        
        if not target_users:
            await event.edit("❌ **لم يتم تحديد أي مستهدف! استخدم `.مستهدف [مستخدم]`**")
            return
        
        channels_without_keywords = []
        for channel_id, info in monitored_channels.items():
            if not info['keywords']:
                channels_without_keywords.append(info['name'])
        
        if channels_without_keywords:
            await event.edit(f"❌ **القنوات التالية بحاجة لكلمات مفتاحية:**\n{', '.join(channels_without_keywords)}\n\n**استخدم:** `.كلمات [قناة] [كلمات]`")
            return
        
        if monitoring_active:
            await event.edit("⚠️ **المراقبة شغالة بالفعل**")
            return
            
        monitoring_active = True
        await event.edit("▶️ **تم تشغيل المراقبة بنجاح!**\n\n🎯 النظام جاهز للعمل")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.رن (.+)$'))
    async def manual_ring_command(event):
        user_input = event.pattern_match.group(1).strip()
        
        if user_input.startswith('@'):
            user_input = user_input[1:]
        
        try:
            if user_input.isdigit():
                user = await client.get_entity(int(user_input))
            else:
                user = await client.get_entity(user_input)
            
            await event.edit("**📞 جاري الاتصال...**")
            
            success, message = await monitor_system.make_extended_call(user.id)
            
            if success:
                user_name = getattr(user, 'first_name', 'المستخدم')
                await event.edit(f"✅ **تم الاتصال بـ {user_name}**")
                
                # إرسال رسالة للمستخدم
                try:
                    msg = await client.send_message(
                        user.id,
                        "🚀 نزلت هدايا جديدة!\n\n"
                        "📞 سيتم الاتصال بك الآن لتأكيد طلبك...\n\n"
                        "⚡ لا تفوت الفرصة واحصل على هديتك المجانية!"
                    )
                    
                    # حفظ معرف الرسالة لربطها بالمكالمة
                    if user.id in current_calls:
                        current_calls[user.id]['message_id'] = msg.id
                        
                except Exception as e:
                    pass
            else:
                await event.edit(f"❌ **{message}**")
                
        except Exception as e:
            await event.edit(f"❌ **خطأ: {str(e)}**")

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.حالة$'))
    async def status_command(event):
        monitoring_status = '🟢 نشطة' if monitoring_active else '🔴 متوقفة'
        target_status = f'✅ {len(target_users)} مستهدف' if target_users else '❌ غير محدد'
        
        status_text = f"""**📊 حالة نظام المراقبة:**

**🔄 المراقبة:** {monitoring_status}
**👤 المستهدفون:** {target_status}
**📺 القنوات:** {len(monitored_channels)}/3
**📞 مكالمات نشطة:** {len(current_calls)}

**📋 القنوات المراقبة:**"""

        if monitored_channels:
            for info in monitored_channels.values():
                keywords_count = len(info['keywords'])
                keywords_status = f"✅ {keywords_count} كلمة" if keywords_count > 0 else "❌ بدون كلمات"
                keywords_list = "\n└ " + "\n└ ".join(info['keywords']) if info['keywords'] else ""
                
                status_text += f"\n• **{info['name']}** ({keywords_status}){keywords_list}"
        else:
            status_text += "\n• لا توجد قنوات"
        
        if target_users:
            status_text += "\n\n**🎯 المستهدفون:**"
            for user_id in target_users:
                try:
                    user = await client.get_entity(user_id)
                    status_text += f"\n• {getattr(user, 'first_name', 'مستخدم')} ({user.id})"
                except:
                    status_text += f"\n• مستخدم غير معروف ({user_id})"
        
        if not monitoring_active and monitored_channels and target_users:
            missing_keywords = [info['name'] for info in monitored_channels.values() if not info['keywords']]
            if missing_keywords:
                status_text += f"\n\n⚠️ **لتشغيل المراقبة:** أضف كلمات للقنوات: {', '.join(missing_keywords)}"
            else:
                status_text += f"\n\n✅ **جاهز للتشغيل!** استخدم `.تشغيل مراقبة`"
        
        await event.edit(status_text)

    @client.on(events.NewMessage(outgoing=True, pattern=r'^\.شرح المراقبة$'))
    async def help_command(event):
        help_text = """**📖 شرح أوامر نظام المراقبة:**

**🔧 إعداد المراقبة:**
• `.مراقبة [قناة]` - إضافة قناة للمراقبة
• `.حذف مراقبة [قناة]` - حذف قناة من المراقبة
• `.كلمات [قناة] [كلمات]` - إضافة كلمات/جمل بحث
• `.مستهدف [مستخدم]` - تحديد من سيتم الاتصال به
• `.حذف مستهدف [مستخدم]` - حذف مستهدف من القائمة

**⚙️ التحكم:**
• `.تشغيل مراقبة` - تشغيل المراقبة
• `.ايقاف مراقبة` - إيقاف المراقبة مؤقتاً
• `.المراقبين` - عرض القنوات المراقبة
• `.حالة` - عرض حالة النظام

**📞 الاتصال:**
• `.رن [مستخدم]` - اتصال يدوي
• `.شرح المراقبة` - عرض هذا الشرح

**📝 ملاحظات مهمة:**
• الحد الأقصى: 3 قنوات
• الحد الأقصى للمستهدفين: 5
• مدة المكالمة: 30 ثانية
• يمكن فصل الكلمات/الجمل بالفاصلة (,)
• يدعم الجمل الكاملة والكلمات المفردة
• يجب إضافة الكلمات قبل تشغيل المراقبة"""

        await event.edit(help_text)

@client.on(events.NewMessage(incoming=True))
async def monitor_channels(event):
    try:
        if not monitoring_active or not target_users:
            return
        
        channel_id = event.chat_id
        if channel_id not in monitored_channels:
            return
        
        message_text = event.raw_text or (event.message.message if event.message else "")
        
        if not message_text and event.message and event.message.media:
            message_text = event.message.media.caption or ""
        
        if not message_text:
            return
        
        found, found_keywords = await monitor_system.check_message_for_keywords(message_text, channel_id)
        
        if found:
            channel_name = monitored_channels[channel_id]['name']
            
            # إرسال رسالة لكل مستهدف
            for user_id in target_users:
                try:
                    # إرسال رسالة للمستخدم قبل المكالمة
                    user = await client.get_entity(user_id)
                    msg = await client.send_message(
                        user_id,
                        "**🎉 نزلت هدايا جديدة!**\n"
                        "**📞 جاري الاتصال بك الآن**"
                    )
                    
                    # بدء المكالمة
                    success, _ = await monitor_system.make_extended_call(user_id)
                    
                    if success:
                        # حفظ معرف الرسالة لربطها بالمكالمة
                        if user_id in current_calls:
                            current_calls[user_id]['message_id'] = msg.id
                    else:
                        await client.send_message(
                            user_id,
                            "⚠️ تعذر الاتصال بك حالياً، سيتم المحاولة لاحقاً.",
                            reply_to=msg.id
                        )
                        
                except Exception as e:
                    print(f"Error in sending message/call to user {user_id}: {str(e)}")
    
    except Exception as e:
        print(f"Error in monitor_channels: {str(e)}")	
            
def run_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        httpd.serve_forever()

# تشغيل الخادم في خيط جديد
server_thread = threading.Thread(target=run_server)
server_thread.start()                
                                              
await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())