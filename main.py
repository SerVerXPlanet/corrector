import keyboard as kb
import pyperclip as clp
from enum import Enum
import pystray as tray
import PIL.Image as Img
from webbrowser import open as open_url
from time import sleep
import io
import base64
import os


class Layout(Enum):
    EN = 0
    RU = 1


charsets = (
    "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM`~@#$^&\\|[]{}'",
    "йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ№"
)

symbols = (
    "`qwertyuiop[]asdfghjkl;'zxcvbnm,./~@#$^&|QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?",
    "ёйцукенгшщзхъфывапролджэячсмитьбю.Ё\"№;:?/ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
)

name = 'corrector'
info = 'Converter text layouts'
base64_icon = (
    'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAABnRSTlMA/wD/AP83WBt9AAAACXBIWXMAAAsTAAALEwEAmpwYAAAMK0lEQVRIxwEgDN'
    '/zAP///////////////////////////////////////////////////////4gAFYgAFf/19f/5+f/8/P///////4gAFf///z9NnD9NnP//////////'
    '/////////////////wQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACJARYAAAB36dQA+fkA/v4ABAQA/v6JBhsAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////////////////////////////////////////////////iAAViAAV/93d/+Li/+fn/+zs//HxiAAV'
    'iAAV////P02cAKLoAKLoP02c////////////////////////BAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIkBFgAAAHfNuAD39wD8/A'
    'D9/QD+/okUKQAAAHf/6gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACJARYAAAB3'
    'vagA9/cA9vYA+PgA9/eJGzAAAAB3/+oAAABATp3BVUwAAAAAAADBVUxATp0AAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAiQEWAAAAd62YAPf3AP39AP39AP39iTlOAAAAd//qAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAIkBFgAAAHechwD19QD19QD29gD19Yk5TgAAAHf/6gAAAAAAAEBOncFVTAAAAAAAAAAAAAAAAMFVTEBOnQAAAAAAAAAAAAAAAAQAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAACJARYAAAB3inUA9fUA/PwA/f0A/PyJUGUAAAB3/+oAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAiQEWAAAAd3lkAPb2APX1APX1APX1iVtwAAAAd//qAAAAAAAAAAAAQE6dwVVMAAAAAAAAAAAAAAAAAA'
    'AAAAAAwVVMQE6dAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAIkBFgAAAHdpVAD29gD8/AD8/AD9/YlziAAAAHf/6gAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH///8AAAAAAAAAAACJARYAAAB3WUQABgYABgYABwcABgaJjqMAAAB3/+oAAAAAAAAAAAAAAA'
    'BATp3BVUwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/q7TAsmMAAAAEAAAAAAAAAAAAAAAAAAAAd0w3APj4AP39AP39AP39AP39AAAAd//qAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAAD5+QD4+AD4+AD4+AD39w'
    'D29gAAAAAAAAAAAAAAAAAAAAAAAEBOncFVTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMFVTEBOnQAAAAQAAAAAAAAAAAAAAAAAAAAA+fkA'
    '/f0A/f0A/f0A/f0A/f0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAA'
    'AAAAAAAAAAAPr6AP7+AP7+AP7+AP7+APz8AAAAAAAAAAAAAAAAAAAAQE6dwVVMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwVVM'
    'QE6dBAAAAAAAAAAAAAAAAAAAAAD7+wD+/gD9/QD9/QD9/QAFBQAAAAAAAAAAAAAAAAAAAAAAAD+rtAAAAAAAAAAAAM1ZTfz/APz+//z/AAAAAAAAAD'
    '+rtAAAAAAAAAAAAAAAAASJARYAAAAAAAAAAAAAAAAAAAAA/f0A//8A//8A/v4A/v4AAACJARYAAAAAAAAAAADA/+oAAAAAAAAAAABATp0JBAH6/f8D'
    'AQEC/gD8///+/wAAAADAsmMAAAAAAAAAAAAEAAAAdzMeAAAAAAAAAAAAAAAAAAAAAP7+AP7+APv7AAAAdzMeAAAAAAAAAAAAic3iAAAAAAAAAAAAAA'
    'AAAAAACQMBAwEA+/4AAwH/+/4B/P//AAAAAAAAAAAAAAAAAAAAAnf/6onN4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAInN4nf/'
    '6gAAAAAAAAAAAAAAAAAAAAsEAQoDAQkDAQkDAQgDAQcCAQAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALBAEEAQAF/gD6/gAE/v/6/gEAAAAAAAAAAAAAAAAAAAACAAAAd//qic3iAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAic3id//qAAAAAAAAAAAAAAAAAAAAAAAADQUBDAUBCwQBCgQBCgMBCgMBAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBOnQAAAAwEAQUCAAUCAAX9APkCABqZsAAAAAAAAAAAAAAAAAAAAAH/'
    '//8AAAAAAACJARZ3Mx4AAAAAAAAAAAAAAAAAAAAAAAAAAACJzeJ3/+oAAAAAAAAAAAAAAABATp0AAAAkeVX4/f/4/f/4/QD4/f/8k64AAADAsmMAAA'
    'AAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQE6dAAAAOYFX+P3/BQIABQIBBQL/9JCt'
    'AAAAwLJjAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAHf/6onN4gAAAAAAAAAAAAAAAAAAAAAAAInN4nf/6gAAAAAAAAAAAEBOnQAAAFCJWQ8FAQ4FAQ'
    '4FAg4FAeeLrAAAAMCyYwAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABATp0AAABl'
    'kVv4/f8FAgAFAgEGAv/JgKkAAADAsmMAAAAAAAAAAAAAAAAAAAAAAAAAAAAB////AAAAAAAAAAAAAAAAiQEWdzMeAAAAAAAAAAAAic3id//qAAAAAA'
    'AAQE6dAAAAephd+f7/+P3/+P0A+P3/pXOmAAAAwLJjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAEBOnQAAAI6gXvn9AAX9AAUCAQUC/51wpQAAAMCyYwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH///8AAAAAAAAAAAAAAAAAAA'
    'CJARZ3Mx4AAACJzeJ3/+oAAABATp0AAACfpmD6/v/6/gD5/f/5/QB7ZKIAAADAsmMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQE6dAAAAr6xh+v4ABf4ABf4ABAEAdGGhAAAAwLJjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAf///wAAAAAAAAAAAAAAAAAAAAAAAIkBFgAAAHf/6kBOnQAAALuwY/z///v+APv+//v+AFhXnwAAAMCyYwAAAAAAAAAAAAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAsmMAAAAD/wEDAf8DAQFTVZ4AAADAsmMAAAAAAAAAAAAAAA'
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBimdLlGW3lAAAAABJRU5ErkJggg=='
)

