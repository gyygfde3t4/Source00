FROM python:3.11-slim

# تحديث النظام وتحميل المكتبات المطلوبة
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libmagickwand-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تحميل المكتبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ ملفات البوت
COPY . .

# تشغيل البوت
CMD ["python", "source.py"]
