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
from PIL import Image
from pydub import AudioSegment
import hashlib
import string
import contextlib
import sys
from mutagen.id3 import ID3NoHeaderError
import glob
import tempfile
import aiofiles
import warnings
import shutil
import gc

# ========== مكتبات HTTP وطلبات الويب ==========
import requests
import httpx
import aiohttp

# ========== مكتبات الجهات الخارجية ==========
import yt_dlp
import pytz
from PIL import Image, ImageDraw, ImageFont
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import yt_dlp as youtube_dl
import youtube_dl as yt_dlp
from yt_dlp import YoutubeDL
from googletrans import Translator
from deep_translator import GoogleTranslator
from telethon import events, functions, types, utils
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from urllib.parse import urlparse
from http.cookiejar import MozillaCookieJar
from urllib.parse import quote

# ========== Telethon - استيراد رئيسي ==========
from telethon import TelegramClient, events, functions, types, Button
from telethon.sessions import StringSession
from telethon.tl.types import (
    DocumentAttributeAnimated, 
    DocumentAttributeAudio,
    InputMediaDice,
    DocumentAttributeAudio,
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

# ========== Telethon - الأخطاء ==========
from telethon.errors import (
    SessionPasswordNeededError,
    ChannelPrivateError,
    FileReferenceExpiredError,
    RPCError,
    UserPrivacyRestrictedError,
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError
)

# ========== Telethon - دوال API ==========
from telethon.tl.functions import (
    account,
    photos,
    messages,
    contacts,
    channels,
    phone,
    stories
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
from telethon.tl.functions.phone import GetCallConfigRequest

from asyncio.exceptions import CancelledError
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import psutil
from platform import python_version
from telethon import version
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo
from datetime import datetime
from telethon import events, functions, types
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty

# الحصول على المتغيرات من environment variables
API_ID = int(os.getenv('API_ID'))  # القيمة الافتراضية 29984076 إذا لم يتم تحديد المتغير

API_HASH = os.getenv('API_HASH')

STRING_SESSION = os.getenv('STRING_SESSION')

# ========== المستخدمون المصرح لهم ==========
AUTHORIZED_USERS = [
    int(uid.strip()) for uid in os.getenv("AUTHORIZED_USERS", "").split(",") if uid.strip().isdigit()
]

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


MAILSAC_API_KEY =os.getenv('MAILSAC_API_KEY') 

# -- Constants for Koyeb -- #
KOYEB_API_TOKEN = os.getenv("KOYEB_API_TOKEN")  # إضافة هذا السطر
UPSTREAM_REPO_URL = ("https://github.com/gyygfde3t4/Source00.git")  # ضع رابط الريبو الخاص بك
UPSTREAM_REPO_BRANCH = ("main")  #

# تخزين البريد الحالي
current_email = None
seen_ids = set()

# ========== حالات النظام ==========
is_auto_saving = False  # حالة الحفظ التلقائي

# ========== إعدادات عامة ==========
protection_enabled = False
accepted_users = {}
warned_users = {}
user_auto_messages = {}
MAX_WARNINGS = 7

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

monitored_channels = {}
target_users = []
current_calls = {}
monitoring_active = False
MAX_TARGETS = 5

# متغيرات التحكم
current_email = None
seen_ids = set()
monitoring_active = False
monitoring_task = None

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
9- ☆ `.تحديث البوت` - **تحديث البوت من السورس** ☆
10- ☆ `.حذف التنصيب` - **إيقاف البوت وحذف التنصيب** ☆
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
3- ☆ `.مكان الاسم اول` - **عرض الوقت في الاسم الأول** ☆
4- ☆ `.مكان الاسم اخير` - **عرض الوقت في الاسم الأخير** ☆
5- ☆ `.وقتيه1` - **زخرفة الأرقام بالنمط 𝟘𝟙𝟚𝟛** ☆
6- ☆ `.وقتيه2` - **زخرفة الأرقام بالنمط ⓪➀➁➂** ☆
7- ☆ `.وقتيه3` - **زخرفة الأرقام بالنمط ⓿➊➋➌** ☆
8- ☆ `.التوقيت` - **عرض قائمة التوقيتات المتاحة** ☆
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
1- ☆ `.الالعاب` - **لعبة تفاعلية مع البوت** ☆
2- ☆ `.تسلية` - **عرض أوامر التسلية** ☆
3- ☆ `.مسدس` - **رسم مسدس** ☆
4- ☆ `.كلب` - **رسم كلب** ☆
5- ☆ `.سبونج بوب` - **رسم شخصية سبونج بوب** ☆
6- ☆ `.إبرة` - **رسم إبرة** ☆
7- ☆ `.وحش` - **رسم وحش** ☆
8- ☆ `.مروحية` - **رسم مروحية** ☆
9- ☆ `.كت` - **سؤال عشوائي للتسلية** ☆
10- ☆ `.تخمين رقم` - **لعبة تخمين الرقم** ☆
11- ☆ `.لغز` - **لعبة الألغاز** ☆
12- ☆ `.تخمين انمي` - **لعبة تخمين شخصية الأنمي** ☆
13- ☆ `.قتل` + اسم - **لعبة قتل (فكاهي)** ☆
14- ☆ `.قاتل` + اسم - **لعبة قتل متقدمة (فكاهي)** ☆
15- ☆ `.تهكير` - **محاكاة عملية تهكير (فكاهي)** ☆
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
5- ☆ `.شرح المراقبة` - **شرح كيفية مراقبة المجموعات** ☆
6- ☆ `.بريد وهمي` - **إنشاء بريد إلكتروني وهمي** ☆
7- ☆ `.فحص البريد` - **فحص البريد الوارد للبريد الوهمي** ☆
8- ☆ `.ايقاف الوهمي` - **إيقاف البريد الوهمي** ☆
9- ☆ `.افتارات` - **قائمة صور الانمي (أولاد، بنات، ستوري، خيرني)** ☆
ٴ⋆─┄─┄─┄─ 𝐄𝐑𝐄𝐍 ─┄─┄─┄─⋆
    """
    if event.is_private or event.sender_id == (await event.client.get_me()).id:
        await event.edit(commands_message)
    else:
        await event.reply(commands_message)



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
name_position = 'first'  # Default to first name

# تحديث الاسم بناءً على الوقت والزخرفة المختارة
async def update_name(timezone_str, style='normal'):
    me = await client.get_me()
    current_time = get_local_time(timezone_str, style)
    
    if name_position == 'first':
        new_first_name = current_time
        new_last_name = me.last_name or ""
    else:
        new_first_name = me.first_name or ""
        new_last_name = current_time
    
    await client(UpdateProfileRequest(
        first_name=new_first_name,
        last_name=new_last_name
    ))

# الأمر لتفعيل الاسم التلقائي
@client.on(events.NewMessage(pattern=r'^\.الاسم التلقائي$'))
async def start_timed_update(event):
    global timed_update_running
    global current_style

    if not timed_update_running:
        timed_update_running = True
        await event.edit("**• جـارِ تفعيـل الاسـم الوقتـي ⅏. . .**")
        await asyncio.sleep(2)
        await event.edit(f"**⎉╎تـم بـدء الاسـم الوقتـي 🝛 .. بنجـاح ✓**\n**⎉╎المكان:** {'الاسم الأول' if name_position == 'first' else 'الاسم الأخير'}")
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

# أمر لتحديد مكان الاسم (أول أو آخر)
@client.on(events.NewMessage(pattern=r'^\.مكان الاسم (اول|اخير)$'))
async def set_name_position(event):
    global name_position
    global timed_update_running
    
    choice = event.pattern_match.group(1)
    if choice == 'اول':
        name_position = 'first'
    else:
        name_position = 'last'
    
    if timed_update_running:
        await event.edit(f"**✾╎تم تغيير مكان الاسم الوقتـي إلى {'الاسم الأول' if name_position == 'first' else 'الاسم الأخير'} .. بنجـاح✓**")
        # Update immediately to reflect the change
        await update_name(current_timezone, current_style)
    else:
        await event.edit(f"**✾╎تم تعيين مكان الاسم الوقتـي إلى {'الاسم الأول' if name_position == 'first' else 'الاسم الأخير'}**\n✾╎الان ارسـل ↶ `.الاسم التلقائي`")

# أمر لإيقاف الاسم التلقائي
@client.on(events.NewMessage(pattern=r'^\.ايقاف الاسم التلقائي$'))
async def stop_timed_update(event):
    global timed_update_running
    
    if timed_update_running:
        timed_update_running = False
        await event.edit("**⎉╎تـم إيقـاف الاسـم الوقتـي .. بنجـاح ✓**")
    else:
        await event.edit("**⚠️ الاسم التلقائي غير مفعل حالياً.**")

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
            try:
                await client.download_profile_photo(user.id, file=user_photo_path)
            except:
                user_photo_path = None
            
            # جمع المعلومات الأساسية
            user_id = user.id
            username = user.username if user.username else "غير متوفر"
            user_name = user.first_name or "غير متوفر"

            # البايو
            bio = "لا يوجد"
            try:
                user_full = await client(functions.users.GetFullUserRequest(user.id))
                if user_full.full_user.about:
                    bio = user_full.full_user.about
            except:
                bio = "لا يوجد"

            # الرتبة
            if user_id == 5683930416:
                rank = "مطـور السـورس 𓄂"
            else:
                rank = "مميز"

            # البريميوم
            account_type = "بريميوم" if getattr(user, 'premium', False) else "عادي"

            # عدد الصور
            try:
                photos = await client(GetUserPhotosRequest(user.id, offset=0, max_id=0, limit=100))
                num_photos = len(photos.photos)
            except:
                num_photos = "غير معروف"

            # حساب عدد الرسائل
            messages_count = 0
            try:
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
            except:
                messages_count = "غير معروف"

            # التفاعل
            interaction = "نشط" if isinstance(messages_count, int) and messages_count > 100 else "ضعيف"

            # تاريخ الإنشاء
            random.seed(user_id)
            year = "2023" if user_id > 6000000000 else "2022"
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            creation_date = f"{day}/{month}/{year}"

            # رسالة المعلومات بتنسيق Quote الحقيقي
            user_info_message = f"""<blockquote>⧉ مـعلومـات المسـتخـدم | سـورس إيــريــن
═════════════════════════════

✦ الاســم: {user_name}
✦ اليـوزر: @{username}
✦ الايـدي: {user_id}
✦ الرتبــه: {rank}
✦ الحساب: {account_type}
✦ الصـور: {num_photos}
✦ الرسائل: {messages_count}
✦ التفاعل: {interaction}
✦ الإنشـاء: {creation_date}
✦ البايـو: {bio}

⧉ قنـاة السـورس @EREN_PYTHON</blockquote>"""

            if user_photo_path:
                await client.send_file(
                    event.chat_id,
                    user_photo_path,
                    caption=user_info_message,
                    reply_to=event.reply_to_msg_id,
                    parse_mode='html'
                )
                # حذف الصورة
                try:
                    os.remove(user_photo_path)
                except:
                    pass
            else:
                await client.send_message(
                    event.chat_id,
                    user_info_message,
                    reply_to=event.reply_to_msg_id,
                    parse_mode='html'
                )
            
            await event.delete()
            
        else:
            await event.edit("**⚠️ لم أتمكن من العثور على معلومات عن هذا المستخدم.**")
    else:
        await event.edit("**⚠️ يرجى الرد على رسالة المستخدم للحصول على معلوماته.**")	

        
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


# ─── Bot Settings ───
StartTime = time.time()
EREN_VERSION = "2.0.0"
ALIVE_PIC = None  # Put image URL here if needed

# ─── Time Calculation Function ───
def get_readable_time(seconds: float) -> str:
    intervals = [
        ('y', 31536000),
        ('m', 2592000),
        ('w', 604800),
        ('d', 86400),
        ('h', 3600),
        ('m', 60),
        ('s', 1)
    ]
    result = []
    for name, count in intervals:
        value = int(seconds // count)
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")
    return ', '.join(result) if result else "0 s"

# ─── Check Command ───
@client.on(events.NewMessage(pattern=r'^\.(check|فحص)$'))
async def eren_check(event):
    try:
        # Start check
        start_time = datetime.now()
        check_msg = await event.edit("**⎆ Checking bot status...**")
        await asyncio.sleep(2)  # Dramatic wait 😄

        # Gather information
        user = await event.get_sender()
        user_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        ping_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Get user profile photo
        user_photo = None
        try:
            user_photo = await event.client.download_profile_photo(
                user.id,
                file=f"downloads/{user.id}.jpg",
                download_big=True
            )
        except Exception as photo_error:
            print(f"⚠️ Error downloading user photo: {photo_error}")

        # Final result
        result = f"""
┏━━━━━━━━━━━━━━━━━┓
┃  ◉ Sᴏᴜʀᴄᴇ EREN  ┃
┣━━━━━━━━━━━━━━━━━┫
┃ • ᴜsᴇʀ ➪ {user_name}
┃ • ᴠᴇʀsɪᴏɴ ➪ {EREN_VERSION}
┃ • ᴘʏᴛʜᴏɴ ➪ {python_version()}
┃ • ᴛᴇʟᴇᴛʜᴏɴ ➪ {version.__version__}
┃ • ᴘʟᴀᴛғᴏʀᴍ ➪ KOYEB
┃ • ᴘɪɴɢ ➪ {ping_time:.2f} ms
┃ • ᴜᴘᴛɪᴍᴇ ➪ {get_readable_time(time.time() - StartTime)}
┃ • sᴛᴀʀᴛᴇᴅ ➪ {datetime.fromtimestamp(StartTime).strftime('%Y/%m/%d %H:%M:%S')}
┃ • ᴅʙ sᴛᴀᴛᴜs ➪ ✅ Good
┃ • ᴄʜᴀɴɴᴇʟ ➪ [Eʀᴇɴ Yᴀ](https://t.me/ERENYA0)
┗━━━━━━━━━━━━━━━━━┛
"""

        # Send result with user photo
        if user_photo and os.path.exists(user_photo):
            await event.client.send_file(
                event.chat_id,
                user_photo,
                caption=result,
                reply_to=event.message.id
            )
            await check_msg.delete()
            # Clean up downloaded photo
            try:
                os.remove(user_photo)
            except:
                pass
        elif ALIVE_PIC:
            await event.client.send_file(
                event.chat_id,
                ALIVE_PIC,
                caption=result,
                reply_to=event.message.id
            )
            await check_msg.delete()
        else:
            await check_msg.edit(result)

    except Exception as e:
        await event.edit(f"**An error occurred:**\n`{str(e)}`")

# ─── Ping Command ───
@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def eren_ping(event):
    start = datetime.now()
    ping_msg = await event.edit("**🏓 Pong...**")
    end = datetime.now()
    ping_time = (end - start).total_seconds() * 1000
    await ping_msg.edit(f"**🏓 Ping:** `{ping_time:.2f} ms`")
                      

async def edit_or_reply(event, text):
    """دالة مساعدة للتعديل أو الرد"""
    if event.is_reply:
        return await event.reply(text)
    return await event.edit(text)

# ============ نظام الحماية ============

@client.on(events.NewMessage(pattern=r'^\.الحمايه تفعيل$'))
async def enable_protection(event):
    if not event.is_private or not await event.get_sender() == await client.get_me():
        return
    global protection_enabled
    protection_enabled = True
    await event.edit("**⎉╎تـم تفعيـل امـر حمايـه الخـاص .. بنجـاح 🔕☑️...**")

@client.on(events.NewMessage(pattern=r'^\.الحمايه تعطيل$'))
async def disable_protection(event):
    if not event.is_private or not await event.get_sender() == await client.get_me():
        return
    global protection_enabled
    protection_enabled = False
    await event.edit("**⎉╎تـم تعطيـل أمـر حمايـة الخـاص .. بنجـاح 🔔☑️...**")

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    global protection_enabled, user_auto_messages
    if not protection_enabled or not event.is_private:
        return

    sender = await event.get_sender()
    user_id = sender.id
    user_name = sender.first_name

    if user_id not in accepted_users and not sender.bot:
        # حذف الرسالة السابقة إن وجدت
        if user_id in user_auto_messages:
            try:
                await client.delete_messages(event.chat_id, user_auto_messages[user_id])
            except:
                pass

        # زيادة عدد التحذيرات
        warned_users[user_id] = warned_users.get(user_id, 0) + 1

        # إرسال التحذير
        reply_message = await event.respond(f"""
**ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - الـرد التلقـائي 〽️**
•─────────────────•
❞** مرحبـاً** {user_name} ❝
**⤶ قد اكـون مشغـول او غيـر موجـود حـاليـاً ؟!**
**⤶ ❨ لديـك هنا {warned_users[user_id]} مـن {MAX_WARNINGS} تحذيـرات ⚠️❩**
**⤶ لا تقـم بـ إزعاجـي والا سـوف يتم حظـرك تلقـائياً . . .**
**⤶ فقط قل سبب مجيئك وانتظـر الـرد ⏳**
        """)
        
        user_auto_messages[user_id] = reply_message.id

        # الحظر عند الوصول للحد الأقصى
        if warned_users[user_id] >= MAX_WARNINGS:
            await event.respond("**❌ تم حظرك تلقائياً بسبب تكرار الإزعاج.**")
            await client(BlockRequest(user_id))
            if user_id in user_auto_messages:
                del user_auto_messages[user_id]

@client.on(events.NewMessage(pattern=r'^\.قبول$'))
async def accept_user(event):
    if not event.is_private or not await event.get_sender() == await client.get_me():
        return
        
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("**⎉╎يجب الرد على رسالة المستخدم لقبوله**")
    
    user = await client.get_entity(reply.sender_id)
    accepted_users[user.id] = {'name': user.first_name, 'reason': "لم يذكر"}
    
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

@client.on(events.NewMessage(pattern=r'^\.رفض$'))
async def reject_user(event):
    if not event.is_private or not await event.get_sender() == await client.get_me():
        return
        
    reply = await event.get_reply_message()
    if not reply:
        return await event.edit("**⎉╎يجب الرد على رسالة المستخدم لرفضه**")
    
    user = await client.get_entity(reply.sender_id)
    await client(BlockRequest(user.id))
    
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

@client.on(events.NewMessage(pattern=r'^\.المقبولين$'))
async def show_accepted(event):
    if not event.is_private or not await event.get_sender() == await client.get_me():
        return
        
    if not accepted_users:
        return await event.edit("**لا يوجد مستخدمين مقبولين حالياً.**")
    
    message = "⎉╎ قائمـة المسمـوح لهـم ( المقبـوليـن ) :\n\n"
    for user_id, info in accepted_users.items():
        user = await client.get_entity(user_id)
        message += f"• 👤 **الاسـم :** {info['name']}\n⎉╎ **الايـدي :** {user_id}\n⎉╎ **المعـرف :** @{user.username}\n⎉╎ **السـبب :** {info['reason']}\n\n"
    
    await event.edit(message)

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
    if not event.out:  # يستجيب فقط للمستخدم الأصلي
        return

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
    # التحقق من أن المرسل هو المستخدم الأصلي فقط
    if not event.out:
        return
    
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
    if not event.out:  # يستجيب فقط للمستخدم الأصلي
        return
    
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
                await event.edit("🔄 جاري تسجيل اللاعبين... اكتب `انا` للانضمام!")
            else:
                await event.edit("⏳ هناك لعبة نشطة بالفعل! استخدموا المحاولات المتاحة.")
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
💡 القواعد:
- يمكن التخمين بالإنجليزية/اليابانية (العربية قريباً) 
- إذا خمنت الاسم بنسبة تطابق 70% ستفوز
- أول إجابة صحيحة تفوز!
- لديكم {} محاولات مشتركة
- للإنضمام اكتب: انا
""".format(5 * player_count)

        # إرسال رسالة جديدة بدلاً من تحرير الرسالة الأصلية
        registration_msg = await event.edit(
            "🎮 لعبة تخمين الأنمي - وضع الجماعي\n\n"
            f"👥 عدد اللاعبين المطلوب: {player_count}\n"
            f"🖊️ اللاعب 1: {sender.first_name}\n\n"
            f"{rules_text}\n"
            "⏳ انتظار اللاعبين . . .\n"
            "(اكتب .انهاء تخمين لإلغاء اللعبة)",
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
            "game_ended": False,
            "chat_id": event.chat_id  # حفظ chat_id للاستخدام لاحقاً
        }

        if player_count == 1:
            await start_anime_game_session(event.chat_id)

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

        # حذف رسالة العد التنازلي السابقة إن وجدت
        if game.get("countdown_message"):
            try:
                await game["countdown_message"].delete()
                game["countdown_message"] = None
            except:
                pass
        
        countdown_msg = await event.reply(
            "🎮 لعبة تخمين الأنمي - وضع الجماعي\n\n"
            f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
            f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
            f"{players_list}\n\n"
            "⏳ سيتم بدأ اللعبة بعد 10 ثوان...",
            parse_mode='html'
        )
        
        game["countdown_message"] = countdown_msg
        game["game_messages"].append(countdown_msg)
        
        if game["registered"] >= game["required_players"]:
            for i in range(9, 0, -1):
                await asyncio.sleep(1)
                try:
                    await countdown_msg.edit(
                        "🎮 لعبة تخمين الأنمي - وضع الجماعي\n\n"
                        f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
                        f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
                        f"{players_list}\n\n"
                        f"⏳ سيتم بدأ اللعبة بعد {i} ثوان...",
                        parse_mode='html'
                    )
                except:
                    pass
            
            try:
                await countdown_msg.edit(
                    "🎮 لعبة تخمين الأنمي - وضع الجماعي\n\n"
                    f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
                    f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
                    f"{players_list}\n\n"
                    "⏳ سيتم بدأ اللعبة بعد قليل...",
                    parse_mode='html'
                )
            except:
                pass
                
            await asyncio.sleep(2)
            
            await start_anime_game_session(event.chat_id)

async def start_anime_game_session(chat_id):
    """بدء لعبة تخمين الأنمي - تم إصلاح المعامل ليكون chat_id بدلاً من event"""
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
        
        # تحديث رسالة العد التنازلي
        if game.get("countdown_message"):
            try:
                await game["countdown_message"].edit(
                    "🎮 لعبة تخمين الأنمي - وضع الجماعي\n\n"
                    f"👥 عدد اللاعبين المطلوب: {game['required_players']}\n"
                    f"🖊️ اللاعبون المسجلون ({game['registered']}/{game['required_players']}):\n"
                    f"{players_list}\n\n"
                    "✅ لقد بدأت اللعبة!",
                    parse_mode='html'
                )
            except:
                pass
        
        caption = (
            "🎌 بدأت لعبة تخمين الأنمي!\n\n"
            f"👥 اللاعبون:\n{players_list}\n\n"
            f"🎯 المحاولات المتاحة: {game['remaining_attempts']}\n"
            f"💡 اكتبوا تخميناتكم الآن!"
        )
        
        try:
            sent_msg = await client.send_file(chat_id, character["image"], caption=caption, parse_mode='html')
            game["game_messages"].append(sent_msg)
        except Exception as img_error:
            print(f"خطأ في إرسال الصورة: {img_error}")
            sent_msg = await client.send_message(
                chat_id, 
                caption + f"\n🖼️ [اضغط هنا لرؤية الصورة]({character['image']})", 
                parse_mode='html'
            )
            game["game_messages"].append(sent_msg)

    except Exception as e:
        print(f"خطأ في بدء اللعبة: {e}")
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
                character.get("name_native", "")
            ] + character.get("nicknames", [])
            
            # تنظيف الأسماء وإزالة القيم الفارغة
            correct_names = [name for name in correct_names if name and isinstance(name, str) and len(name.strip()) > 0]
            
            is_correct = any(
                similar(guess, name)
                for name in correct_names
            )
            
            if is_correct:
                game["players"][player_id]["guessed"] = True
                game["game_ended"] = True
                winner = game["players"][player_id]["name"]
                
                message = (
                    "✨ تهانينا! لقد فاز {winner_name} ✨\n\n"
                    "🎯 التخمين الصحيح:\n"
                    f"🏷️ الاسم: {character['name']}"
                ).format(winner_name=winner.first_name)
                
                if character.get("name_native"):
                    message += f" ({character['name_native']})"
                
                message += f"\n📺 الأنمي: {character['anime']}\n\n"
                
                if character.get("url"):
                    message += f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
                
                await event.reply(message, link_preview=False, parse_mode='html')
                del anime_games[event.chat_id]
                return
            
            if game["remaining_attempts"] <= 0:
                game["game_ended"] = True
                message = (
                    "💔 انتهت جميع المحاولات!\n\n"
                    "🔎 الإجابة الصحيحة كانت:\n"
                    f"🏷️ الاسم: {character['name']}"
                )
                
                if character.get("name_native"):
                    message += f" ({character['name_native']})"
                    
                message += f"\n📺 الأنمي: {character['anime']}\n\n"
                
                if character.get("url"):
                    message += f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
                
                await event.reply(message, link_preview=False, parse_mode='html')
                del anime_games[event.chat_id]
            else:
                remaining = game["remaining_attempts"]
                attempts_word = "محاولة" if remaining == 1 else "محاولات"
                reply_msg = await event.reply(
                    f"❌ تخمين خاطئ!\n"
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
    # التحقق من أن المرسل هو المستخدم الأصلي فقط
    if not event.out:
        return
    
    if event.chat_id not in anime_games:
        await event.reply("⚠️ لا توجد لعبة نشطة لإنهائها")
        return
    
    async with message_locks[event.chat_id]:
        if event.chat_id not in anime_games:
            await event.reply("⚠️ لا توجد لعبة نشطة لإنهائها")
            return
            
        game = anime_games[event.chat_id]
        
        character = game.get("character")
        
        if character:
            message = (
                "🛑 تم إنهاء اللعبة!\n\n"
                "🔎 الإجابة الصحيحة كانت:\n"
                f"🏷️ الاسم: {character['name']}"
            )
            
            if character.get("name_native"):
                message += f" ({character['name_native']})"
                
            message += f"\n📺 الأنمي: {character['anime']}\n\n"
            
            if character.get("url"):
                message += f"🔗 [اضغط هنا للمزيد عن الشخصية]({character['url']})"
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
            
            for chat_id, game in list(anime_games.items()):
                # اذا مر 5 دقائق دون تخمين توقف اللعبة او اثناء التسجيل 
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


@client.on(events.NewMessage(pattern=r'^\.لصوره$'))
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

@client.on(events.NewMessage(pattern=r'^\.حول بصمه$'))
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


@client.on(events.NewMessage(pattern=r'^\.حول صوت$'))
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

@client.on(events.NewMessage(pattern=r'^\.لمتحرك$'))
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




@client.on(events.NewMessage(pattern=r'^\.لمتحركه$'))
async def handler(event):
    # التحقق من وجود رسالة رد تحتوي على فيديو
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()

        if reply_message.video:
            # إرسال رسالة "جاري التحويل..." والاحتفاظ بها
            processing_message = await event.edit("**جاري التحويل...**")

            try:
                # تشغيل التحويل في مهمة منفصلة
                await convert_video_to_gif_async(event, reply_message, processing_message)
            except Exception as e:
                await processing_message.edit(f"**حدث خطأ:** {e}")
                
        else:
            await event.edit("**يرجى الرد على فيديو.**")
    else:
        await event.edit("**يرجى الرد على فيديو.**")

async def convert_video_to_gif_async(event, reply_message, processing_message):
    """تحويل الفيديو إلى GIF بشكل غير متزامن"""
    
    # تحميل الفيديو
    file_path = await reply_message.download_media()
    gif_path = file_path.split('.')[0] + ".gif"
    
    try:
        # الحصول على معلومات الفيديو
        original_fps = await get_video_fps_async(file_path)
        
        # تحسين إعدادات التحويل للسرعة
        target_fps = min(original_fps, 15)  # تقليل FPS للسرعة
        max_duration = 6  # تقليل المدة القصوى
        
        # تحويل بإعدادات محسّنة للسرعة
        success = await convert_with_timeout(
            file_path, gif_path, target_fps, max_duration, timeout=45
        )
        
        if not success:
            # إذا فشل التحويل الأول، جرب بإعدادات أبسط
            success = await convert_simple_gif(file_path, gif_path, timeout=30)
        
        if success:
            # التحقق من حجم الملف
            if await check_and_resize_gif(file_path, gif_path):
                # إرسال GIF
                await client.send_file(
                    event.chat_id, 
                    gif_path, 
                    caption="**تم التحويل بنجاح! 🎬**"
                )
                
                # حذف رسالة "جاري التحويل..."
                await processing_message.delete()
                # حذف الرسالة الأصلية
                await event.delete()
            else:
                await processing_message.edit("**الملف كبير جداً للإرسال**")
        else:
            await processing_message.edit("**انتهت مهلة التحويل (45 ثانية)**")
            
    except Exception as e:
        await processing_message.edit(f"**خطأ في التحويل:** {str(e)[:100]}")
    finally:
        # حذف الملفات المؤقتة
        cleanup_files(file_path, gif_path)

async def get_video_fps_async(file_path):
    """الحصول على FPS الفيديو بشكل غير متزامن"""
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json', 
            '-show_streams', '-select_streams', 'v:0', file_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, _ = await asyncio.wait_for(process.communicate(), timeout=10)
        
        video_info = json.loads(stdout.decode())
        fps_str = video_info['streams'][0].get('r_frame_rate', '30/1')
        
        if '/' in fps_str:
            num, den = fps_str.split('/')
            return int(float(num) / float(den))
        return 30
        
    except:
        return 30

async def convert_with_timeout(file_path, gif_path, fps, duration, timeout=45):
    """تحويل مع timeout محدد"""
    try:
        cmd = [
            'ffmpeg', '-y',
            '-i', file_path,
            '-vf', f'fps={fps},scale=400:-1:flags=fast_bilinear',
            '-t', str(duration),
            '-c:v', 'gif',
            gif_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await asyncio.wait_for(process.communicate(), timeout=timeout)
        return process.returncode == 0
        
    except asyncio.TimeoutError:
        try:
            process.terminate()
            await process.wait()
        except:
            pass
        return False
    except:
        return False

async def convert_simple_gif(file_path, gif_path, timeout=30):
    """تحويل مبسط كخيار احتياطي"""
    try:
        cmd = [
            'ffmpeg', '-y',
            '-i', file_path,
            '-vf', 'fps=10,scale=320:-1',
            '-t', '4',
            gif_path
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await asyncio.wait_for(process.communicate(), timeout=timeout)
        return process.returncode == 0
        
    except:
        return False

async def check_and_resize_gif(file_path, gif_path):
    """فحص حجم GIF وتصغيره إذا لزم الأمر"""
    max_size = 8 * 1024 * 1024  # 8 MB
    
    if not os.path.exists(gif_path):
        return False
        
    file_size = os.path.getsize(gif_path)
    
    if file_size <= max_size:
        return True
    
    # إعادة تحويل بحجم أصغر
    try:
        temp_gif = gif_path + ".temp"
        cmd = [
            'ffmpeg', '-y',
            '-i', file_path,
            '-vf', 'fps=8,scale=240:-1',
            '-t', '3',
            temp_gif
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await asyncio.wait_for(process.communicate(), timeout=20)
        
        if process.returncode == 0 and os.path.exists(temp_gif):
            os.replace(temp_gif, gif_path)
            return os.path.getsize(gif_path) <= max_size
            
    except:
        pass
    
    return False

def cleanup_files(*file_paths):
    """حذف الملفات بأمان"""
    for file_path in file_paths:
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass



def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@mailsac.com"

def fetch_inbox(email):
    inbox_url = f"https://mailsac.com/api/addresses/{email}/messages"
    headers = {"Mailsac-Key": MAILSAC_API_KEY}
    response = requests.get(inbox_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def fetch_message(email, message_id):
    url = f"https://mailsac.com/api/text/{email}/{message_id}"
    headers = {"Mailsac-Key": MAILSAC_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return "❌ فشل في جلب الرسالة."

async def is_developer(user_id):
    me = await client.get_me()
    return user_id == me.id or user_id in AUTHORIZED_USERS

async def respond(event, message, **kwargs):
    try:
        if event.out:
            return await event.edit(message, **kwargs)
        else:
            return await event.reply(message, **kwargs)
    except:
        return await event.reply(message, **kwargs)

@client.on(events.NewMessage(pattern=r'^\.بريد وهمي$'))
async def create_temp_mail(event):
    global current_email, seen_ids, monitoring_active, monitoring_task
    
    if monitoring_task and not monitoring_task.done():
        monitoring_task.cancel()
    
    seen_ids = set()
    current_email = generate_random_email()
    monitoring_active = True
    
    is_dev = await is_developer(event.sender_id)
    
    response_text = (
        f"📧 **تم إنشاء بريد وهمي جديد:**\n"
        f"`{current_email}`\n"
        f"📬 رابط الصندوق: https://mailsac.com/inbox/{current_email.split('@')[0]}\n"
        f"🔄 سيتم فحص الرسائل كل 5 ثواني...\n"
        f"⏹ استخدم `.ايقاف الوهمي` لإيقاف المراقبة"
    )
    
    message = await respond(event, response_text)

    async def monitor_inbox():
        try:
            while monitoring_active:
                messages = fetch_inbox(current_email)
                new_messages = [msg for msg in messages if msg['_id'] not in seen_ids]

                if new_messages:
                    for msg in new_messages:
                        seen_ids.add(msg['_id'])
                        body = fetch_message(current_email, msg['_id'])

                        sender_data = msg.get('from', [])
                        if isinstance(sender_data, list) and sender_data:
                            sender_email = sender_data[0].get('address', 'غير معروف')
                        elif isinstance(sender_data, str):
                            sender_email = sender_data
                        else:
                            sender_email = 'غير معروف'

                        msg_content = (
                            f"📬 **رسالة جديدة وصلت!**\n\n"
                            f"👤 من: `{sender_email}`\n"
                            f"📌 الموضوع: `{msg.get('subject', 'بدون')}`\n\n"
                            f"📝 المحتوى:\n{body[:1000]}"
                        )

                        if is_dev:
                            await event.reply(msg_content)
                        else:
                            current_text = message.text
                            if msg_content not in current_text:
                                new_text = f"{current_text}\n\n{msg_content}"
                                try:
                                    await message.edit(new_text)
                                except:
                                    message = await event.reply(new_text)
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            error_msg = f"⚠️ خطأ أثناء المراقبة: {e}"
            await respond(event, error_msg)

    monitoring_task = asyncio.create_task(monitor_inbox())

@client.on(events.NewMessage(pattern=r'^\.فحص البريد$'))
async def check_mail(event):
    if not current_email:
        error_msg = "⚠️ لا يوجد بريد حاليًا. استخدم `.بريد وهمي` أولاً."
        await respond(event, error_msg)
        return

    messages = fetch_inbox(current_email)
    response_msg = (
        f"📬 **فحص البريد المؤقت**\n\n"
        f"• البريد: `{current_email}`\n"
        f"• عدد الرسائل المستلمة: `{len(messages)}`\n"
        f"• [رابط الصندوق](https://mailsac.com/inbox/{current_email.split('@')[0]})"
    )

    await respond(event, response_msg, link_preview=False)

@client.on(events.NewMessage(pattern=r'^\.ايقاف الوهمي$'))
async def stop_monitoring(event):
    global monitoring_active, monitoring_task
    
    if not current_email:
        await respond(event, "⚠️ لا يوجد بريد وهمي نشط حالياً.")
        return
    
    if monitoring_task:
        monitoring_active = False
        monitoring_task.cancel()
        try:
            await monitoring_task
        except:
            pass
    
    await respond(event, f"✅ تم إيقاف مراقبة البريد الوهمي: `{current_email}`")

            
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
            
            call_config = await self.client(GetCallConfigRequest())
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
                    pass
    
    except Exception as e:
        pass

async def main():
    await client.start()

    
    try:
        me = await client.get_me()
        print(f"👤 تم تسجيل الدخول باسم: {me.first_name}")
        print(f"🆔 معرف الحساب: {me.id}")
        if me.username:
            print(f"📝 اسم المستخدم: @{me.username}")
        print("=" * 50)
    except Exception as e:
        pass
 
@client.on(events.NewMessage(pattern=r'^\.افتارات$'))
async def show_avatars_menu(event):
    avatars_message = """
╭━━━┳━━━━╮
**قائمة صور الأنـمـي ⎚**
╰━━━┻━━━━╯
ٴ⋆─┄─┄─┄─ 𝐀𝐕𝐀𝐓𝐀𝐑 ─┄─┄─┄─⋆
1- ☆ `.ولد انمي` - **صورة ولد أنمي عشوائية** ☆
2- ☆ `.بنت انمي` - **صورة بنت أنمي عشوائية** ☆
3- ☆ `.خيرني` - **صورة "لو خيروك" عشوائية** ☆
4- ☆ `.ستوري انمي` - **لعرض ستوري أنمي** ☆
5- ☆ `.صور + اسم + عدد` - **لإرسال صور حسب الطلب** ☆
ٴ⋆─┄─┄─┄─ 𝐀𝐕𝐀𝐓𝐀𝐑 ─┄─┄─┄─⋆
    """
    if event.is_private or event.sender_id == (await event.client.get_me()).id:
        await event.edit(avatars_message)
    else:
        await event.reply(avatars_message)                                                                                         
async def edit_or_reply(event, text):
    """دالة مساعدة للتعديل أو الرد"""
    if event.is_reply:
        return await event.reply(text)
    return await event.edit(text)

@client.on(events.NewMessage(pattern=r'^\.ستوري انمي$'))
async def anime_story(event):
    if not event.out:  # يستجيب فقط إذا كان المرسل هو المستخدم الأصلي
        return
    try:
        zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الستـوري ...**")
        sources = ["@animeforlovers", "@ANIME_editsssss"]
        stories = []
        
        for source in sources:
            async for msg in client.iter_messages(source, filter=InputMessagesFilterVideo):
                stories.append(msg)
        
        if not stories:
            return await zzevent.edit("**╮•⎚ لا توجد ستوريات متاحة حالياً**")
        
        selected = random.choice(stories)
        caption = """0:10━❍──────── -1:00
↻     ⊲  Ⅱ  ⊳     ↺
VOLUME: ▁▂▃▄▅▆▇ 100%
╔═.✵.══════════╗
✵ #Stories  
✵ #Anime_Edit 
✵ Channel: @PP2P6
╚══════════.✵.═╝"""
        
        await client.send_file(
            event.chat_id,
            file=selected,
            caption=caption
        )
        await zzevent.delete()
    except Exception as e:
        await event.reply(f"**حدث خطأ: {str(e)}**")

@client.on(events.NewMessage(pattern=r'^\.خيرني$'))
async def choice_game(event):
    if not event.out:  # يستجيب فقط إذا كان المرسل هو المستخدم الأصلي
        return
    try:
        zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ التحميل ...**")
        images = []
        async for msg in client.iter_messages("@SourceSaidi", filter=InputMessagesFilterPhotos):
            images.append(msg)
        
        if not images:
            return await zzevent.edit("**╮•⎚ لا توجد صور متاحة حالياً**")
        
        await client.send_file(
            event.chat_id,
            file=random.choice(images),
            caption="**✦┊لـو خيـروك ➧⁉️🌉◟**"
        )
        await zzevent.delete()
    except Exception as e:
        await event.reply(f"**حدث خطأ: {str(e)}**")

@client.on(events.NewMessage(pattern=r'^\.ولد انمي$'))
async def anime_boy(event):
    if not event.out:  # يستجيب فقط إذا كان المرسل هو المستخدم الأصلي
        return
    try:
        zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ التحميل ...**")
        images = []
        async for msg in client.iter_messages("@sou00l", filter=InputMessagesFilterPhotos):
            images.append(msg)
        
        if not images:
            return await zzevent.edit("**╮•⎚ لا توجد صور متاحة حالياً**")
        
        await client.send_file(
            event.chat_id,
            file=random.choice(images),
            caption="**◞افتـارات آنمي شبـاب ➧🎆🙋🏻‍♂◟**"
        )
        await zzevent.delete()
    except Exception as e:
        await event.reply(f"**حدث خطأ: {str(e)}**")

@client.on(events.NewMessage(pattern=r'^\.بنت انمي$'))
async def anime_girl(event):
    if not event.out:  # يستجيب فقط إذا كان المرسل هو المستخدم الأصلي
        return
    try:
        zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ التحميل ...**")
        images = []
        async for msg in client.iter_messages("@sougir0", filter=InputMessagesFilterPhotos):
            images.append(msg)
        
        if not images:
            return await zzevent.edit("**╮•⎚ لا توجد صور متاحة حالياً**")
        
        await client.send_file(
            event.chat_id,
            file=random.choice(images),
            caption="**◞افتـارات آنمي بنـات ➧🎆🧚🏻‍♀◟**"
        )
        await zzevent.delete()
    except Exception as e:
        await event.reply(f"**حدث خطأ: {str(e)}**")
                                                             

# شروط الفوز لكل لعبة
WIN_CONDITIONS = {
    "🎯": 6,    # السهم - الفوز عند الحصول على 6 (في المنتصف)
    "🎲": 6,     # النرد - الفوز عند الحصول على 6
    "🏀": 5,     # كرة السلة - الفوز عند الحصول على 5
    "⚽️": 5,    # كرة القدم - الفوز عند الحصول على 5
    "🎰": 64    # ماكينة الحظ - الفوز عند الحصول على 64 (جاكبوت)
}

async def edit_or_reply(event, text, **kwargs):
    """دالة مساعدة للتعديل أو الرد"""
    try:
        if hasattr(event, 'edit'):
            return await event.edit(text, **kwargs)
        else:
            return await event.reply(text, **kwargs)
    except:
        return await event.reply(text, **kwargs)

@client.on(events.NewMessage(pattern=r'^\.الالعاب$'))
async def games_menu(event):
    """عرض قائمة الألعاب"""
    menu = """
🎮 **قائمة الألعاب الجماعية**:

1. `.اكس او` - لعبة XO ضد البوت (فردية)
2. `.سهم [عدد اللاعبين]` - لعبة السهام (🎯)
3. `.نرد [عدد اللاعبين]` - لعبة النرد (🎲)
4. `.سله [عدد اللاعبين]` - كرة السلة (🏀)
5. `.كرة [عدد اللاعبين]` - كرة القدم (⚽️)
6. `.حظ [عدد اللاعبين]` - ماكينة الحظ (🎰)
7. `.ايقاف` - إيقاف اللعبة الحالية

📌 مثال: `.سهم 3` - لعبة سهام لـ3 لاعبين
"""
    await edit_or_reply(event, menu)

@client.on(events.NewMessage(pattern=r'^\.اكس او$'))
async def xo_game(event):
    """لعبة XO مع البوت"""
    bot_username = "@xobot"
    try:
        zzevent = await edit_or_reply(event, "**⚔️ جاري بدء لعبة XO...**")
        tap = await client.inline_query(bot_username, "play")
        await tap[0].click(event.chat_id)
        await zzevent.delete()
    except Exception as e:
        await edit_or_reply(event, f"**⚠️ حدث خطأ:** {str(e)}")

@client.on(events.NewMessage(pattern=r'^\.(سهم|نرد|سله|كرة|حظ)(?:\s+(\d+))?$'))
async def start_game(event):
    """بدء لعبة جماعية"""
    game_types = {
        "سهم": "🎯",
        "نرد": "🎲", 
        "سله": "🏀",
        "كرة": "⚽️",
        "حظ": "🎰"
    }
    game_type = game_types[event.pattern_match.group(1)]
    win_condition = WIN_CONDITIONS[game_type]
    
    chat_id = event.chat_id
    sender = await event.get_sender()
    
    try:
        player_count = int(event.pattern_match.group(2)) if event.pattern_match.group(2) else 1
        if player_count < 1 or player_count > 10:
            raise ValueError
    except:
        await edit_or_reply(event, "**⚠️ يرجى إدخال عدد صحيح بين 1 و 10**")
        return

    if chat_id in active_games:
        await edit_or_reply(event, "**⏳ هناك لعبة نشطة بالفعل!**")
        return

    zzevent = await edit_or_reply(event, "**⚡ جاري إعداد اللعبة...**")
    
    active_games[chat_id] = {
        "game_type": game_type,
        "win_condition": win_condition,
        "status": "registering",
        "players": {str(event.sender_id): {"name": sender, "score": 0}},
        "required_players": player_count,
        "current_player": 0,
        "registration_msg": zzevent,
        "game_messages": [],
        "chat_id": chat_id
    }

    players_list = f"1. {sender.first_name}"
    try:
        await zzevent.edit(
            f"{game_type} **بدء لعبة جديدة**\n\n"
            f"🏆 **شرط الفوز:** الحصول على {win_condition} نقاط\n"
            f"👤 **اللاعبون** (1/{player_count}):\n{players_list}\n\n"
            "📝 للانضمام اكتب: `انا`\n"
            "🛑 للإيقاف اكتب: `.ايقاف`"
        )
    except:
        # إذا فشل التعديل، أرسل رسالة جديدة
        new_msg = await event.reply(
            f"{game_type} **بدء لعبة جديدة**\n\n"
            f"🏆 **شرط الفوز:** الحصول على {win_condition} نقاط\n"
            f"👤 **اللاعبون** (1/{player_count}):\n{players_list}\n\n"
            "📝 للانضمام اكتب: `انا`\n"
            "🛑 للإيقاف اكتب: `.ايقاف`"
        )
        active_games[chat_id]["registration_msg"] = new_msg

@client.on(events.NewMessage(pattern=r'^انا$'))
async def register_player(event):
    """تسجيل لاعب جديد"""
    chat_id = event.chat_id
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    if game["status"] != "registering":
        return

    player_id = str(event.sender_id)
    if player_id in game["players"]:
        await event.reply("**✅ أنت مسجل بالفعل في اللعبة!**")
        return

    sender = await event.get_sender()
    game["players"][player_id] = {"name": sender, "score": 0}

    players = "\n".join(
        f"{idx+1}. {p['name'].first_name}"
        for idx, p in enumerate(game["players"].values())
    )
    
    try:
        await game["registration_msg"].edit(
            f"{game['game_type']} **بدء لعبة جديدة**\n\n"
            f"🏆 **شرط الفوز:** الحصول على {game['win_condition']} نقاط\n"
            f"👤 **اللاعبون** ({len(game['players'])}/{game['required_players']}):\n{players}\n\n"
            "📝 للانضمام اكتب: `انا`\n"
            "🛑 للإيقاف اكتب: `.ايقاف`"
        )
    except:
        # إذا فشل التعديل، أرسل رسالة جديدة
        new_msg = await event.reply(
            f"{game['game_type']} **بدء لعبة جديدة**\n\n"
            f"🏆 **شرط الفوز:** الحصول على {game['win_condition']} نقاط\n"
            f"👤 **اللاعبون** ({len(game['players'])}/{game['required_players']}):\n{players}\n\n"
            "📝 للانضمام اكتب: `انا`\n"
            "🛑 للإيقاف اكتب: `.ايقاف`"
        )
        game["registration_msg"] = new_msg

    if len(game["players"]) >= game["required_players"]:
        await start_game_round(chat_id)

async def start_game_round(chat_id):
    """بدء جولة اللعبة"""
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    game["status"] = "playing"
    players = list(game["players"].values())
    current_player = players[game["current_player"]]
    
    try:
        await game["registration_msg"].delete()
    except:
        pass

    try:
        game_msg = await client.send_message(
            chat_id,
            f"{game['game_type']} **دور اللاعب:** {current_player['name'].first_name}\n\n"
            "🎮 اكتب `ارمي` لرمي النرد!\n"
            f"🏆 **شرط الفوز:** الحصول على {game['win_condition']} نقاط"
        )
        game["game_messages"].append(game_msg)
    except Exception as e:
        print(f"خطأ في إرسال رسالة اللعبة: {e}")

@client.on(events.NewMessage(pattern=r'^ارمي$'))
async def play_turn(event):
    """معالجة محاولة اللاعب"""
    chat_id = event.chat_id
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    if game["status"] != "playing":
        return

    player_id = str(event.sender_id)
    players = list(game["players"].values())
    current_player_idx = game["current_player"]
    current_player_id = list(game["players"].keys())[current_player_idx]

    if player_id != current_player_id:
        await event.reply("**⏳ ليس دورك الآن!**")
        return

    try:
        result = await event.reply(file=InputMediaDice(emoticon=game["game_type"]))
        await asyncio.sleep(3)
        dice_value = result.media.value
        
        game["players"][player_id]["score"] = dice_value
        current_player = players[current_player_idx]
        
        await event.reply(
            f"{game['game_type']} **نتيجة {current_player['name'].first_name}:** {dice_value}"
        )
        
        if dice_value == game["win_condition"]:
            await end_game(chat_id, player_id)
        else:
            await next_player_turn(chat_id)
            
    except Exception as e:
        await event.reply(f"**⚠️ حدث خطأ:** {str(e)}")

async def next_player_turn(chat_id):
    """الانتقال للاعب التالي"""
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    players = list(game["players"].values())
    game["current_player"] = (game["current_player"] + 1) % len(players)
    
    current_player = players[game["current_player"]]
    
    try:
        game_msg = await client.send_message(
            chat_id,
            f"{game['game_type']} **دور اللاعب:** {current_player['name'].first_name}\n\n"
            "🎮 اكتب `ارمي` لرمي النرد!\n"
            f"🏆 **شرط الفوز:** الحصول على {game['win_condition']} نقاط"
        )
        game["game_messages"].append(game_msg)
    except Exception as e:
        print(f"خطأ في إرسال رسالة دور اللاعب: {e}")

async def end_game(chat_id, winner_id):
    """إنهاء اللعبة بإعلان الفائز"""
    if chat_id not in active_games:
        return

    game = active_games[chat_id]
    winner = game["players"][winner_id]["name"]
    
    try:
        await client.send_message(
            chat_id,
            f"🎉 **تهانينا! فاز {winner.first_name} باللعبة!**\n\n"
            f"🏆 **النتيجة النهائية:** {game['win_condition']} نقاط\n"
            f"🎮 **نوع اللعبة:** {game['game_type']}\n\n"
            "💫 للعب مجدداً، اكتب الأمر مرة أخرى"
        )
    except Exception as e:
        print(f"خطأ في إرسال رسالة النهاية: {e}")
    
    del active_games[chat_id]

@client.on(events.NewMessage(pattern=r'^\.ايقاف$'))
async def stop_game(event):
    """إيقاف اللعبة الحالية"""
    chat_id = event.chat_id
    if chat_id not in active_games:
        await event.reply("**⚠️ لا يوجد لعبة نشطة لإنهائها**")
        return

    game_type = active_games[chat_id]["game_type"]
    del active_games[chat_id]
    await event.reply(f"**🛑 تم إيقاف لعبة {game_type}**")



GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")     

# سيتم تعبئة هذه المتغيرات تلقائياً
KOYEB_APP_NAME = None
KOYEB_SERVICE_ID = None

# إعدادات ثابتة
REPO_REMOTE_NAME = "temponame"
NO_KOYEB_APP_CFGD = "no koyeb application found, but a key given? 😕 "
RESTARTING_APP = "re-starting koyeb application"
koyeb_api = "https://app.koyeb.com/v1"

# مسارات النظام
requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def get_koyeb_app_info():
    """جلب معلومات التطبيق والخدمة من Koyeb تلقائياً"""
    if not KOYEB_API_TOKEN:
        return None
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        # إضافة timeout للطلبات
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # الحصول على قائمة التطبيقات مع تضمين الخدمات
            async with session.get(
                f"{koyeb_api}/apps?include=services",
                headers=headers
            ) as response:
                
                if response.status == 401:
                    return None
                elif response.status == 403:
                    return None
                elif response.status != 200:
                    return None
                
                apps_data = await response.json()
                
                if apps_data.get('apps'):
                    # نأخذ أول تطبيق في القائمة
                    app = apps_data['apps'][0]
                    global KOYEB_APP_NAME, KOYEB_SERVICE_ID
                    KOYEB_APP_NAME = app.get('name')
                    app_id = app.get('id')
                    
                    # أولاً: محاولة الحصول على معرف الخدمة من بيانات التطبيق مباشرة
                    if 'services' in app and app['services']:
                        KOYEB_SERVICE_ID = app['services'][0].get('id')
                        if KOYEB_SERVICE_ID:
                            return True
                    
                    # ثانياً: استخدام الطريقة الجديدة للحصول على الخدمات
                    async with session.get(
                        f"{koyeb_api}/services?app_id={app_id}",
                        headers=headers
                    ) as svc_response:
                        
                        if svc_response.status == 200:
                            services_data = await svc_response.json()
                            
                            if services_data.get('services'):
                                KOYEB_SERVICE_ID = services_data['services'][0].get('id')
                                return True
                        else:
                            # محاولة بديلة: جلب جميع الخدمات ثم تصفيتها
                            async with session.get(
                                f"{koyeb_api}/services",
                                headers=headers
                            ) as all_svc_response:
                                if all_svc_response.status == 200:
                                    all_services = await all_svc_response.json()
                                    
                                    # البحث عن خدمة تخص تطبيقنا
                                    app_services = [
                                        svc for svc in all_services.get('services', [])
                                        if svc.get('app_id') == app_id
                                    ]
                                    
                                    if app_services:
                                        KOYEB_SERVICE_ID = app_services[0].get('id')
                                        return True
                                    else:
                                        # محاولة أخيرة: استخدام app_id كـ service_id
                                        KOYEB_SERVICE_ID = app_id
                                        return True
                                else:
                                    return None
                
                    return None
                else:
                    return None
                    
    except aiohttp.ClientError:
        return None
    except asyncio.TimeoutError:
        return None
    except Exception:
        return None

async def get_koyeb_service_info():
    """جلب معلومات الخدمة من Koyeb"""
    if not KOYEB_API_TOKEN or not KOYEB_SERVICE_ID:
        return None
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                f"{koyeb_api}/services/{KOYEB_SERVICE_ID}",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except Exception:
        return None

async def redeploy_koyeb_service():
    """إعادة نشر الخدمة على Koyeb"""
    if not KOYEB_API_TOKEN or not KOYEB_SERVICE_ID:
        return False
    
    headers = {
        "Authorization": f"Bearer {KOYEB_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                f"{koyeb_api}/services/{KOYEB_SERVICE_ID}/redeploy",
                headers=headers
            ) as response:
                success = response.status in [200, 201, 202]
                return success
    except Exception:
        return False

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
#                                              🛠️ دوال مساعدة للنظام
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

async def gen_chlog(repo, diff):
    """إنشاء سجل التغييرات"""
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )

async def update_requirements():
    """تحديث المتطلبات من requirements.txt"""
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
#                                            🚀 دوال التحديث الرئيسية
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

async def update_bot(event, repo, ups_rem, ac_br):
    """تحديث البوت محلياً فقط"""
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    
    await update_requirements()
    
    await event.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
        "**•─────────────────•**\n\n"
        "**•⎆┊تم التحـديث ⎌ بنجـاح**\n"
        "**•⎆┊جـارِ إعـادة تشغيـل البـوت ⎋ **\n"
        "**•⎆┊انتظـࢪ مـن 2 - 1 دقيقـه . . .📟**"
    )
    
    # إضافة تأخير قبل قطع الاتصال
    await asyncio.sleep(3)
    try:
        await event.client.disconnect()
    except:
        pass

async def deploy(event, repo, ups_rem, ac_br, txt):
    """تنفيذ التحديث الكامل مع Koyeb"""
    if not KOYEB_API_TOKEN:
        return await event.edit(
            "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
            "**•─────────────────•**\n"
            "** ⪼ لم تقـم بوضـع متغيـر KOYEB_API_TOKEN\n"
            "قم بضبـط المتغيـر أولاً لتحديث البوت ..؟!**"
        )
    
    # التحقق من وجود معلومات التطبيق والخدمة
    if not KOYEB_APP_NAME or not KOYEB_SERVICE_ID:
        return await event.edit(
            f"{txt}\n**❌ معلومات التطبيق أو الخدمة غير متوفرة**"
        )
    
    service_info = await get_koyeb_service_info()
    if not service_info:
        await event.edit(f"{txt}\n**❌ بيانات اعتماد كويب غير صالحة لتنصيب التحديث**")
        return repo.__del__()
    
    await event.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
        "**•─────────────────•**\n"
        "**✾╎جـارِ تنصـيب التحـديث الجـذري ⎌**\n"
        "**✾╎يُرجـى الانتظـار حتى تنتهـي العمليـة ⎋**\n"
        "**✾╎عـادة ما يستغـرق هـذا التحـديث مـن 5 - 4 دقائـق 📟**"
    )
    
    try:
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        
        # إعداد URL مع GitHub token إذا كان متوفراً
        if GITHUB_TOKEN and UPSTREAM_REPO_URL:
            # تحويل HTTPS URL لتشمل التوكن
            if UPSTREAM_REPO_URL.startswith("https://github.com/"):
                auth_url = UPSTREAM_REPO_URL.replace("https://github.com/", f"https://{GITHUB_TOKEN}@github.com/")
            else:
                auth_url = UPSTREAM_REPO_URL
        else:
            auth_url = UPSTREAM_REPO_URL
        
        # التحقق من وجود remote origin وإعداده
        if "origin" in [remote.name for remote in repo.remotes]:
            origin = repo.remote("origin")
            # تحديث URL للـ remote
            origin.set_url(auth_url)
        else:
            # إنشاء origin جديد
            origin = repo.create_remote("origin", auth_url)
        
        # محاولة Push مع التعامل مع الأخطاء
        try:
            origin.push(f"HEAD:{UPSTREAM_REPO_BRANCH}", force=True)
        except Exception as push_error:
            # في حالة فشل Push، نكمل مع Koyeb فقط
            await event.edit(
                "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
                "**•─────────────────•**\n"
                "**⚠️ تحذير: فشل في رفع التحديثات للـ repository**\n"
                "**لكن سيتم المتابعة مع إعادة نشر Koyeb...**"
            )
            
            await asyncio.sleep(3)
        
    except Exception as error:
        await event.edit(
            f"{txt}\n**❌ خطأ في العملية:**\n`{str(error)[:300]}...`\n\n"
            "**تحقق من:**\n"
            "• صحة UPSTREAM_REPO_URL\n"
            "• وجود GITHUB_TOKEN (إذا كان repository خاص)\n"
            "• صلاحيات الوصول للـ repository"
        )
        return repo.__del__()
    
    redeploy_success = await redeploy_koyeb_service()
    if not redeploy_success:
        return await event.edit(
            "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
            "**•─────────────────•**\n"
            "**❌ فشل إعادة النشر على Koyeb!**\n"
            "**حدثت بعض الأخطاء في Koyeb...**"
        )
    
    await event.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
        "**•─────────────────•**\n\n"
        "**•⎆┊تم تحـديث البـوت بنجـاح ✅**\n"
        "**•⎆┊جـارِ إعـادة تشغيـل الخدمـة على كويـب 🌐**\n"
        "**•⎆┊قد يستغـرق الأمـر حتى 5 دقائـق ⏰**\n"
        "**•⎆┊انتظـر حتى يعـود البـوت للعمـل . . .📟**"
    )
    
    await asyncio.sleep(10)
    try:
        await event.client.disconnect()
    except:
        pass



async def progress_bar(event, steps=10):
    """عرض شريط تقدم مرئي للتحديث"""
    messages = [
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟷𝟶 ▬▭▭▭▭▭▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟸𝟶 ▬▬▭▭▭▭▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟹𝟶 ▬▬▬▭▭▭▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟺𝟶 ▬▬▬▬▭▭▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟻𝟶 ▬▬▬▬▬▭▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟼𝟶 ▬▬▬▬▬▬▭▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟽𝟶 ▬▬▬▬▬▬▬▭▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟾𝟶 ▬▬▬▬▬▬▬▬▭▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟿𝟶 ▬▬▬▬▬▬▬▬▬▭",
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n**•─────────────────•**\n\n**⇜ يتـم تحـديث البـوت .. انتظـر . . .🌐**\n\n%𝟷𝟶𝟶 ▬▬▬▬▬▬▬▬▬▬💯"
    ]
    
    for i in range(min(steps + 1, len(messages))):
        await event.edit(messages[i])
        await asyncio.sleep(1)


@client.on(events.NewMessage(pattern=r'^\.تحديث البوت$'))
async def update_command(event):
    """
    🚀 المعالج الرئيسي لأمر تحديث البوت
    
    الاستخدام: .تحديث البوت
    يتطلب وضع المتغيرات في Koyeb Environment Variables
    """
    
    # فحص أولي للمتغيرات المطلوبة
    if not KOYEB_API_TOKEN:
        return await event.edit(
            "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
            "**•─────────────────•**\n\n"
            "**❌ يجب تعيين متغير KOYEB_API_TOKEN أولاً**\n\n"
            "**📋 خطوات الإعداد:**\n"
            "• اذهب لـ Koyeb Dashboard\n"
            "• Settings → Environment Variables\n"
            "• أضف KOYEB_API_TOKEN\n"
            "• 🔒 فعل Secret option"
        )
    
    if not UPSTREAM_REPO_URL or "github.com" not in UPSTREAM_REPO_URL:
        return await event.edit(
            "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
            "**•─────────────────•**\n\n"
            "**❌ يجب تعيين متغير UPSTREAM_REPO_URL**\n\n"
            "**📋 مثال:**\n"
            "`https://github.com/username/repository.git`\n\n"
            "**ضعه في Koyeb Environment Variables**"
        )
    
    # إظهار رسالة التحميل
    loading_msg = await event.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
        "**•─────────────────•**\n\n"
        "**🔍 جاري فحص التطبيقات على Koyeb...**\n"
        "**⏳ قد يستغرق هذا بضع ثوانٍ...**"
    )
    
    # جلب معلومات التطبيق والخدمة تلقائياً
    app_info = await get_koyeb_app_info()
    if not app_info:
        return await loading_msg.edit(
            "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
            "**•─────────────────•**\n\n"
            "**❌ فشل في جلب معلومات التطبيق والخدمة**\n\n"
            "**🔍 الأسباب المحتملة:**\n"
            "• الـ API Token غير صحيح\n"
            "• لا يوجد تطبيقات في حسابك على Koyeb\n"
            "• مشكلة في الاتصال بالإنترنت\n"
            "• الحساب لا يملك صلاحيات كافية"
        )
    
    await loading_msg.edit(
        "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗘𝗥𝗘𝗡 - تحـديث إيرين\n"
        "**•─────────────────•**\n\n"
        f"**✅ تم العثور على التطبيق بنجاح**\n"
        f"**✅ تم العثور على الخدمة بنجاح**\n"
        f"**✅ تم ربط المستودع بنجاح**\n\n"
        "**🔧 جاري تحضير التحديث...**"
    )
    
    # تحديد المجلد الحالي
    current_dir = os.getcwd()
    
    # محاولة الانتقال للمجلد المناسب
    if "/app" in current_dir or "koyeb" in current_dir.lower():
        os.chdir(current_dir)
    else:
        if os.path.exists("/app"):
            os.chdir("/app")
        elif os.path.exists("./"):
            os.chdir("./")
    
    # إعداد repository
    try:
        txt = (
            "`❌ لا يمكن المتابعة بسبب حدوث بعض المشاكل`\n\n"
            "**سجل الأخطاء:**\n"
        )
        repo = Repo()
        
    except NoSuchPathError as error:
        await loading_msg.edit(f"{txt}\n\n**❌ المسـار** {error} **غيـر مـوجـود**")
        return
    except GitCommandError as error:
        await loading_msg.edit(f"{txt}\n**❌ خطـأ في Git:**\n`{str(error)[:500]}...`")
        return
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO_URL)
        origin.fetch()
        try:
            repo.create_head(UPSTREAM_REPO_BRANCH, origin.refs[UPSTREAM_REPO_BRANCH])
            repo.heads[UPSTREAM_REPO_BRANCH].set_tracking_branch(origin.refs[UPSTREAM_REPO_BRANCH])
            repo.heads[UPSTREAM_REPO_BRANCH].checkout(True)
        except:
            repo.create_head("main", origin.refs.main)
            repo.heads.main.set_tracking_branch(origin.refs.main)
            repo.heads.main.checkout(True)
    
    # تشغيل شريط التقدم
    await progress_bar(loading_msg)
    
    # بدء عملية النشر
    ac_br = repo.active_branch.name
    
    # التحقق من وجود upstream remote
    if "upstream" in [remote.name for remote in repo.remotes]:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO_URL)
    
    try:
        ups_rem.fetch(ac_br)
    except Exception:
        # المتابعة رغم الخطأ
        pass
    
    # تنفيذ التحديث
    await deploy(loading_msg, repo, ups_rem, ac_br, txt)

@client.on(events.NewMessage(pattern=r'\.بحث (.+)'))
async def download_and_send_audio(event):
    query = event.pattern_match.group(1)
    await event.edit("**╮ جـارِ البحث ؏ـن المقطـٓع الصٓوتـي... 🎧♥️╰**")

    try:
        # إعدادات yt-dlp محسنة للسرعة
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best[height<=480]',  # أولوية للصوت المضغوط
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'writeinfojson': False,  # عدم كتابة ملفات JSON
            'writethumbnail': False,  # عدم تحميل الصورة بشكل منفصل
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # جودة أقل للسرعة
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            },
            # تحسينات الشبكة
            'socket_timeout': 30,
            'retries': 2,
            'fragment_retries': 2,
            'concurrent_fragment_downloads': 4,  # تحميل متوازي
        }

        # التحقق من وجود ملف الكوكيز
        if os.path.exists('cookies.txt'):
            ydl_opts['cookiefile'] = 'cookies.txt'

        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs('downloads', exist_ok=True)

        with YoutubeDL(ydl_opts) as ydl:
            try:
                # البحث عن الفيديو
                info = await asyncio.to_thread(ydl.extract_info, f"ytsearch1:{query}", download=False)
                
                if not info or not info.get('entries'):
                    await event.edit("**⚠️ لم يتم العثور على نتائج**")
                    return

                video = info['entries'][0]
                video_id = video.get('id')
                video_url = video.get('webpage_url')
                title = video.get('title', 'Unknown Title')
                artist = video.get('uploader', 'Unknown Artist')
                duration = video.get('duration', 0)
                thumbnail = video.get('thumbnail')

                if not video_url:
                    await event.edit("**⚠️ لا يوجد رابط للفيديو**")
                    return

                await event.edit("**╮ جـارِ التحميل... 🎧♥️╰**")

                # تحميل الصورة المصغرة
                thumb_path = None
                if thumbnail:
                    try:
                        thumb_path = f'downloads/{video_id}_thumb.jpg'
                        async with httpx.AsyncClient(timeout=10.0) as client:
                            response = await client.get(thumbnail)
                            if response.status_code == 200:
                                with open(thumb_path, 'wb') as f:
                                    f.write(response.content)
                    except Exception:
                        pass

                # تحميل الملف الصوتي
                audio_path = f'downloads/{video_id}.mp3'
                await asyncio.to_thread(ydl.download, [video_url])

                # التحقق من وجود الملف
                if not os.path.exists(audio_path):
                    # البحث عن الملف بأي امتداد
                    existing_files = glob.glob(f'downloads/{video_id}.*')
                    if existing_files:
                        audio_path = existing_files[0]

                if not os.path.exists(audio_path):
                    raise Exception("فشل في إنشاء ملف الصوت")

                # إضافة البيانات الوصفية
                try:
                    audio = EasyID3(audio_path)
                except ID3NoHeaderError:
                    audio = EasyID3()
                
                audio['title'] = title
                audio['artist'] = artist
                audio.save()

                # إضافة صورة الغلاف إذا كانت موجودة
                if thumb_path and os.path.exists(thumb_path):
                    try:
                        audio = ID3(audio_path)
                        with open(thumb_path, 'rb') as f:
                            audio.add(APIC(
                                encoding=3,
                                mime='image/jpeg',
                                type=3,
                                desc='Cover',
                                data=f.read()
                            ))
                        audio.save()
                    except Exception:
                        pass

                # إرسال الملف
                await event.edit("**╮ ❐ جـارِ الرفع...𓅫╰**")
                
                await event.client.send_file(
                    event.chat_id,
                    audio_path,
                    caption=f"**⌔╎البحث:** `{artist} - {title}`",
                    thumb=thumb_path if thumb_path and os.path.exists(thumb_path) else None,
                    attributes=[
                        DocumentAttributeAudio(
                            duration=duration,
                            voice=False,
                            title=title,
                            performer=artist
                        )
                    ],
                    supports_streaming=True,
                    part_size_kb=512,  # حجم أجزاء الرفع (محسن للسرعة)
                )
                
                await event.delete()

            except Exception as e:
                await event.edit(f"**⚠️ خطأ:** {str(e)[:500]}")
                return

    except Exception as e:
        await event.edit(f"**⚠️ خطأ عام:** {str(e)[:500]}")
    
    finally:
        # تنظيف الملفات المؤقتة بشكل أسرع
        if 'video_id' in locals():
            cleanup_tasks = []
            for pattern in [f'downloads/{video_id}*', 'downloads/*.part']:
                for file_path in glob.glob(pattern):
                    cleanup_tasks.append(asyncio.create_task(
                        asyncio.to_thread(os.remove, file_path)
                    ))
            
            if cleanup_tasks:
                await asyncio.gather(*cleanup_tasks, return_exceptions=True)

