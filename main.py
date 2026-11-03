import os
import sys
import time
import json
import re
import webbrowser
import webview
from dotenv import load_dotenv, set_key
from groq import Groq

from dispatcher import dispatch_post

GITHUB_URL = "https://github.com/rahuldas75/ShimaEnagaChan-xASSIST"
WEBSITE_URL = "https://rahuldas75.github.io/"
EXTERNAL_LINKS = {
    "github": GITHUB_URL,
    "website": WEBSITE_URL,
}

INITIAL_WIDTH = 920
INITIAL_HEIGHT = 620
MIN_WIDTH = 840
MIN_HEIGHT = 560
MAX_POST_LENGTH = 280


def fit_complete_post(text: str) -> str:
    """Keep the final complete sentence that fits the platform limit."""
    if len(text) <= MAX_POST_LENGTH:
        return text

    limited = text[:MAX_POST_LENGTH]
    sentence_ends = list(re.finditer(r"[.!?](?:\s|$)", limited))
    if sentence_ends:
        return limited[:sentence_ends[-1].end()].strip()

    word_boundary = limited.rfind(" ")
    if word_boundary > 0:
        return limited[:word_boundary].rstrip(" .,;:-") + "."
    return limited.rstrip(" .,;:-") + "."


def get_app_dir():
    """Resolve the directory used for files created by the application."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

def get_resource_dir():
    """Resolve the directory containing bundled application resources."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_app_dir()
RESOURCE_DIR = get_resource_dir()
ENV_FILE = os.path.join(BASE_DIR, ".env")

try:
    os.chdir(BASE_DIR)
except Exception:
    pass

load_dotenv(ENV_FILE)


