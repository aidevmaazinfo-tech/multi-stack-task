"""
🔷 FLET - HTML/CSS Login Page Embedded in Python
Browser Mode (NO download required!)

Run:  python embed_flet.py
"""

import flet as ft
from urllib.parse import quote
import os

HTML_PATH = os.path.join(os.path.dirname(__file__), "login_page.html")

def main(page: ft.Page):
    page.title = "Flet App with HTML/CSS UI"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.colors.TRANSPARENT

    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    encoded_html = quote(html_content, safe='')
    data_uri = f"data:text/html;charset=utf-8,{encoded_html}"

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.DESKTOP_WINDOWS, color=ft.colors.WHITE, size=24),
            ft.Text("Flet App", color=ft.colors.WHITE, size=18, weight=ft.FontWeight.BOLD),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Text("HTML Inside", color=ft.colors.WHITE70, size=12),
                bgcolor=ft.colors.WHITE10, border_radius=15,
                padding=ft.padding.symmetric(horizontal=12, vertical=6)
            )
        ]),
        bgcolor=ft.colors.INDIGO_600, padding=15,
        border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
    )

    web_view = ft.WebView(url=data_uri, expand=True)

    footer = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.CODE, color=ft.colors.INDIGO_400, size=16),
            ft.Text("Python Flet + HTML/CSS", color=ft.colors.GREY_500, size=12),
            ft.Container(expand=True),
            ft.Text("🔷 Browser Mode", color=ft.colors.INDIGO_400, size=12, weight=ft.FontWeight.BOLD)
        ]),
        padding=10,
        border=ft.border.only(top=ft.border.BorderSide(1, ft.colors.GREY_200))
    )

    page.add(ft.Column([header, web_view, footer], expand=True, spacing=0))


if __name__ == "__main__":
    print("🚀 Starting Flet in Browser Mode...")
    print("   Chrome/Edge mein khulega automatically")
    print("   URL: http://localhost:8550")

    # ✅ WEB_BROWSER = No download needed! Desktop client nahi chahiye.
    ft.run(main, view=ft.AppView.WEB_BROWSER, port=8550)