# desktop_mode/desktop_eel.py - RESPONSIVE WINDOW VERSION
import eel
import requests
import subprocess
import time
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QResizeEvent

# PHP backend URL
PHP_API_URL = "http://localhost:8080/auth_api.php"

# EEL init - serve web folder
eel.init("web")


@eel.expose
def login_via_php(username, password):
    """EEL function that calls PHP backend"""
    try:
        response = requests.post(
            PHP_API_URL,
            json={"username": username, "password": password},
            timeout=5
        )
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "PHP backend not running!"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


class DesktopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Login - Desktop EEL")
        self.setMinimumSize(400, 600)  # Minimum window size
        self.resize(500, 750)  # Default window size

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://localhost:8000/login.html"))
        layout.addWidget(self.web_view)

    def resizeEvent(self, event: QResizeEvent):
        """Window resize hone par UI auto adjust ho"""
        super().resizeEvent(event)
        # WebView automatically adjusts, no extra code needed
        # But you can add zoom or custom logic here if needed


def start_php_server():
    try:
        proc = subprocess.Popen(
            ["php", "-S", "localhost:8080", "-t", "../php_backend"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return proc
    except FileNotFoundError:
        print("❌ PHP not found! Please install PHP and add to PATH.")
        raise SystemExit(1)


def start_eel_subprocess():
    """EEL server ko alag Python process mein chalayen"""
    script_content = """
import eel
import requests
import os

eel.init("web")

@eel.expose
def login_via_php(username, password):
    try:
        response = requests.post(
            "http://localhost:8080/auth_api.php",
            json={"username": username, "password": password},
            timeout=5
        )
        return response.json()
    except:
        return {"success": False, "message": "PHP backend not running!"}

# mode=None => No browser, block=True => keeps running
eel.start("login.html", port=8000, mode=None, block=True)
"""

    temp_file = "temp_eel_server.py"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    proc = subprocess.Popen(
        [sys.executable, temp_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return proc, temp_file


if __name__ == "__main__":
    print("🚀 Starting PHP backend on http://localhost:8080")
    php_proc = start_php_server()
    time.sleep(1)

    print("🖥️ Starting EEL server in subprocess (no browser)...")
    eel_proc, temp_file = start_eel_subprocess()

    time.sleep(3)  # Wait for EEL to start

    print("🖥️ Starting responsive desktop window (PyQt5)...")
    app = QApplication(sys.argv)
    window = DesktopWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    finally:
        php_proc.terminate()
        eel_proc.terminate()
        if os.path.exists(temp_file):
            os.remove(temp_file)