class AppAPI:
    def __init__(self):
        self._window = None

    def set_window(self, win):
        self._window = win

    def open_external_link(self, target: str):
        """Open a configured external link in the default browser."""
        url = EXTERNAL_LINKS.get(target)
        if not url:
            self.log(f"❌ Unknown external link: {target}")
            return False

        webbrowser.open(url)
        self.log(f"🌐 Opened {target.capitalize()} link in browser.")
        return True

    def _eval_js(self, script: str):
        if self._window:
            try:
                self._window.evaluate_js(script)
            except Exception as e:
                print(f"[Bridge Error] {e}", file=sys.stderr)

    def log(self, message: str):
        """Send a safely encoded log message to the webview."""
        timestamp = time.strftime("[%H:%M:%S]")
        formatted = f"{timestamp} {message}"
        self._eval_js(f"window.appendLog({json.dumps(formatted)});")

    def load_keys(self):
        return {
            "groq_api_key": os.getenv("GROQ_API_KEY", ""),
            "llm_model": os.getenv("LLM_MODEL", "gpt-oss-120b")
        }

    def save_keys(self, data: dict):
        try:
            if not os.path.exists(ENV_FILE):
                with open(ENV_FILE, "w", encoding="utf-8") as f:
                    f.write("")
            for key, val in data.items():
                env_key = str(key).upper().strip()
                val_str = str(val).strip()
                set_key(ENV_FILE, env_key, val_str)
                os.environ[env_key] = val_str
            self.log("✅ Credentials saved to .env")
            return True
        except Exception as e:
            self.log(f"❌ Failed to save credentials: {e}")
            return False

    def get_groq_client(self):
        try:
            groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
            return groq
        except Exception as e:
            self.log(f"⚠️ Auth Setup Error: {e}")
            return None

    def generate_content(self, focus_topic: str) -> str:
        groq = self.get_groq_client()
        if not groq:
            self.log("❌ Groq client missing or GROQ_API_KEY invalid.")
            return ""

        self.log(f"🧠 Asking Groq to formulate post on: '{focus_topic[:30]}...'")
        prompt = (
            f"Write a concise, high-signal post about: {focus_topic}.\n"
            f"Rules: Write a complete post between 180 and 240 characters, never over "
            f"{MAX_POST_LENGTH}. "
            "Never stop mid-sentence. Punchy, authentic, plain text only. "
            "No hashtags, no emojis, no quotes. Return only the post."
        )
        try:
            model_name = os.getenv("LLM_MODEL", "gpt-oss-120b")
            request = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 512
            }
            if "gpt-oss" in model_name.lower():
                request["reasoning_effort"] = "low"

            res = groq.chat.completions.create(**request)
            if not res.choices or not res.choices[0].message.content:
                finish_reason = res.choices[0].finish_reason if res.choices else "no choices"
                self.log(
                    f"❌ Groq returned no post content (finish reason: {finish_reason}). "
                    "Try another model if this continues."
                )
                return ""

            text = res.choices[0].message.content.strip().replace('"', '')
            if not text:
                self.log("❌ Groq returned an empty post.")
                return ""

            if len(text) > MAX_POST_LENGTH:
                retry_request = dict(request)
                retry_request["messages"] = [{
                    "role": "user",
                    "content": (
                        f"Rewrite this as one complete post between 180 and 240 characters, "
                        f"never over {MAX_POST_LENGTH} "
                        f"characters. Do not cut it off mid-sentence. Return only the post:\n{text}"
                    ),
                }]
                retry = groq.chat.completions.create(**retry_request)
                retry_content = retry.choices[0].message.content if retry.choices else None
                text = retry_content.strip().replace('"', '') if retry_content else ""
                if not text:
                    self.log("❌ Groq returned an empty rewritten post.")
                    return ""
                if len(text) > MAX_POST_LENGTH:
                    text = fit_complete_post(text)
                    self.log(f"⚠️ Rewritten post was shortened to its last complete sentence ({len(text)} chars).")

            self.log(f"✨ Post generated ({len(text)} chars)")
            self._eval_js(f"window.setGeneratedContent({json.dumps(text)});")
            return text
        except Exception as e:
            self.log(f"❌ Groq Error: {e}")
            return ""

    def generate_persona_focus(self) -> str:
        groq = self.get_groq_client()
        if not groq:
            self.log("❌ Groq client missing or GROQ_API_KEY invalid.")
            return ""

        prompt = (
            "Create one fresh instruction for an X post writer. Include a distinct persona, "
            "a specific topic focus, and a useful writing angle. Keep it concise, natural, "
            "and under 240 characters. Return only the instruction."
        )
        try:
            model_name = os.getenv("LLM_MODEL", "gpt-oss-120b")
            request = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9,
                "max_tokens": 256,
            }
            if "gpt-oss" in model_name.lower():
                request["reasoning_effort"] = "low"

            res = groq.chat.completions.create(**request)
            content = res.choices[0].message.content if res.choices else None
            text = content.strip() if content else ""
            if not text:
                self.log("❌ Groq returned no persona and focus.")
                return ""

            if len(text) > 280:
                text = text[:280].rsplit(" ", 1)[0].rstrip(" .,;:-")
            self.log("🎲 Persona and focus generated by Groq.")
            return text
        except Exception as e:
            self.log(f"❌ Groq Error while generating persona and focus: {e}")
            return ""

    def auto_dispatch_content(self, text: str) -> bool:
        """Open X in the browser and submit the post with the native shortcut."""
        if not text or not text.strip():
            self.log("⚠️ Content is empty. Nothing to dispatch.")
            return False

        self.log("🚀 Opening X for automated dispatch...")
        try:
            success = dispatch_post(text, auto_close=True)
        except Exception as e:
            self.log(f"❌ Dispatch Error: {e}")
            return False

        if success:
            self.log("🎉 Tweet submitted through automated browser dispatch.")
        else:
            self.log("❌ Automated dispatch did not complete.")
        return success

    def trigger_generate_only(self, topic: str):
        return self.generate_content(topic)

if __name__ == "__main__":
    api = AppAPI()

    ui_dir = os.path.join(RESOURCE_DIR, "ui")
    index_file = os.path.join(ui_dir, "index.html")
    icon_file = os.path.join(ui_dir, "assets", "shima-enaga-icon.ico")

    window = webview.create_window(
        title="ShimaEnagaChan - xASSIST",
        url=index_file,
        js_api=api,
        width=INITIAL_WIDTH,
        height=INITIAL_HEIGHT,
        min_size=(MIN_WIDTH, MIN_HEIGHT),
        background_color='#E0F2FE'
    )
    api.set_window(window)

    app_icon = icon_file if os.path.exists(icon_file) else None
    webview.start(http_server=True, debug=False, icon=app_icon)