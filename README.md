# 🛡️ EdgeGuard-Core

An advanced, cross-platform infrastructure and system telemetry monitoring platform. EdgeGuard tracks real-time node vitals (such as RAM, CPU, and platform status) through an asynchronous background architecture and streams them instantly to an interactive dashboard using Python, Flask, and WebSockets.

---

## 🚀 Key Features

* **Real-Time Data Streaming:** Leverages high-performance WebSockets (`Flask-SocketIO`) to push system telemetry updates down to the browser client instantly without polling.
* **Asynchronous Processing:** Built using a multi-threaded architecture featuring a robust background engine decoupled from the web layer.
* **Cross-Platform Ready:** Fully compatible with both **Windows** and **Linux** environments. Automatically detects the host OS matrix and displays native badges on the UI.
* **Demo-Ready Mock Data:** Includes a built-in mock simulation system for rapid presentation and sandbox demos without requiring full infrastructure access.

---

## 🏗️ Architectural Component Core

1.  **Telemetry Collection Engine (`daemon.py`):** Runs in the background to handle data capture (or simulated sandbox mock streams) and write live metrics logs.
2.  **Flask WebSocket Server (`app_flask.py`):** Acts as a path-agnostic log tailer that moves cursors directly to the End-of-File (EOF) and broadcasts new events to browser clients
