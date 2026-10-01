# mobile_mode/mobile_eel.py - FINAL WORKING VERSION
import eel
import requests
import subprocess
import time
import sys
import os
import flet as ft

# PHP backend URL
PHP_API_URL = "http://localhost:8080/auth_api.php"

# EEL init (Required for exposing functions)
eel.init("web")


@eel.expose
def login_via_php(username, password):
    """EEL function that calls PHP backend"""
    try:
        print(f"🔍 Sending request to PHP: {PHP_API_URL} with user: {username}")  # Debug print
        response = requests.post(
            PHP_API_URL,
            json={"username": username, "password": password},
            timeout=5
        )
        print(f"✅ PHP Response: {response.status_code} - {response.text}")  # Debug print
        return response.json()
    except requests.exceptions.ConnectionError:
        print("❌ PHP backend not running!")
        return {"success": False, "message": "PHP backend not running! Check if PHP server is started."}
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


def start_php_server():
    """Start PHP backend"""
    try:
        proc = subprocess.Popen(
            ["php", "-S", "localhost:8080", "-t", "../php_backend"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("✅ PHP server started on http://localhost:8080")
        return proc
    except FileNotFoundError:
        print("❌ PHP not found! Please install PHP and add to PATH.")
        raise SystemExit(1)


def main(page: ft.Page):
    """Flet Main UI"""
    page.title = "🔐 Login - Mobile EEL"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20
    page.window_width = 420
    page.window_height = 780
    page.window_resizable = True
    page.bgcolor = ft.Colors.GREY_100  # ✅ Updated to new Colors syntax

    # State variables
    alert_text = ft.Text("", color=ft.Colors.WHITE)

    def show_alert(msg, is_success):
        alert_text.value = f"{'✅' if is_success else '❌'} {msg}"
        alert_text.color = ft.Colors.GREEN if is_success else ft.Colors.RED
        alert_container.bgcolor = ft.Colors.GREEN_100 if is_success else ft.Colors.RED_100
        alert_container.visible = True
        page.update()
        # Auto-hide after 3 seconds
        import threading
        threading.Timer(3.0, lambda: setattr(alert_container, 'visible', False) or page.update()).start()

    def login_clicked(e):
        u = username_field.value.strip()
        p = password_field.value.strip()

        if not u or not p:
            show_alert("Fill all fields!", False)
            return

        login_btn.disabled = True
        login_btn.text = "Checking..."
        page.update()

        # ⚠️ IMPORTANT: Direct function call, NOT async/await
        # EEL ke expose functions sync hote hain
        try:
            result = login_via_php(u, p)

            if result["success"]:
                show_alert(result["message"], True)
            else:
                show_alert(result["message"], False)
        except Exception as ex:
            show_alert(f"Error: {str(ex)}", False)

        login_btn.disabled = False
        login_btn.text = "Sign In →"
        page.update()

    # UI Components with ✅ Updated Flet 0.25+ Syntax
    title = ft.Text("🔐 Welcome Back", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO)
    subtitle = ft.Text("Sign in - Mobile (Flet)", size=14, color=ft.Colors.GREY_600)

    username_field = ft.TextField(
        label="Username",
        hint_text="Enter username",
        prefix_icon=ft.Icons.PERSON,  # ✅ Fixed: ft.Icons.PERSON instead of ft.icons.PERSON
        border_color=ft.Colors.INDIGO_400,
        width=320,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )

    password_field = ft.TextField(
        label="Password",
        hint_text="Enter password",
        prefix_icon=ft.Icons.LOCK,  # ✅ Fixed: ft.Icons.LOCK
        password=True,
        can_reveal_password=True,
        border_color=ft.Colors.INDIGO_400,
        width=320,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )

    login_btn = ft.ElevatedButton(
        text="Sign In →",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
        width=320,
        on_click=login_clicked,
    )

    alert_container = ft.Container(
        content=alert_text,
        visible=False,
        padding=10,
        border_radius=10,
        width=320,
    )

    hint = ft.Text("💡 Demo: admin / 1234 or user / pass", size=12, color=ft.Colors.GREY_500)

    # Main Card Layout
    card = ft.Container(
        content=ft.Column(
            [
                title,
                subtitle,
                ft.Container(height=10),
                alert_container,
                username_field,
                password_field,
                ft.Container(height=10),
                login_btn,
                ft.Container(height=10),
                hint,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor=ft.Colors.WHITE,
        padding=30,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.3, ft.Colors.INDIGO)),
        width=380,
    )

    # Add everything to page
    page.add(card)


if __name__ == "__main__":
    print("🚀 Starting PHP backend on http://localhost:8080")
    php_proc = start_php_server()
    time.sleep(1)

    print("📱 Starting Flet mobile app (Native UI)...")
    ft.app(target=main)

    # Cleanup
    php_proc.terminate()
    print("✅ App closed. PHP server stopped.")