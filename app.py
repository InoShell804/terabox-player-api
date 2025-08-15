from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/box/terabox/<surl>', methods=['GET'])
def get_video_link(surl):
    if not surl:
        return jsonify({"error": "surl is missing from the path"}), 400

    terabox_url = f"https://www.terabox.com/s/1{surl}"

    try:
        headers = { 'User-Agent': 'Mozilla/5.0' }
        response = requests.get(terabox_url, headers=headers, allow_redirects=True)
        response.raise_for_status()
        html_content = response.text
        
        match = re.search(r'dlink":"([^"]+)"', html_content)
        if not match:
            thumb_match = re.search(r'"thumbs":{"url3":"([^"]+)"', html_content)
            if thumb_match:
                dlink = thumb_match.group(1).replace("&size=256x256", "").replace("?thumbnail=1", "")
                return jsonify({"dlink": dlink})
            else:
                return jsonify({"error": "Could not find the direct video link."}), 404

        dlink = match.group(1).replace("\\", "")
        return jsonify({"dlink": dlink})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "API is running!"
