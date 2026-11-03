# \# ⚡ X Intent Autopilot

# 

# An autonomous Windows 11 desktop studio that drafts high-signal, engaging posts using \*\*Groq LLM\*\* and dispatches them directly to X (Twitter) via \*\*OS Web Intent shortcuts\*\*—completely bypassing the need for paid or restricted X Developer API keys.

# 

# \---

# 

# \## ✨ Features

# 

# \- \*\*No X API Keys Needed:\*\* Avoids developer tier paywalls, app approvals, and rate limits by utilizing X's native Web Intent endpoint (`https://x.com/intent/post`).

# \- \*\*OS Shortcut Dispatcher:\*\* Automatically focuses your default web browser and triggers keyboard shortcuts (`Ctrl + Enter`) via `pyautogui` and `pygetwindow`.

# \- \*\*Ultra-Fast LLM Generation:\*\* Integrates Groq (`llama-3.3-70b-versatile`) for immediate, authentic drafting.

# \- \*\*Modern GUI:\*\* Built with `pywebview` for an elegant, responsive native desktop wrapper.

# \- \*\*Custom Post Scheduling \& Jitter:\*\* Configurable posting intervals with randomized delays to maintain natural activity patterns.

# 

# \---

# 

# \## 🛠️ How It Works



\[ Persona / Topic Inputs ]

↓

\[ Groq API (LLM) ] ── (Generates concise draft)

↓

\[ Web Intent URL ] ── (https://x.com/intent/post?text=...)

↓

\[ OS Shortcut Dispatcher ]

├── Opens your default browser (pre-authenticated)

├── Focuses the browser window via pygetwindow

└── Simulates OS keystroke (Ctrl + Enter) to publish

\---



\## 🚀 Quick Start (Windows 11)



\### 1. Prerequisites

\- \*\*Windows 10 / 11\*\*

\- \*\*Python 3.10+\*\* (Ensure \*\*"Add Python to PATH"\*\* was checked during installation)

\- An active browser (Chrome, Edge, Brave, etc.) logged into your X account.



\### 2. Clone the Repository

```cmd

git clone \[https://github.com/your-username/x-intent-autopilot.git](https://github.com/your-username/x-intent-autopilot.git)

cd x-intent-autopilot



3\. Create \& Activate Virtual Environment

DOS

python -m venv venv

venv\\Scripts\\activate

4\. Install Dependencies

DOS

pip install -r requirements.txt

5\. Setup Environment Variables

Copy .env.example to .env:



DOS

copy .env.example .env

Open .env and add your Groq API Key (obtain a free key from Groq Console):



Code snippet

GROQ\_API\_KEY=gsk\_your\_actual\_key\_here

🖥️ Running the Application

Launch the desktop UI:



DOS

python main.py

Tips for Smooth Dispatching:

Ensure your default browser is already logged in to x.com.



During the shortcut dispatch sequence, avoid interacting with the mouse or keyboard for \~2 seconds while the window gains focus and submits the post.



⚙️ Compiling to a Standalone Executable (.exe)

To turn the script into a single-file executable for Windows:



DOS

pip install pyinstaller

pyinstaller --noconsole --onefile main.py

The compiled application will be generated in dist/main.exe.



⚠️ Disclaimer

This tool uses desktop automation to assist with posting content. Always comply with X's Automation Rules and Terms of Service. Avoid high-frequency spam or aggressive automated behavior that could result in account penalties.



📄 License

Distributed under the MIT License. See LICENSE for more information.

