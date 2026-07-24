# api/events.py
import json
import time
import os
from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_html_files():
    """Barcha HTML fayllarni o'qish (index.html dan tashqari)"""
    files = []
    for file in os.listdir('.'):
        if file.endswith('.html') and file != 'index.html':
            files.append(file)
    return sorted(files)

@app.route('/api/files')
def get_files():
    """Fayllar ro'yxatini qaytarish"""
    return jsonify(get_html_files())

@app.route('/api/events')
def stream_events():
    """SSE - real-time yangilanishlar"""
    def generate():
        last_files = []
        while True:
            try:
                current_files = get_html_files()
                
                # O'zgarishlarni tekshirish
                if current_files != last_files:
                    # Yangi ma'lumot yuborish
                    data = {
                        'type': 'update',
                        'files': current_files,
                        'timestamp': time.time()
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    last_files = current_files
                
                # Har 2 sekundda tekshirish
                time.sleep(2)
                
            except Exception as e:
                print(f"SSE xatolik: {e}")
                time.sleep(5)
    
    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

# Vercel uchun
app = app
