#!/bin/bash

echo "🎬 بدء إعداد MoviePy..."

# التأكد من وجود المجلدات المطلوبة
mkdir -p /tmp/moviepy
chmod 777 /tmp/moviepy

# تحديد متغيرات البيئة
export IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg
export FFMPEG_BINARY=/usr/bin/ffmpeg
export MOVIEPY_TEMP_PREFIX=/tmp/moviepy

# اختبار ffmpeg
echo "🔧 اختبار ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg موجود: $(ffmpeg -version | head -n1)"
else
    echo "❌ ffmpeg غير موجود!"
    exit 1
fi

# اختبار ImageMagick
echo "🔧 اختبار ImageMagick..."
if command -v convert &> /dev/null; then
    echo "✅ ImageMagick موجود: $(convert -version | head -n1)"
else
    echo "❌ ImageMagick غير موجود!"
    exit 1
fi

# اختبار Python وMoviePy
echo "🐍 اختبار Python وMoviePy..."
python3 -c "
try:
    import moviepy
    from moviepy.editor import ColorClip
    print('✅ MoviePy يعمل بشكل صحيح')
    
    # اختبار عملي سريع
    clip = ColorClip(size=(10,10), color=(255,0,0), duration=0.1)
    clip.close()
    print('✅ الاختبار العملي نجح')
    
except Exception as e:
    print(f'❌ خطأ في MoviePy: {e}')
    exit(1)
"

echo "🎯 انتهى إعداد MoviePy بنجاح!"
