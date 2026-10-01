# web_mode/web_eel.py - SIRF BROWSER MODE
import eel
import requests
import subprocess
import time
import sys
import os

# PHP backend URL
PHP_API_URL = "http://localhost:8080/auth_api.php"

# HTML embedded directly in Python (EEL style)
HTML_UI = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Web EEL</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; display: flex; justify-content: center; align-items: center;
            padding: 20px;
        }
        .login-container {
            background: rgba(255,255,255,0.95);
            padding: 50px 40px;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 420px;
            animation: slideUp 0.7s ease;
        }
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
        .login-container h2 { text-align: center; color: #2d3748; margin-bottom: 8px; font-size: 26px; }
        .subtitle { text-align: center; color: #718096; font-size: 14px; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; }
        .input-group label { display: block; margin-bottom: 8px; color: #4a5568; font-weight: 600; }
        .input-group input {
            width: 100%; padding: 14px 16px; border: 2px solid #e2e8f0;
            border-radius: 12px; font-size: 15px; background: #f7fafc; color: #2d3748;
        }
        .input-group input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,0.15); }
        .login-btn {
            width: 100%; padding: 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer;
        }
        .login-btn:hover { transform: translateY(-2px); }
        .login-btn:disabled { opacity: 0.7; cursor: not-allowed; }
        .alert {
            padding: 14px; border-radius: 10px; margin-bottom: 20px; display: none;
            text-align: center; font-weight: 600;
        }
        .alert-success { background: #c6f6d5; color: #22543d; }
        .alert-error { background: #fed7d7; color: #742a2a; }
        .badge { position: fixed; top: 12px; right: 16px; background: rgba(255,255,255,0.2); color: #fff; padding: 5px 12px; border-radius: 20px; font-size: 12px; }
        @media (max-width: 400px) {
            .login-container { padding: 25px 20px; }
            .login-container h2 { font-size: 22px; }
            .input-group input { padding: 12px 14px; font-size: 14px; }
            .login-btn { padding: 14px; font-size: 14px; }
        }
    </style>
</head>
<body>
    <div class="badge">🌐 Web Mode - EEL</div>
    <div class="login-container">
        <h2>🔐 Welcome Back</h2>
        <p class="subtitle">Sign in - Web (EEL)</p>
        <div id="alertBox" class="alert"></div>
        <form id="loginForm" onsubmit="return handleLogin(event)">
            <div class="input-group">
                <label>Username</label>
                <input type="text" id="username" placeholder="Enter username" required>
            </div>
            <div class="input-group">
                <label>Password</label>
                <input type="password" id="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="login-btn" id="loginBtn">Sign In →</button>
        </form>
        <p style="text-align: center; color: #718096; font-size: 12px; margin-top: 20px;">💡 Demo: admin / 1234 or user / pass</p>
    </div>
    <script src="/eel.js"></script>
    <script>
        async function handleLogin(e) {
            e.preventDefault();
            const u = document.getElementById('username').value.trim();
            const p = document.getElementById('password').value.trim();
            const btn = document.getElementById('loginBtn');

            if (!u || !p) { showAlert('Fill all fields!', 'error'); return false; }

            btn.disabled = true;
            btn.textContent = 'Checking...';
            try {
                const result = await eel.login_via_php(u, p)();
                showAlert((result.success ? '✅ ' : '❌ ') + result.message, result.success ? 'success' : 'error');
            } catch (err) {
                showAlert('❌ Could not reach backend!', 'error');
            } finally {
                btn.disabled = false;
                btn.textContent = 'Sign In →';
            }
            return false;
        }
        function showAlert(msg, type) {
            const box = document.getElementById('alertBox');
            box.textContent = msg; box.className = 'alert alert-' + type;
            box.style.display = 'block';
            setTimeout(() => box.style.display = 'none', 3000);
        }
    </script>
</body>
</html>
"""

# Create web folder with HTML
if not os.path.exists("web"):
    os.makedirs("web")
with open("web/login.html", "w", encoding="utf-8") as f:
    f.write(HTML_UI)

# EEL init - this will serve the HTML
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


def start_php_server():
    """Start PHP built-in server"""
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


if __name__ == "__main__":
    print("🚀 Starting PHP backend on http://localhost:8080")
    php_proc = start_php_server()
    time.sleep(1)

    print("🌐 Starting EEL web app in default browser...")

    # 🚀 KEY CHANGE: mode="default" ensures it opens in browser, not in separate window
    try:
        eel.start("login.html", size=(480, 780), port=8000, mode="default")
    except Exception as e:
        print(f"⚠️ Error: {e}")
    finally:
        php_proc.terminate()