@client.on(events.NewMessage(pattern=r'\.يوت(?: |$)(.*)'))
async def download_and_send_video(event):
    # التحقق مما إذا كان هناك رابط في الرسالة أو الرد على رسالة تحتوي على رابط
    reply = await event.get_reply_message()
    input_url = event.pattern_match.group(1).strip()

    if reply and not input_url:  # إذا كان الرد على رسالة تحتوي على رابط
        input_url = reply.message.strip()

    if not input_url:  # إذا لم يكن هناك رابط في الرسالة أو الرد
        await event.edit("**╮ ❐ يـرجى إرسـال الامـر مـع رابـط الفيـديـو .يوت + رابط او بالـرد ع رابـط 📹╰**")
        return

    await event.edit("**╮ جـارِ تحميـل الفيـديـو مـن يـوتيـوب... 📹♥️╰**")

    try:
        # التحقق من وجود ملف الكوكيز
        cookie_file = 'cookies.txt'
        if not os.path.exists(cookie_file):
            await event.edit("**⚠️ خطـأ**: ملف الكـوكيـز غيـر موجـود!")
            return

        # إعدادات yt-dlp محسنة مع الكوكيز
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_file,
            'extract_flat': False,
            'ignoreerrors': False,
            
            # إعدادات محسنة لتجاوز اكتشاف البوت
            'extractor_args': {
                'youtube': {
                    'skip': ['translated_subs', 'automatic_captions'],
                    'player_client': ['android', 'web'],
                }
            },
            
            # تحديد User-Agent محدث
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            
            # إضافة تأخير لتجنب اكتشاف البوت
            'sleep_interval': 1,
            'max_sleep_interval': 3,
        }

        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs('downloads', exist_ok=True)

        # تأخير عشوائي قبل البدء
        await asyncio.sleep(random.uniform(2, 4))

        # تنزيل الفيديو
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(input_url, download=True)
                video_title = info.get('title', 'فيـديـو بـدون عـنوان')
                video_file = ydl.prepare_filename(info)
                
                # التحقق من أن الملف تم تنزيله
                if not os.path.exists(video_file):
                    await event.edit("**⚠️ فشـل في تحميـل الفيـديـو**")
                    return

                await event.edit("**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")

                # التحقق من حجم الملف
                file_size = os.path.getsize(video_file)
                if file_size > 2000 * 1024 * 1024:  # 2GB
                    await event.edit("**⚠️ الملف كبير جداً للإرسال (أكثر من 2GB)**")
                    os.remove(video_file)
                    return

                # إرسال الفيديو
                await client.send_file(
                    event.chat_id,
                    video_file,
                    caption=f"**📹╎عـنوان الفيـديـو:** `{video_title}`",
                    supports_streaming=True,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")
                    )
                )

                await event.edit(f"**╮ ❐ تم إرسـال الفيـديـو بنجـاح ✅**\n**╰ ❐ العـنوان:** `{video_title}`")

            except Exception as download_error:
                error_msg = str(download_error)
                
                # رسائل خطأ محددة لمساعدة المستخدم
                if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
                    await event.edit("**⚠️ YouTube يطلب التحقق. حدث الكوكيز أو جرب لاحقاً**")
                elif "Video unavailable" in error_msg:
                    await event.edit("**⚠️ الفيـديـو غيـر متـوفر أو محـذوف**")
                elif "Private video" in error_msg:
                    await event.edit("**⚠️ الفيـديـو خـاص ولا يمكـن تحميـله**")
                elif "too large" in error_msg.lower():
                    await event.edit("**⚠️ الفيـديـو كبيـر جـداً للإرسـال**")
                else:
                    await event.edit(f"**⚠️ خطـأ في التحـميل**: {str(download_error)}")
                return

    except Exception as e:
        await event.edit(f"**⚠️ حـدث خـطأ عـام**: {str(e)}")
    
    finally:
        # تنظيف الملفات المؤقتة
        try:
            if 'video_file' in locals() and os.path.exists(video_file):
                os.remove(video_file)
        except Exception as cleanup_error:
            print(f"تحذير: فشل في تنظيف الملفات: {cleanup_error}")

