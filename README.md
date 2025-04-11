
---

<h1 align="center">Hipin Bot</h1>

<p align="center">
<strong>Boost your productivity with Hipin Bot – your friendly automation tool that handles key tasks with ease!</strong>
</p>

<p align="center">
<a href="https://github.com/livexords-nw/hipin-bot/actions">
<img src="https://img.shields.io/github/actions/workflow/status/livexords-nw/hipin-bot/ci.yml?branch=main" alt="Build Status" />
</a>
<a href="https://github.com/livexords-nw/hipin-bot/releases">
<img src="https://img.shields.io/github/v/release/livexords-nw/hipin-bot" alt="Latest Release" />
</a>
<a href="https://github.com/livexords-nw/hipin-bot/blob/main/LICENSE">
<img src="https://img.shields.io/github/license/livexords-nw/hipin-bot" alt="License" />
</a>
<a href="https://t.me/livexordsscript">
<img src="https://img.shields.io/badge/Telegram-Join%20Group-2CA5E0?logo=telegram&style=flat" alt="Telegram Group" />
</a>
</p>

---

## 🚀 About the Bot

Hipin Bot is your automation buddy designed to simplify daily operations. This bot takes over repetitive tasks so you can focus on what really matters. With Hipin Bot, you get:

- **Daily Reward Check & Claim 🎁:**  
  Automatically check and claim your daily rewards.
- **Automatically Solving Tasks 🤖:**  
  Handle routine tasks automatically, reducing manual intervention.
- **Automatic Farming for Abundant Harvest 🌾:**  
  Collect resources through automated farming processes.
- **Automatic Level Up System 📈:**
  The bot automatically checks your level-up requirements and upgrades your model when the criteria are met, ensuring continuous progress without manual effort.
- **Multi Account Support 👥:**  
  Manage multiple accounts effortlessly with built-in multi account support.
- **Thread System 🧵:**  
  Run tasks concurrently with configurable threading options to improve overall performance and speed.
- **Configurable Delays ⏱️:**  
  Fine-tune delays between account switches and loop iterations to match your specific workflow needs.
- **Support Proxy 🔌:**  
  Use HTTP/HTTPS proxies to enhance your multi-account setups.

Hipin Bot is built with flexibility and efficiency in mind – it's here to help you automate your operations and boost your productivity!

---

## 🌟 Version Updates

**Current Version: v1.0.1**

### v1.0.1 - Latest Update

1. **Added Auto Level Up System:**  
   The bot now automatically checks your level-up requirements and upgrades your model when the criteria are met.

---

## 📝 Register

Before you start using Hipin Bot, make sure to register your account.  
Click the link below to get started:

[🔗 Register for Hipin Bot](https://t.me/hi_PIN_bot/app?startapp=pAuthDl)

---

## ⚙️ Configuration

### Main Bot Configuration (`config.json`)

```json
{
  "farming": true,
  "task": true,
  "daily": true,
  "thread": 1,
  "proxy": false,
  "delay_account_switch": 10,
  "delay_loop": 3000
}
```

| **Setting**            | **Description**                                    | **Default Value** |
| ---------------------- | -------------------------------------------------- | ----------------- |
| `farming`              | Automate farming sessions and reward claims        | `true`            |
| `task`                 | Automate task execution and reward claims          | `true`            |
| `daily`                | Automate daily check-in and claim rewards          | `true`            |
| `thread`               | Number of concurrent threads (accounts) to process | `1`               |
| `proxy`                | Enable/Disable proxy usage                         | `false`           |
| `delay_account_switch` | Delay before switching accounts (in seconds)       | `10`              |
| `delay_loop`           | Delay before restarting the bot loop (in seconds)  | `3000`            |

---

## 📅 Requirements

- **Minimum Python Version:** `Python 3.9+`
- **Required Libraries:**
  - colorama
  - requests
  - fake-useragent
  - brotli
  - chardet
  - urllib3

These are installed automatically when running:

```bash
pip install -r requirements.txt
```

---

## 📅 Installation Steps

### Main Bot Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/livexords-nw/hipin-bot.git
   ```

2. **Navigate to the Project Folder**

   ```bash
   cd hipin-bot
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Your Query**

   Create a file named `query.txt` and add your query data.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   _Only HTTP and HTTPS proxies are supported._

6. **Run Bot**

   ```bash
   python main.py
   ```

---

### 🔹 Want Free Proxies?

You can obtain free proxies from [Webshare.io](https://www.webshare.io/).

---

### 📂 Project Structure

```
hipin-bot/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI workflow for automated checks/deploys
├── config.json                 # Main configuration file for the bot
├── query.txt                   # Contains query data to be processed
├── proxy.txt                   # (Optional) Proxy list (HTTP/HTTPS) to use for multi-account support
├── main.py                     # Main Python script (entry point of the bot)
├── requirements.txt            # Python dependencies required to run the bot
├── LICENSE                     # License for the project
└── README.md                   # Documentation and feature list 
```

---

## 🛠️ Contributing

This project is developed by **Livexords**.  
If you have ideas, questions, or want to contribute, please join our Telegram group for discussions and updates.  
For contribution guidelines, please consider:

- **Code Style:** Follow standard Python coding conventions.
- **Pull Requests:** Test your changes before submitting a PR.
- **Feature Requests & Bugs:** Report and discuss via our Telegram group.

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/badge/Join-Telegram%20Group-2CA5E0?logo=telegram&style=for-the-badge" height="25" alt="Telegram Group" />
  </a>
</div>

---

## 📖 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 🔍 Usage Example

After installation and configuration, simply run:

```bash
python main.py
```

You should see output indicating the bot has started its operations. For further instructions or troubleshooting, please check our Telegram group or open an issue in the repository.

---

## 📣 Community & Support

For support, updates, and feature requests, join our Telegram group.  
This is the central hub for all discussions related to Hipin Bot, including roadmap ideas and bug fixes.

---
