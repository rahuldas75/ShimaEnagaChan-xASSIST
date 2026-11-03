import time
import urllib.parse
import webbrowser
import pyautogui
import pygetwindow as gw


BROWSER_LOAD_DELAY = 3.5
POST_SETTLE_DELAY = 1.2


def dispatch_post(text: str, auto_close: bool = True) -> bool:
    """
    Open an X composer and optionally submit it with Ctrl+Enter.
    """
    if not text or not text.strip():
        return False

    encoded_text = urllib.parse.quote(text.strip())
    intent_url = f"https://x.com/compose/post?text={encoded_text}"

    webbrowser.open(intent_url)
    time.sleep(BROWSER_LOAD_DELAY)

    try:
        active_win = gw.getActiveWindow()
        if active_win:
            active_win.activate()
    except Exception:
        pass

    pyautogui.hotkey("ctrl", "enter")

    if auto_close:
        time.sleep(POST_SETTLE_DELAY)
        pyautogui.hotkey("ctrl", "w")

    return True