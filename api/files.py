# api/files.py
import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/files')
def list_files():
    """Barcha HTML fayllarni ro'yxatini qaytaradi"""
    try:
        files = []
        # Joriy papkadagi barcha fayllarni skaner qilish
        for file in os.listdir('.'):
            # .html bilan tugaydigan va index.html bo'lmagan fayllar
            if file.endswith('.html') and file != 'index.html':
                files.append(file)
        
        # Tartiblash
        files.sort()
        return jsonify(files)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel uchun
app = app