async def progress(current, total, event, text):
    """دالة لعرض شريط التقدم"""
    progress = f"{current * 100 / total:.1f}%"
    await event.edit(f"{text}\n\n**╮ ❐ جـارِ الـرفع:** `{progress}`\n**╰ ❐ الحجـم:** `{humanbytes(current)} / {humanbytes(total)}`")

def humanbytes(size):
    """تحويل الحجم إلى صيغة مقروءة"""
    if not size:
        return "0B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"      

@client.on(events.NewMessage(pattern=r'\.انستا(?: |$)(.*)'))
async def download_and_send_instagram(event):
    # التحقق مما إذا كان هناك رابط في الرسالة أو الرد على رسالة تحتوي على رابط
    reply = await event.get_reply_message()
    input_url = event.pattern_match.group(1).strip()

    if reply and not input_url:  # إذا كان الرد على رسالة تحتوي على رابط
        input_url = reply.message.strip()

    if not input_url:  # إذا لم يكن هناك رابط في الرسالة أو الرد
        await event.edit("**╮ ❐ يـرجى إرسـال الامـر مـع رابـط إنستـجرام .انستا + رابط او بالـرد ع رابـط 📹╰**")
        return

    await event.edit("**╮ جـارِ تحميـل الفيـديـو مـن إنستـجرام... 📹♥️╰**")

    try:
        # التحقق من وجود ملف الكوكيز
        cookie_file = 'cks.txt'
        if not os.path.exists(cookie_file):
            await event.edit("**⚠️ خطـأ**: ملف الكـوكيـز غيـر موجـود!")
            return

        # إعدادات yt-dlp محسنة مع الكوكيز
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_file,
            'extract_flat': False,
            'ignoreerrors': False,
            
            # إعدادات محسنة لتجاوز اكتشاف البوت
            'extractor_args': {
                'instagram': {
                    'skip': ['translated_subs', 'automatic_captions'],
                }
            },
            
            # تحديد User-Agent محدث
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            
            # إضافة تأخير لتجنب اكتشاف البوت
            'sleep_interval': 1,
            'max_sleep_interval': 3,
        }

        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs('downloads', exist_ok=True)

        # تأخير عشوائي قبل البدء
        await asyncio.sleep(random.uniform(2, 4))

        # تنزيل الفيديو
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(input_url, download=True)
                video_title = info.get('title', 'فيـديـو إنستـجرام بـدون عـنوان')
                video_file = ydl.prepare_filename(info)
                
                # التحقق من أن الملف تم تنزيله
                if not os.path.exists(video_file):
                    await event.edit("**⚠️ فشـل في تحميـل الفيـديـو**")
                    return

                await event.edit("**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")

                # التحقق من حجم الملف
                file_size = os.path.getsize(video_file)
                if file_size > 2000 * 1024 * 1024:  # 2GB
                    await event.edit("**⚠️ الملف كبير جداً للإرسال (أكثر من 2GB)**")
                    os.remove(video_file)
                    return

                # إرسال الفيديو
                await client.send_file(
                    event.chat_id,
                    video_file,
                    caption=f"**📹╎عـنوان الفيـديـو:** `{video_title}`",
                    supports_streaming=True,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")
                    )
                )

                await event.edit(f"**╮ ❐ تم إرسـال الفيـديـو بنجـاح ✅**\n**╰ ❐ العـنوان:** `{video_title}`")

            except Exception as download_error:
                error_msg = str(download_error)
                
                # رسائل خطأ محددة لمساعدة المستخدم
                if "Login Required" in error_msg or "private" in error_msg.lower():
                    await event.edit("**⚠️ المنشور خاص أو يتطلب تسجيل الدخول**")
                elif "Video unavailable" in error_msg:
                    await event.edit("**⚠️ الفيـديـو غيـر متـوفر أو محـذوف**")
                elif "too large" in error_msg.lower():
                    await event.edit("**⚠️ الفيـديـو كبيـر جـداً للإرسـال**")
                elif "rate limit" in error_msg.lower():
                    await event.edit("**⚠️ تم تجاوز حد الطلبات، حاول لاحقاً**")
                else:
                    await event.edit(f"**⚠️ خطـأ في التحـميل**: {str(download_error)}")
                return

    except Exception as e:
        await event.edit(f"**⚠️ حـدث خـطأ عـام**: {str(e)}")
    
    finally:
        # تنظيف الملفات المؤقتة
        try:
            if 'video_file' in locals() and os.path.exists(video_file):
                os.remove(video_file)
        except Exception as cleanup_error:
            print(f"تحذير: فشل في تنظيف الملفات: {cleanup_error}")

