"""
📱 FLET MOBILE APP - HTML/CSS Login Page Embedded in Python

Yeh file mobile devices (Android/iOS) ke liye optimized hai.
Same HTML/CSS login page Flet app ke andar render hota hai.

BUILD COMMANDS:
    Android:  flet build apk
    iOS:      flet build ipa
    Web:      flet build web

INSTALL:
    pip install flet

RUN (for testing on desktop):
    python embed_flet_mobile.py
"""

import flet as ft
from urllib.parse import quote
import os

HTML_PATH = os.path.join(os.path.dirname(__file__), "login_page.html")


def main(page: ft.Page):
    # Mobile-optimized settings
    page.title = "Login App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO  # Mobile pe scroll zaroori

    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.INDIGO,
        use_material3=True,
    )

    # HTML read karo
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    encoded_html = quote(html_content, safe='')
    data_uri = f"data:text/html;charset=utf-8,{encoded_html}"

    # Mobile App Bar
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.LOCK_PERSON, color=ft.colors.WHITE),
        title=ft.Text("Login Portal", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.colors.INDIGO_600,
    )

    # WebView - HTML render hoga
    web_view = ft.WebView(url=data_uri, expand=True)

    # Mobile Bottom Navigation
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        bgcolor=ft.colors.WHITE,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.LOGIN, label="Login"),
            ft.NavigationBarDestination(icon=ft.icons.INFO, label="Info"),
            ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
        ],
    )

    # Floating Action Button
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.REFRESH,
        bgcolor=ft.colors.INDIGO_600,
        on_click=lambda e: setattr(web_view, 'url', data_uri) or page.update()
    )

    page.add(ft.Container(content=web_view, expand=True))


if __name__ == "__main__":
    # ✅ Cross-version compatible
    try:
        ft.run(main, view=ft.AppView.FLET_APP)          # Newer versions
    except TypeError:
        try:
            ft.run(target=main, view=ft.AppView.FLET_APP)  # Some versions
        except:
            ft.app(target=main, view=ft.AppView.FLET_APP)  # Older versions