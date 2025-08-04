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

# تحديث pip وتثبيت المكتبات الأساسية
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy>=1.24.0 \
    imageio>=2.31.0 \
    decorator>=5.1.0 \
    proglog>=0.1.9 \
    tqdm>=4.64.0

# تثبيت مكتبات معالجة الصور
RUN pip install --no-cache-dir \
    Pillow>=10.0.0 \
    Wand>=0.6.11

# تثبيت MoviePy مع إعداد ffmpeg path
RUN pip install --no-cache-dir moviepy>=1.0.3

# تثبيت باقي المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# التحقق من ffmpeg
RUN ffmpeg -version && echo "✅ FFmpeg يعمل بشكل صحيح"

# اختبار المكتبات
RUN python -c "\
import sys; \
print('🐍 Python version:', sys.version); \
import os; \
os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/bin/ffmpeg'; \
libraries = {'imageio': 'imageio', 'numpy': 'numpy', 'PIL': 'PIL', 'wand': 'wand.api', 'moviepy': 'moviepy'}; \
for name, module in libraries.items(): \
    try: \
        lib = __import__(module, fromlist=['']); \
        version = getattr(lib, '__version__', 'غير معروف'); \
        print(f'✅ {name}: {version}'); \
    except Exception as e: \
        print(f'❌ {name}: {e}'); \
print('🎬 اختبار MoviePy...'); \
try: \
    from moviepy.editor import ColorClip; \
    test_clip = ColorClip(size=(10, 10), color=(255, 0, 0), duration=0.1); \
    test_clip.close(); \
    print('✅ MoviePy: الاختبار العملي نجح'); \
except Exception as e: \
    print(f'⚠️ MoviePy test: {e}'); \
print('🎯 انتهى الاختبار!')"

# نسخ ملفات البوت
COPY . .

# إنشاء نقطة صحة للحاوية
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import moviepy; print('صحي')" || exit 1

# تشغيل البوت
CMD ["python", "source.py"]