async def progress(current, total, event, text):
    """دالة لعرض شريط التقدم"""
    progress = f"{current * 100 / total:.1f}%"
    await event.edit(f"{text}\n\n**╮ ❐ جـارِ الـرفع:** `{progress}`\n**╰ ❐ الحجـم:** `{humanbytes(current)} / {humanbytes(total)}`")

def humanbytes(size):
    """تحويل الحجم إلى صيغة مقروءة"""
    if not size:
        return "0B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"

@client.on(events.NewMessage(pattern=r'\.تيك(?: |$)(.*)'))
async def download_and_send_tiktok(event):
    # التحقق مما إذا كان هناك رابط في الرسالة أو الرد على رسالة تحتوي على رابط
    reply = await event.get_reply_message()
    input_url = event.pattern_match.group(1).strip()

    if reply and not input_url:  # إذا كان الرد على رسالة تحتوي على رابط
        input_url = reply.message.strip()

    if not input_url:  # إذا لم يكن هناك رابط في الرسالة أو الرد
        await event.edit("**╮ ❐ يـرجى إرسـال الامـر مـع رابـط تيـك تـوك .تيك + رابط او بالـرد ع رابـط 📹╰**")
        return

    await event.edit("**╮ جـارِ تحميـل الفيـديـو مـن تيـك تـوك... 📹♥️╰**")

    try:
        # التحقق من وجود ملف الكوكيز
        cookie_file = 'tekcook.txt'
        if not os.path.exists(cookie_file):
            await event.edit("**⚠️ خطـأ**: ملف الكـوكيـز غيـر موجـود!")
            return

        # إعدادات yt-dlp محسنة مع الكوكيز
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': cookie_file,
            'extract_flat': False,
            'ignoreerrors': False,
            'socket_timeout': 60,
            
            # إعدادات خاصة بتيك توك
            'extractor_args': {
                'tiktok': {
                    'skip': ['watermark'],  # تخطي علامة الماء إن أمكن
                }
            },
            
            # تحديد User-Agent محدث
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Referer': 'https://www.tiktok.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
            },
            
            # معالج ما بعد التحميل لضمان التوافق
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            
            # إضافة تأخير لتجنب اكتشاف البوت
            'sleep_interval': 2,
            'max_sleep_interval': 5,
        }

        # إنشاء مجلد التحميل إذا لم يكن موجوداً
        os.makedirs('downloads', exist_ok=True)

        # تأخير عشوائي قبل البدء
        await asyncio.sleep(random.uniform(1, 3))

        # تنزيل الفيديو
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(input_url, download=True)
                video_title = info.get('title', 'فيـديـو تيـك تـوك بـدون عـنوان')
                video_file = ydl.prepare_filename(info)
                
                # تأكيد تحويل الصيغة إلى mp4 إن لزم
                if not video_file.endswith('.mp4'):
                    new_path = os.path.splitext(video_file)[0] + '.mp4'
                    os.rename(video_file, new_path)
                    video_file = new_path
                
                # التحقق من أن الملف تم تنزيله
                if not os.path.exists(video_file):
                    await event.edit("**⚠️ فشـل في تحميـل الفيـديـو**")
                    return

                await event.edit("**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")

                # التحقق من حجم الملف
                file_size = os.path.getsize(video_file)
                if file_size > 2000 * 1024 * 1024:  # 2GB
                    await event.edit("**⚠️ الملف كبير جداً للإرسال (أكثر من 2GB)**")
                    os.remove(video_file)
                    return

                # إرسال الفيديو
                await client.send_file(
                    event.chat_id,
                    video_file,
                    caption=f"**📹╎عـنوان الفيـديـو:** `{video_title}`",
                    supports_streaming=True,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")
                    )
                )

                await event.edit(f"**╮ ❐ تم إرسـال الفيـديـو بنجـاح ✅**\n**╰ ❐ العـنوان:** `{video_title}`")

            except Exception as download_error:
                error_msg = str(download_error)
                
                # رسائل خطأ محددة لمساعدة المستخدم
                if "Private video" in error_msg or "private" in error_msg.lower():
                    await event.edit("**⚠️ الفيـديـو خـاص ولا يمكـن تحميـله**")
                elif "Video unavailable" in error_msg:
                    await event.edit("**⚠️ الفيـديـو غيـر متـوفر أو محـذوف**")
                elif "too large" in error_msg.lower():
                    await event.edit("**⚠️ الفيـديـو كبيـر جـداً للإرسـال**")
                elif "rate limit" in error_msg.lower() or "Too many" in error_msg:
                    await event.edit("**⚠️ تم تجاوز حد الطلبات، حاول لاحقاً**")
                elif "copyright" in error_msg.lower():
                    await event.edit("**⚠️ الفيـديـو محمـي بحقـوق النشـر**")
                else:
                    await event.edit(f"**⚠️ خطـأ في التحـميل**: {str(download_error)}")
                return

    except Exception as e:
        await event.edit(f"**⚠️ حـدث خـطأ عـام**: {str(e)}")
    
    finally:
        # تنظيف الملفات المؤقتة
        try:
            if 'video_file' in locals() and os.path.exists(video_file):
                os.remove(video_file)
        except Exception as cleanup_error:
            print(f"تحذير: فشل في تنظيف الملفات: {cleanup_error}")

