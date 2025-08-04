FROM python:3.11-slim

# إعداد متغيرات البيئة مبكراً
ENV DEBIAN_FRONTEND=noninteractive
ENV MAGICK_HOME=/usr
ENV PATH="$MAGICK_HOME/bin:$PATH"
ENV IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg
ENV FFMPEG_BINARY=/usr/bin/ffmpeg
ENV MOVIEPY_TEMP_PREFIX=/tmp/moviepy

# تحديث النظام وتحميل المكتبات المطلوبة
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    libmagickwand-dev \
    pkg-config \
    wget \
    curl \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavfilter-dev \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مجلدات مؤقتة
RUN mkdir -p /tmp/moviepy && chmod 777 /tmp/moviepy

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.txt .

# تحديث pip
RUN pip install --no-cache-dir --upgrade pip

# تحميل وإعداد imageio-ffmpeg بشكل منفصل
RUN pip install --no-cache-dir imageio-ffmpeg && \
    python -c "import imageio_ffmpeg; imageio_ffmpeg.download()" && \
    echo "✅ imageio-ffmpeg تم إعداده بنجاح"

# تثبيت المكتبات الأساسية أولاً
RUN pip install --no-cache-dir \
    numpy>=1.24.0 \
    imageio>=2.31.0 \
    decorator>=5.1.0 \
    proglog>=0.1.9 \
    tqdm>=4.64.0

# تثبيت مكتبات معالجة الصور
RUN pip install --no-cache-dir \
    Pillow>=10.0.0 \
    Wand>=0.6.11

# تثبيت MoviePy
RUN pip install --no-cache-dir moviepy>=1.0.3

# تثبيت باقي المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# التحقق الشامل من التثبيت
RUN python -c "\
import sys; \
print('🐍 Python version:', sys.version); \
libraries = ['imageio', 'numpy', 'PIL', 'wand', 'moviepy']; \
[print(f'✅ {lib}: {getattr(__import__(lib), \"__version__\", \"غير معروف\")}') if __import__(lib) else print(f'❌ {lib}: failed') for lib in libraries]; \
from moviepy.editor import ColorClip; \
test_clip = ColorClip(size=(10, 10), color=(255, 0, 0), duration=0.1); \
test_clip.close(); \
print('✅ MoviePy: الاختبار العملي نجح'); \
print('🎯 جميع الاختبارات اكتملت!')"

# نسخ سكريبت الإعداد
COPY setup_moviepy.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/setup_moviepy.sh

# نسخ ملفات البوت
COPY . .

# إنشاء نقطة صحة للحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import moviepy; print('صحي')" || exit 1

# تشغيل البوت
CMD ["python", "source.py"]
