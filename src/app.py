from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import os
import platform
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


def log_watcher():
    """Background file tailer that streams engine telemetry events via WebSockets."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)

    # Path agnostic resolution pattern
    path_options = [
        os.path.join(base_dir, 'edgeguard_local.log'),
        os.path.join(root_dir, 'edgeguard_local.log')
    ]

    log_path = None
    while not log_path:
        for path in path_options:
            if os.path.exists(path) and os.path.getsize(path) > 0:
                log_path = path
                break
        if not log_path:
            time.sleep(1)

    with open(log_path, 'r') as f:
        # Move file cursor matrix pointer directly to the EOF
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line or not line.strip():
                time.sleep(0.5)  # Wait for daemon clock interval
                continue
            try:
                data = json.loads(line.strip())
                # Dynamic Environment Awareness Feature
                data["platform"] = platform.system()  # Injects Windows or Linux automatically

                # Instantly broadcast downstream to the active browser clients
                socketio.emit('telemetry_update', data)
            except Exception:
                pass


if __name__ == '__main__':
    # Threading strategy handles the I/O locking architecture smoothly inside PyCharm
    watcher_thread = threading.Thread(target=log_watcher, daemon=True)
    watcher_thread.start()

    print("[*] EdgeGuard UI Server successfully online at http://127.0.0.1:5000")

    # FIX ADDED HERE: allow_unsafe_werkzeug=True added to bypass the development runtime block
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)