async def progress(current, total, event, text):
    """دالة لعرض شريط التقدم"""
    progress = f"{current * 100 / total:.1f}%"
    await event.edit(f"{text}\n\n**╮ ❐ جـارِ الـرفع:** `{progress}`\n**╰ ❐ الحجـم:** `{humanbytes(current)} / {humanbytes(total)}`")

def humanbytes(size):
    """تحويل الحجم إلى صيغة مقروءة"""
    if not size:
        return "0B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}PB"                        


##########################

# تجاهل تحذيرات SSL
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# الدوال المساعدة
def humanbytes(size):
    """تحويل الحجم إلى صيغة مقروءة"""
    if not size:
        return "0B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TB"

async def progress(current, total, event, text):
    """دالة لعرض شريط التقدم"""
    if not current or not total:
        return
    try:
        progress_percent = (current * 100) / total
        if progress_percent % 10 < 1:
            await event.edit(f"{text}\n\n**╮ ❐ التقـدم:** `{progress_percent:.1f}%`\n**╰ ❐ الحجـم:** `{humanbytes(current)} / {humanbytes(total)}`")
    except Exception as e:
        print(f"Error in progress: {e}")

def expand_pinterest_url(short_url):
    """توسيع الروابط المختصرة من pin.it إلى pinterest.com"""
    try:
        if 'pin.it' in short_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.head(short_url, headers=headers, allow_redirects=True, timeout=10, verify=False)
            expanded_url = response.url
            print(f"Expanded URL: {short_url} -> {expanded_url}")
            return expanded_url
        return short_url
    except Exception as e:
        print(f"Error expanding URL: {e}")
        return short_url

