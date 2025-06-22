

# 📒 KisNapló Session Tool

> ⚠️ **UNOFFICIAL CLI TOOL**
> This is a third-party tool for automating interactions with the *Lépésről Lépésre* ("Step by Step") interface of the **Karinthy KisNapló** system.
> It is **not affiliated with, endorsed by, or supported by** the official KisNapló devs, the school, or anyone else respectable.

A Python automation tool for interacting with the [KisNapló Karinthy interface](https://kisnaplo.karinthy.hu), supporting session management, name updates, and profile picture uploads via the KSNPLSID token system.

> ⚠️ For educational and personal automation use only. Don’t be a skiddie. You’re better than that.



Sure, Benedek. Here's a **really good README** for your KisNapló session automation project – clean, structured, and dev-friendly, like something that’d make even a sleep-deprived sysadmin nod in approval.

---

# 📒 KisNapló Session Tool

A Python automation tool for interacting with the [KisNapló Karinthy interface](https://kisnaplo.karinthy.hu), supporting session management, name updates, and profile picture uploads via the KSNPLSID token system.

> ⚠️ This is for educational and personal automation use only. Don’t be a skiddie. You’re better than that.

---

## 🧠 Features

* 🟢 Session validation & auto-renewal.
* 🧑‍🎓 Change your display name programmatically.
* 🖼 Upload profile pictures easily.
* 🧾 Logs all activities with unique log files.

---

## 📁 Project Structure

```
.
├── main.py           # CLI interface
├── session.py        # Session management and login logic
├── tools.py          # Utility functions (update name, upload picture)
├── .env              # (Optional) Save your password here
└── logs/             # Auto-generated log files
```

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/b31556/karinthy_lep_lepre_unofficial_cli_tool.git
cd karinthy_lep_lepre_unofficial_cli_tool
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file (optional)

```
aaaa-bbbb-cccc
```

Or you’ll be prompted to enter it when you run the script.

---

## 🚀 Usage

### Run the tool

```bash
python main.py
```

### Available Commands

| Command          | Alias | Description                          |
| ---------------- | ----- | ------------------------------------ |
| `update_name`    | `un`  | Change your profile display name     |
| `upload_picture` | `up`  | Upload a new profile picture         |
| `test`           | `t`   | Validate session; auto-renew if dead |
| `Ctrl + C`       | —     | Quit                                 |

---

## 🔒 Password Format

Your login password must follow this format:

```
aaaa-bbbb-cccc
```

Each block is 4 characters long. The system strips dashes, whitespace, and formats it into a list like:

```python
["aaaa", "bbbb", "cccc"]
```

---

## 🧪 Session Flow

1. Sends a request to the login form.
2. Extracts and fills inputs using your 3-part password.
3. Extracts the `KSNPLSID` from the redirect URL.
4. Creates a `Session` object and logs all activity.

---

## 📂 Logging

* Logs are saved in the `logs/` directory as `1.log`, `2.log`, etc.
* Each session has a unique log that captures every interaction.
* Automatically saves logs if login or session test fails.

---

## ⚠️ Error Handling

* ❌ If login fails, you get a saved log and a traceback.
* ❌ If the picture path is invalid, it raises `FileNotFoundError`.
* 🔄 If session is invalid, it will try to renew it automatically.

---

## ✍️ Sample Session

```bash
$ python main.py
>>> Enter your password (4 x 3) eg aaaa-bbbb-cccc > test-test-test
>>> Starting session...
>>> Session created successfully!
> un
>>> Enter new name: csatlord420
>>> Name updated to: csatlord420
> up
>>> Enter picture path: ./pfp.jpg
>>> Picture uploaded from: ./pfp.jpg
> t
>>> Session is active and valid.
```

---

## 🤓 Developer Notes

* Code is modular. You can import `Session` and use it in your own script.
* `tools.py` contains standalone utilities you can add if you are willing to.
* BeautifulSoup is used to parse forms and inputs.

---


## 📜 License

MIT License – do what you want, but don’t be an ass.