copy_keys = 'ctrl+c'
paste_keys = 'ctrl+v'

convert_keys = 'ctrl+`'
buffer_keys = 'ctrl+1'

menu_use = 'How to use'
menu_github = 'GitHub'
menu_exit = 'Exit'

url = r'https://github.com/SerVerXPlanet/corrector'

help_text = ('To change the layout of the text \n'
             '- in the selected text, press \"CTRL+~\"\n'
             '- in the clipboard, press \"CTRL+1\" or double click mouse on system tray icon.')

pause = 0.05


def main():
    logo = io.BytesIO(base64.b64decode(base64_icon))
    ico = Img.open(logo)

    menu = tray.MenuItem(menu_exit, on_clicked),

    if os.name == 'nt':
        menu = (tray.MenuItem(menu_use, lambda icon: icon.notify(help_text, title='corrector: help')),
                tray.MenuItem(menu_github, on_clicked),) + menu

    app = tray.Icon(name, ico, title=info, menu=tray.Menu(*menu))

    app.run(startapp)


def startapp(icon: tray.Icon) -> None:
    icon.visible = True

    if icon.visible:
        kb.add_hotkey(convert_keys, lambda: convert(), suppress=True)
        kb.add_hotkey(buffer_keys, lambda: convert_buffer(), suppress=True)


def on_clicked(icon: tray.Icon, item: tray.MenuItem) -> None:
    if str(item) == menu_github:
        open_url(url, new=2)
    elif str(item) == menu_exit:
        icon.visible = False
        icon.stop()


def convert():
    buffer = clp.paste()
    sleep(pause)

    kb.press_and_release(copy_keys)
    sleep(pause)

    convert_buffer()

    kb.press_and_release(paste_keys)
    sleep(pause)

    clp.copy(buffer)
    sleep(pause)


def convert_buffer():
    txt = clp.paste()
    sleep(pause)

    lang = define_keyboard_layout(txt)
    new_lang = (lang + 1) % len(Layout)
    txt = replace_layout(txt, lang, new_lang)

    clp.copy(txt)
    sleep(pause)


def define_keyboard_layout(txt: str) -> int:
    count_layouts = len(Layout)
    marks = [0] * count_layouts

    for i in range(count_layouts):
        for c in txt:
            marks[i] += (c in charsets[i])

    max_index = marks.index(max(marks))

    return max_index


def replace_layout(txt: str, old_lang: int, new_lang: int) -> str:
    new_txt = []

    for c in txt:
        ind = symbols[old_lang].find(c)
        new_txt.append(symbols[new_lang][ind] if ind != -1 else c)

    return ''.join(new_txt)


if __name__ == '__main__':
    main()