def convert_cookies_to_netscape(cookies):
    """تحويل الكوكيز من JSON إلى تنسيق Netscape"""
    netscape_cookies = "# Netscape HTTP Cookie File\n"
    for cookie in cookies:
        netscape_cookies += (
            f"{cookie.get('domain', '.pinterest.com')}\t"
            f"{'TRUE' if cookie.get('secure') else 'FALSE'}\t"
            f"{cookie.get('path', '/')}\t"
            f"{'TRUE' if cookie.get('secure') else 'FALSE'}\t"
            f"{cookie.get('expiry', '0')}\t"
            f"{cookie['name']}\t"
            f"{cookie['value']}\n"
        )
    return netscape_cookies

def load_pinterest_cookies():
    """تحميل كوكيز Pinterest من ملف pincook.txt"""
    cookie_files = ['pincook.txt', 'cookies.txt']
    
    for cookie_file in cookie_files:
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content.startswith('# Netscape HTTP Cookie File'):
                    return content
                elif content.startswith('[') or content.startswith('{'):
                    cookies = json.loads(content)
                    return convert_cookies_to_netscape(cookies)
                
            except Exception as e:
                print(f"Error loading cookies from {cookie_file}: {e}")
    
    return None

async def download_with_gallerydl(url, temp_dir, cookies=None):
    """استخدام gallery-dl لتحميل المحتوى مع الكوكيز"""
    try:
        # إنشاء ملف الكوكيز المؤقت إذا كانت متوفرة
        cookies_file = None
        if cookies:
            cookies_file = os.path.join(temp_dir, "cookies.txt")
            with open(cookies_file, 'w', encoding='utf-8') as f:
                f.write(cookies)
        
        # بناء أمر gallery-dl
        cmd = [
            'gallery-dl',
            '--no-check-certificate',
            '--write-metadata',
            '--write-info-json',
            '--directory', temp_dir,
            '--no-part',
            '--no-mtime',
            url
        ]
        
        if cookies_file:
            cmd.extend(['--cookies', cookies_file])
        
        # تنفيذ الأمر
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        print(f"gallery-dl stdout: {stdout.decode()}")
        print(f"gallery-dl stderr: {stderr.decode()}")
        
        if process.returncode != 0:
            raise Exception(f"gallery-dl failed with code {process.returncode}: {stderr.decode()}")
        
        # البحث عن الملف الذي تم تنزيله
        downloaded_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mkv')):
                    downloaded_files.append(os.path.join(root, file))
        
        if not downloaded_files:
            raise Exception("No media files found after download")
        
        # نرجع أول ملف (الأكبر حجماً عادةً)
        downloaded_files.sort(key=lambda x: os.path.getsize(x), reverse=True)
        return downloaded_files[0]
        
    except Exception as e:
        print(f"Error in download_with_gallerydl: {e}")
        raise

