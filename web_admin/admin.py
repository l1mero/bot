import asyncio
import io
import logging
import sys
import threading
from typing import Optional
import bcrypt
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui, run

log_capture_string = io.StringIO()
from users import users_page
from logs import logs
from watchfiles import awatch
# in reality users passwords would obviously need to be hashed
passwords = {'user1': b'$2b$12$aB2I3VTnkiL2zCk08uGkCOHlwswTOaF0jGF0JYEPl4YG8ph34Sl8a'}

unrestricted_page_routes = {'/login'}

class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)


app.add_middleware(AuthMiddleware)


@ui.page('/')
async def main_page() -> None:
    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to('/login')

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('One')
        two = ui.tab('Two')
    with ui.tab_panels(tabs, value=two).classes('w-full'):
        with ui.tab_panel(one):
            global p
            with open('web.log', 'rb') as f:
                f.seek(-16384, 2)
                p = f.read(16384)
            log = ui.log(max_lines=100).style("height: 70vh;")
            def upd():
                global p
                with open('web.log', 'rb') as f:
                    f.seek(-16384 * 4, 2)
                    f = f.read(16384 * 4)
                    a = f.index(p)
                    n = f[a + 16384:]
                    p = f[-16384:]

                    for line in n.split(b'\n')[1:]:
                        log.push(line.decode())



            ui.timer(1, upd)

            ui.button("Clear", on_click=lambda: log.clear())

        with ui.tab_panel(two):
            await users_page()

    ui.button(on_click=logout, icon='logout').props('outline round')


@ui.page('/subpage')
def test_page() -> None:
    ui.label('This is a sub page.')


@ui.page('/login')
def login() -> Optional[RedirectResponse]:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if passwords.get(username.value) and bcrypt.checkpw(password.value.encode(), passwords.get(username.value)):
            app.storage.user.update({'username': username.value, 'authenticated': True})
            ui.navigate.to('/users')  # go back to where the user wanted to go
        else:
            ui.notify('Wrong username or password.', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/users')
    with ui.card().classes('absolute-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
    return None

if __name__ in {'__main__', '__mp_main__'}:
    logging.basicConfig(level=logging.DEBUG, filename="web.log")


    ui.run(storage_secret='THIS_NEEDS_TO_BE_CHANGED', on_air=True)

