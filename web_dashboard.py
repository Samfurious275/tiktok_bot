# web_dashboard.py

from flask import Flask, render_template, request, jsonify
import threading
import logging
import main  # Will use config.py globals

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log storage
logs = []

def log_message(msg):
    print(msg)
    logs.append(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_bot', methods=['POST'])
def start_bot():
    data = request.json
    edit_mode = data.get('edit_mode', True)
    keep_audio = data.get('keep_audio', True)

    # ✅ Dynamically update config.py variables
    import config

    config.EDIT_MODE = edit_mode
    config.KEEP_AUDIO = keep_audio
    config.REMOVE_AUDIO = not keep_audio

    log_message(f"[⚙️] Settings: Edit Mode = {edit_mode}, Keep Audio = {keep_audio}")

    def run_bot():
        try:
            log_message("[🟢] Starting TikTok Reel Bot...")
            main.job()
            log_message("[✅] Bot job completed.")
        except Exception as e:
            log_message(f"[❌] Error: {str(e)}")

    thread = threading.Thread(target=run_bot)
    thread.start()

    return jsonify({
        "status": "Bot started",
        "edit_mode": edit_mode,
        "keep_audio": keep_audio
    })

@app.route('/logs')
def get_logs():
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