@client.on(events.NewMessage(pattern=r'\.بنترست(?: |$)(.*)'))
async def download_pinterest(event):
    # التحقق من وجود رابط
    reply = await event.get_reply_message()
    input_url = event.pattern_match.group(1).strip()
    
    if reply and not input_url:
        input_url = reply.message.strip()
    
    if not input_url:
        await event.edit("**╮ ❐ يـرجى إرسـال الامـر مـع رابـط بنترست .بنترست + رابط او بالـرد ع رابـط 📌╰**")
        return

    if not any(domain in input_url for domain in ['pinterest.com', 'pin.it']):
        await event.edit("**⚠️ يـجب إدخـال رابـط بنترست صـحيح**")
        return

    # توسيع الرابط المختصر إذا كان من pin.it
    if 'pin.it' in input_url:
        input_url = expand_pinterest_url(input_url)
        if not input_url or 'pinterest.com' not in input_url:
            await event.edit("**⚠️ فشل في توسيع الرابط المختصر**")
            return

    await event.edit("**╮ جـارِ تحميـل المحتـوى مـن بنترسـت... 📌♥️╰**")

    try:
        # إنشاء مجلد التحميل المؤقت
        temp_dir = tempfile.mkdtemp()
        
        # تحميل الكوكيز من ملف pincook.txt
        cookies = load_pinterest_cookies()
        
        if not cookies:
            await event.edit("**⚠️ لم يتم العثور على ملف الكوكيز**\n\n**ضع ملف الكوكيز باسم:** `pincook.txt`\n\n**طريقة الحصول على الكوكيز:**\n1. افتح Pinterest في متصفحك\n2. استخدم إضافة مثل Cookie-Editor\n3. احفظ الكوكيز بصيغة Netscape (pincook.txt)")
            return
        
        print(f"Loaded cookies for Pinterest")
        
        # تحميل المحتوى باستخدام gallery-dl
        downloaded_file = await download_with_gallerydl(input_url, temp_dir, cookies)
        
        # التحقق من حجم الملف
        file_size = os.path.getsize(downloaded_file)
        if file_size == 0:
            await event.edit("**⚠️ الملف فارغ أو تالف**")
            os.remove(downloaded_file)
            return
            
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            await event.edit(f"**⚠️ الملف كبير جداً للإرسال ({humanbytes(file_size)})**\n**الحد الأقصى: {humanbytes(max_size)}**")
            os.remove(downloaded_file)
            return

        # تحديد نوع المحتوى
        is_video = downloaded_file.lower().endswith(('.mp4', '.webm', '.mkv'))
        is_gif = downloaded_file.lower().endswith('.gif')
        
        await event.edit("**╮ ❐ جـارِ الـرفع انتظـر ...𓅫╰**")
        
        # إعداد التسمية التوضيحية
        caption = f"**📌╎تم تحميـل {'الفيديـو' if is_video else 'الصـورة'} مـن بنترست**\n"
        caption += f"**📊 الحجـم:** {humanbytes(file_size)}"
        
        # محاولة قراءة ملف المعلومات (إن وجد)
        info_file = os.path.splitext(downloaded_file)[0] + '.info.json'
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    if 'description' in info:
                        caption += f"\n**📝 الوصـف:** {info['description'][:100]}"
            except:
                pass
        
        try:
            # إرسال المحتوى
            if is_video:
                await event.client.send_file(
                    event.chat_id,
                    downloaded_file,
                    caption=caption,
                    supports_streaming=True,
                    progress_callback=lambda d, t: asyncio.create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ رفـع الفيـديـو ...🎬╰**")
                    ) if d and t else None
                )
            elif is_gif:
                await event.client.send_file(
                    event.chat_id,
                    downloaded_file,
                    caption=caption,
                    force_document=False,
                    progress_callback=lambda d, t: asyncio.create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ رفـع الصـورة المتحركة ...🖼️╰**")
                    ) if d and t else None
                )
            else:
                await event.client.send_file(
                    event.chat_id,
                    downloaded_file,
                    caption=caption,
                    progress_callback=lambda d, t: asyncio.create_task(
                        progress(d, t, event, "**╮ ❐ جـارِ رفـع الصـورة ...🖼️╰**")
                    ) if d and t else None
                )

            await event.edit(f"**╮ ❐ تم إرسـال المحتـوى بنجـاح ✅**\n**╰ ❐ النـوع:** {'فيديو' if is_video else ('صورة متحركة' if is_gif else 'صورة')}\n**📊 الحجـم:** {humanbytes(file_size)}")

        except Exception as upload_error:
            print(f"Upload error: {upload_error}")
            await event.edit("**⚠️ فشل في رفع الملف، يرجى المحاولة لاحقاً**")

        # تنظيف الملفات المؤقتة
        try:
            shutil.rmtree(temp_dir)
        except Exception as cleanup_error:
            print(f"Cleanup error: {cleanup_error}")

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Main error: {e}")
        
        if "403" in error_msg or "forbidden" in error_msg:
            await event.edit("**⚠️ تم حظر الوصول - جرب استخدام كوكيز صالح أو VPN**")
        elif "private" in error_msg or "login" in error_msg:
            await event.edit("**⚠️ المحتوى خاص ويتطلب تسجيل دخول - تأكد من صحة الكوكيز**")
        elif "not found" in error_msg or "unavailable" in error_msg or "404" in error_msg:
            await event.edit("**⚠️ المحتوى غير متوفر أو تم حذفه**")
        elif "timeout" in error_msg:
            await event.edit("**⚠️ انتهت مهلة الاتصال - حاول مرة أخرى**")
        elif "invalid" in error_msg and "url" in error_msg:
            await event.edit("**⚠️ الرابط غير صحيح أو غير مدعوم**")
        else:
            await event.edit(f"**⚠️ حـدث خـطأ**: {str(e)[:200]}...")

