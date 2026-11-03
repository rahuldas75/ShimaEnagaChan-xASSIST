# ⚡ X Intent Autopilot

A Windows desktop application for generating engaging X (formerly Twitter) post drafts with **Groq-powered LLMs** and opening them in X through its native Web Intent interface.

> **Important:** This project uses browser and keyboard automation to assist with publishing. Review every post before it is published, and use the tool responsibly.

---

## ✨ Features

- **No X Developer API key required** — Uses X's Web Intent URL to prepare a post.
- **AI-powered drafting** — Generates concise post drafts with Groq.
- **Desktop interface** — A native desktop window powered by `pywebview`.
- **Browser-assisted publishing** — Opens your default browser and uses desktop automation to interact with the posting flow.
- **Configurable scheduling** — Set posting intervals with randomized delays (“jitter”).
- **Windows-focused workflow** — Designed for Windows 10/11 desktop environments.

## 🧰 Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python |
| LLM provider | Groq API |
| Desktop UI | `pywebview` |
| Browser / keyboard automation | `pygetwindow`, `pyautogui` |
| Post composer | X Web Intent |

## 🔄 How It Works

```text
Persona / topic / instructions
              │
              ▼
        Groq API (LLM)
              │
              ▼
       Generated post draft
              │
              ▼
       X Web Intent composer
       https://x.com/intent/post
              │
              ▼
       Desktop automation
       ├── Opens the default browser
       ├── Attempts to focus the browser window
       └── Sends a keyboard shortcut
              │
              ▼
       User reviews and publishes
```

The exact behavior depends on your browser, desktop focus, and application configuration. Keyboard automation can be unreliable if another window receives focus.

---

## 🚀 Getting Started

### Prerequisites

- Windows 10 or Windows 11
- Python **3.10 or later**
- A supported desktop browser installed
- An X account signed in to `x.com`
- A Groq API key: [Groq Console](https://console.groq.com/)

### 1. Clone the repository

Replace the placeholder URL below with the repository's actual URL:

```powershell
git clone https://github.com/your-username/x-intent-autopilot.git
cd x-intent-autopilot
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, you can use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Add your Groq API key to `.env`:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Keep `.env` private. **Do not commit API keys or other secrets to version control.**

### 5. Launch the application

```powershell
python main.py
```

---

## 🖥️ Usage

1. Launch the application.
2. Enter or configure the persona, topic, and prompt details.
3. Generate a draft using Groq.
4. Review and edit the generated content.
5. Start the dispatch workflow to open the post in X.
6. Confirm the correct browser window and account are active.
7. **Review the post and publish it yourself**, unless your configured workflow explicitly performs that action.

### Tips for reliable browser automation

- Sign in to X in your default browser before starting.
- Avoid using the mouse or keyboard while the automation sequence is running.
- Keep the browser visible and allow it to receive focus.
- Test the workflow with a draft before enabling any scheduled activity.
- Do not use high-frequency or repetitive posting patterns.

---

## 📦 Build a Windows executable

You can package the application with PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```

The executable is typically created at:

```text
dist\main.exe
```

> **Packaging note:** Depending on how the project loads its UI assets and configuration files, additional PyInstaller options or bundled files may be required. Test the executable on a clean environment before distributing it.

---

## 🔐 Security & Privacy

- Store your Groq API key in `.env` or another secure local configuration mechanism.
- Ensure `.env` is listed in `.gitignore`.
- Never publish API keys, access tokens, or personal data in issues, screenshots, or commits.
- Generated content may be sent to Groq for processing; avoid including confidential information in prompts.
- Browser automation operates within your local desktop session. Keep your device and browser session secure.

## ⚠️ Limitations & Responsible Use

- This project relies on UI and keyboard automation, which may fail due to focus changes, browser updates, display scaling, or timing differences.
- X Web Intent prepares content in X; it is not an official X Developer API integration.
- Scheduling and randomized delays do not guarantee successful delivery or compliance.
- You are responsible for reviewing content and complying with [X's Terms of Service](https://x.com/en/tos) and [Automation Rules](https://help.x.com/en/rules-and-policies/x-automation).

---

## 🛠️ Troubleshooting

| Issue | Suggested check |
| --- | --- |
| `GROQ_API_KEY` not detected | Confirm `.env` exists, the key name is exact, and the app loads environment variables. |
| Dependency installation fails | Verify Python version and run `python -m pip install --upgrade pip`. |
| Browser does not open | Check your Windows default browser settings. |
| Automation targets the wrong window | Close unrelated windows and ensure the browser is visible before dispatch. |
| Executable fails to launch | Run `python main.py` first to identify errors; check PyInstaller asset and hidden-import requirements. |

If an issue persists, open a GitHub issue with the error message and steps to reproduce. **Do not include secrets or API keys.**

---

## 📄 License

This project is distributed under the **MIT License**. See [`LICENSE`](LICENSE) for the full license text.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com/) for LLM inference.
- [X Web Intent](https://x.com/intent/post) for the post-composer interface.
- The open-source Python ecosystem powering the desktop application.
