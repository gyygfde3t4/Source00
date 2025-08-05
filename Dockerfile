FROM python:3.11-slim

# إعداد متغيرات البيئة
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# تحديث النظام وتثبيت المكتبات المطلوبة فقط
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تحديث pip وتثبيت المكتبات
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# التحقق من ffmpeg والمكتبات الأساسية
RUN ffmpeg -version && echo "✅ FFmpeg يعمل بشكل صحيح"

# اختبار سريع للمكتبات الأساسية
RUN python -c "import telethon, PIL, requests, mutagen, pytz; print('✅ جميع المكتبات تم تثبيتها بنجاح!')"

# نسخ ملفات البوت
COPY . .

# تشغيل البوت
CMD ["python", "source.py"]