#######################

# تجاهل تحذيرات SSL
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# الدوال المساعدة
def humanbytes(size):
    """تحويل الحجم إلى صيغة مقروءة"""
    if not size:
        return "0B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f}{unit}"
        size /= 1024
    return f"{size:.2f}TB"

async def progress(current, total, event, text):
    """دالة لعرض شريط التقدم"""
    if not current or not total:
        return
    try:
        progress_percent = (current * 100) / total
        if progress_percent % 10 < 1:
            await event.edit(f"{text}\n\n**╮ ❐ التقـدم:** `{progress_percent:.1f}%`\n**╰ ❐ الحجـم:** `{humanbytes(current)} / {humanbytes(total)}`")
    except Exception as e:
        print(f"Error in progress: {e}")

def convert_cookies_to_netscape(cookies):
    """تحويل الكوكيز من JSON إلى تنسيق Netscape"""
    netscape_cookies = "# Netscape HTTP Cookie File\n"
    for cookie in cookies:
        netscape_cookies += (
            f"{cookie.get('domain', '.pinterest.com')}\t"
            f"{'TRUE' if cookie.get('secure') else 'FALSE'}\t"
            f"{cookie.get('path', '/')}\t"
            f"{'TRUE' if cookie.get('secure') else 'FALSE'}\t"
            f"{cookie.get('expiry', '0')}\t"
            f"{cookie['name']}\t"
            f"{cookie['value']}\n"
        )
    return netscape_cookies

def load_pinterest_cookies():
    """تحميل كوكيز Pinterest من ملف pincook.txt"""
    cookie_files = ['pincook.txt', 'cookies.txt']
    
    for cookie_file in cookie_files:
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content.startswith('# Netscape HTTP Cookie File'):
                    return content
                elif content.startswith('[') or content.startswith('{'):
                    cookies = json.loads(content)
                    return convert_cookies_to_netscape(cookies)
                
            except Exception as e:
                print(f"Error loading cookies from {cookie_file}: {e}")
    
    return None

# متغير لتتبع البحثات السابقة مع تحسينات لتجنب التكرار
search_cache = {}

async def download_pinterest_images(query, count, temp_dir, cookies, offset=None):
    """تحميل الصور من Pinterest بناءً على البحث مع دعم التصفح المتعدد"""
    try:
        # إنشاء ملف الكوكيز المؤقت
        cookies_file = None
        if cookies:
            cookies_file = os.path.join(temp_dir, "cookies.txt")
            with open(cookies_file, 'w', encoding='utf-8') as f:
                f.write(cookies)
        
        # إضافة تنويع في البحث لتجنب تكرار النتائج
        search_variations = [
            f"https://www.pinterest.com/search/pins/?q={quote(query)}",
            f"https://www.pinterest.com/search/pins/?q={quote(query)}&rs=typed",
            f"https://www.pinterest.com/search/pins/?q={quote(query)}&source_id=",
            f"https://www.pinterest.com/search/pins/?q={quote(query)}&sort=latest",
            f"https://www.pinterest.com/search/pins/?q={quote(query)}&sort=popular",
        ]
        
        # اختيار رابط البحث بشكل عشوائي مع إضافة معلمات مختلفة
        search_url = random.choice(search_variations)
        
        # إذا كان هناك offset، نضيفه إلى رابط البحث
        if offset is not None:
            search_url = f"{search_url}&page={offset + 1}"
        
        # بناء أمر gallery-dl مع تحسينات للذاكرة
        cmd = [
            'gallery-dl',
            '--no-check-certificate',
            '--write-metadata',
            '--write-info-json',
            '--directory', temp_dir,
            '--no-part',
            '--no-mtime',
            '--range', f'1-{count}',
            '--sleep', '0.5',
            '--retries', '3',
            search_url
        ]
        
        if cookies_file:
            cmd.extend(['--cookies', cookies_file])
        
        # تنفيذ الأمر مع تحسينات الذاكرة
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            limit=1024*1024  # تحديد حد الذاكرة للعملية
        )
        
        stdout, stderr = await process.communicate()
        
        print(f"gallery-dl stdout: {stdout.decode()}")
        print(f"gallery-dl stderr: {stderr.decode()}")
        
        if process.returncode != 0:
            raise Exception(f"gallery-dl failed with code {process.returncode}: {stderr.decode()}")
        
        # البحث عن الملفات التي تم تنزيلها
        downloaded_files = []
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                    file_path = os.path.join(root, file)
                    downloaded_files.append(file_path)
        
        # ترتيب الملفات حسب وقت التعديل لضمان الترتيب الصحيح
        downloaded_files.sort(key=lambda x: os.path.getmtime(x))
        
        if not downloaded_files:
            raise Exception("No images found after download")
        
        return downloaded_files
        
    except Exception as e:
        print(f"Error in download_pinterest_images: {e}")
        raise

@client.on(events.NewMessage(pattern=r'\.صور (.*?) (\d+)'))
async def pinterest_images_search(event):
    # استخراج البحث وعدد الصور من الأمر
    match = event.pattern_match
    query = match.group(1).strip()
    count = int(match.group(2))
    
    # تحديد الحد الأقصى للصور (50 صورة كحد أقصى)
    if count > 50:
        await event.edit("**⚠️ الحد الأقصى لعدد الصور هو 50**")
        return
    elif count < 1:
        await event.edit("**⚠️ يجب أن يكون عدد الصور على الأقل 1**")
        return
    
    await event.edit(f"**╮ جـارِ البحث عن {count} صورة لـ {query} في بنترست... 📌╰**")

    temp_dir = None
    try:
        # إنشاء مجلد التحميل المؤقت
        temp_dir = tempfile.mkdtemp()
        
        # تحميل الكوكيز من ملف pincook.txt
        cookies = load_pinterest_cookies()
        
        if not cookies:
            await event.edit("**⚠️ لم يتم العثور على ملف الكوكيز**\n\n**ضع ملف الكوكيز باسم:** `pincook.txt`")
            return
        
        # استخدام معرف فريد للبحث يتضمن التاريخ والوقت لتجنب التكرار
        search_key = f"{query.lower().strip()}-{int(time.time() / 3600)}"  # يتغير كل ساعة
        
        # تحميل الصور مع محاولات متعددة لضمان الحصول على العدد المطلوب
        downloaded_files = []
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                # تنظيف الذاكرة قبل كل محاولة
                gc.collect()
                
                # استخدام offset عشوائي لتجنب تكرار النتائج
                random_offset = random.randint(0, 10) * count
                
                batch_files = await download_pinterest_images(query, count, temp_dir, cookies, random_offset)
                
                # إضافة الملفات الجديدة فقط (تجنب التكرار)
                new_files = []
                for file_path in batch_files:
                    if file_path not in downloaded_files:
                        new_files.append(file_path)
                
                downloaded_files.extend(new_files)
                
                # إذا حصلنا على العدد المطلوب، نتوقف
                if len(downloaded_files) >= count:
                    downloaded_files = downloaded_files[:count]
                    break
                
                # تأخير قصير بين المحاولات
                await asyncio.sleep(1)
                
            except Exception as batch_error:
                print(f"Attempt {attempt + 1} failed: {batch_error}")
                if attempt == max_attempts - 1:
                    raise batch_error
                await asyncio.sleep(2)
        
        if not downloaded_files:
            raise Exception("No images found after all attempts")
        
        await event.edit(f"**╮ ❐ جـارِ رفـع {len(downloaded_files)} صورة ...🖼️╰**")
        
        # إرسال الصور مع تحسينات الذاكرة والتأخير
        for i, image_path in enumerate(downloaded_files, start=1):
            try:
                # تنظيف الذاكرة كل 5 صور
                if i % 5 == 0:
                    gc.collect()
                
                # قراءة الصورة وإرسالها مباشرة لتوفير الذاكرة
                await event.client.send_file(
                    event.chat_id,
                    image_path,
                    caption=f"**الصورة {i} من {len(downloaded_files)} لـ {query}**"
                )
                
                # تأخير ثانية واحدة بين إرسال كل صورة
                if i < len(downloaded_files):  # لا حاجة للتأخير بعد آخر صورة
                    await asyncio.sleep(1)
                
                # حذف الصورة فور إرسالها لتوفير الذاكرة
                try:
                    os.remove(image_path)
                except:
                    pass
                
                # تحديث الرسالة كل 10 صور
                if i % 10 == 0 or i == len(downloaded_files):
                    try:
                        await event.edit(f"**╮ ❐ تم إرسـال {i}/{len(downloaded_files)} صورة ...🖼️╰**")
                    except:
                        pass
                        
            except Exception as upload_error:
                print(f"Error uploading image {i}: {upload_error}")
                continue
        
        # تنظيف نهائي للذاكرة
        gc.collect()
        
        await event.edit(f"**╮ ❐ تم إرسـال {len(downloaded_files)} صورة لـ {query} بنجـاح ✅╰**")

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Main error: {e}")
        
        # تنظيف الذاكرة عند الخطأ
        gc.collect()
        
        if "403" in error_msg or "forbidden" in error_msg:
            await event.edit("**⚠️ تم حظر الوصول - جرب استخدام كوكيز صالح أو VPN**")
        elif "private" in error_msg or "login" in error_msg:
            await event.edit("**⚠️ المحتوى خاص ويتطلب تسجيل دخول - تأكد من صحة الكوكيز**")
        elif "not found" in error_msg or "unavailable" in error_msg:
            await event.edit("**⚠️ لم يتم العثور على صور لهذا البحث**")
        else:
            await event.edit(f"**⚠️ حـدث خـطأ**: {str(e)[:200]}...")

    finally:
        # تنظيف الملفات المؤقتة
        if temp_dir:
            try:
                shutil.rmtree(temp_dir)
            except Exception as cleanup_error:
                print(f"Cleanup error: {cleanup_error}")
        
        # تنظيف نهائي للذاكرة
        gc.collect()


                          
def run_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), handler) as httpd:
        httpd.serve_forever()

# تشغيل الخادم في خيط جديد
server_thread = threading.Thread(target=run_server)
server_thread.start()                
                                              
print("""
$$$$$$$$\ $$$$$$$\  $$$$$$$$\ $$\   $$\ 
$$  _|$$  $$\ $$  ___|$$$\  $$ |
$$ |      $$ |  $$ |$$ |      $$$$\ $$ |
$$$$$\    $$$$$$$  |$$$$$\    $$ $$\$$ |
$$  |   $$  $$< $$  __|   $$ \$$$$ |
$$ |      $$ |  $$ |$$ |      $$ |\$$$ |
$$$$$$$$\ $$ |  $$ |$$$$$$$$\ $$ | \$$ |
\__|\|  \|\__|\|  \|
تـم تـنـصـيـب ســورس ايـريـن بنـجـاح✔️
""")

async def main():
    await start_client()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main()) 
