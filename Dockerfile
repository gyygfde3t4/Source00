FROM python:3.11-slim

# تحديث النظام وتحميل المكتبات المطلوبة
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libmagickwand-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# إعداد متغيرات البيئة لـ ImageMagick
ENV MAGICK_HOME=/usr
ENV PATH="$MAGICK_HOME/bin:$PATH"

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
