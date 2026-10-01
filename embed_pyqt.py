import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_page.html")

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt App with HTML/CSS UI")
        self.setGeometry(400, 100, 520, 800)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QWidget()
        header.setStyleSheet("background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #667eea,stop:1 #764ba2);")
        header.setFixedHeight(60)
        hlayout = QHBoxLayout(header)
        hlayout.setContentsMargins(20, 0, 20, 0)
        title = QLabel("🖥️ PyQt Desktop App")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        hlayout.addWidget(title)
        hlayout.addStretch()
        layout.addWidget(header)

        # WebView
        with open(HTML_PATH, 'r', encoding='utf-8') as f:
            html_content = f.read()

        self.web_view = QWebEngineView()
        self.web_view.setHtml(html_content)
        layout.addWidget(self.web_view, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())