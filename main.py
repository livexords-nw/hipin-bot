from datetime import datetime
import requests
from urllib.parse import parse_qs, urlsplit
import json
import time
from colorama import init, Fore, Style
import random
from fake_useragent import UserAgent
import asyncio


class hipin:
    BASE_URL = "https://prod-api.pinai.tech/"
    HEADERS = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "prod-api.pinai.tech",
        "Origin": "https://web.pinai.tech",
        "Referer": "https://web.pinai.tech/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
        "lang": "en-GB",
        "sec-ch-ua": '"Microsoft Edge";v="134", "Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge WebView2";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 HiPin Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔐 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(f"📋 Using token: {token[:10]}... (truncated)", Fore.CYAN)

        # Request login ke API baru
        login_url = f"{self.BASE_URL}passport/login/telegram"
        payload = {"init_data": token}
        self.log("📡 Sending login request...", Fore.CYAN)
        try:
            response = requests.post(login_url, headers=self.HEADERS, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to send login request: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {response.text}", Fore.RED)
            except Exception:
                pass
            return

        login_data = response.json()
        self.token = login_data.get("access_token")
        if not self.token:
            self.log("❌ Login failed: access_token not found.", Fore.RED)
            return
        self.log("✅ Login successful!", Fore.GREEN)

        # Request ke API home
        home_url = f"{self.BASE_URL}home"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        self.log("📡 Fetching home data...", Fore.CYAN)
        try:
            home_response = requests.get(home_url, headers=headers)
            home_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch home data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {home_response.text}", Fore.RED)
            except Exception:
                pass
            return

        home_data = home_response.json()

        # Menampilkan data penting secara terpisah
        self.log("⭐ Home Data ⭐", Fore.CYAN)
        self.log(f"🔹 Pin Points   : {home_data.get('pin_points', 'N/A')}", Fore.CYAN)
        self.log(f"🔹 Data Power   : {home_data.get('data_power', 'N/A')}", Fore.CYAN)

        current_model = home_data.get("current_model", {})
        if current_model:
            self.log("🚀 Current Model:", Fore.CYAN)
            self.log(
                f"   • Name         : {current_model.get('name', 'N/A')}", Fore.CYAN
            )
            self.log(
                f"   • Current Level: {current_model.get('current_level', 'N/A')}",
                Fore.CYAN,
            )
            self.log(
                f"   • Total Level  : {current_model.get('total_level', 'N/A')}",
                Fore.CYAN,
            )

        user_info = home_data.get("user_info", {})
        if user_info:
            self.log("👤 User Info:", Fore.CYAN)
            self.log(f"   • Name   : {user_info.get('name', 'N/A')}", Fore.CYAN)
            self.log(f"   • Picture: {user_info.get('picture', 'N/A')}", Fore.CYAN)

    def farming(self) -> None:
        # Request the home API to get the initial data
        home_url = f"{self.BASE_URL}home"
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}
        self.log("📡 Fetching home data...", Fore.CYAN)
        try:
            home_response = requests.get(home_url, headers=headers)
            home_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch home data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {home_response.text}", Fore.RED)
            except Exception:
                pass
            return

        home_data = home_response.json()

        # Extract important data from the home data
        pin_points_str = home_data.get("pin_points", "0")
        next_level = home_data.get("current_model", {}).get("next_level")
        next_level_need_point_str = home_data.get("current_model", {}).get(
            "next_level_need_point", "0"
        )
        next_level_add_power = home_data.get("current_model", {}).get(
            "next_level_add_power"
        )

        self.log(f"🔹 Pin Points             : {pin_points_str}", Fore.CYAN)
        self.log(f"🔹 Next Level             : {next_level}", Fore.CYAN)
        self.log(f"🔹 Next Level Need Points : {next_level_need_point_str}", Fore.CYAN)
        self.log(f"🔹 Next Level Add Power   : {next_level_add_power}", Fore.CYAN)

        # Function to parse abbreviated point values, e.g., "580.8K" becomes 580800 and "1.2M" becomes 1200000
        def parse_point(point_str: str) -> float:
            point_str = point_str.replace(",", "").strip()
            if not point_str:
                return 0
            multiplier = 1
            if point_str[-1].upper() == "K":
                multiplier = 1000
                num_str = point_str[:-1]
            elif point_str[-1].upper() == "M":
                multiplier = 1000000
                num_str = point_str[:-1]
            else:
                num_str = point_str
            try:
                return float(num_str) * multiplier
            except ValueError:
                return 0

        current_points = parse_point(pin_points_str)
        required_points = parse_point(next_level_need_point_str)

        # Check if pin_points are sufficient to level up
        if current_points >= required_points:
            self.log("✅ Level up requirements met. Upgrading model...", Fore.GREEN)
            upgrade_url = f"{self.BASE_URL}model/upgrade"
            payload = {}
            try:
                upgrade_response = requests.post(
                    upgrade_url, headers=headers, json=payload
                )
                upgrade_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to upgrade model: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response: {upgrade_response.text}", Fore.RED)
                except Exception:
                    pass
                return

            upgrade_data = upgrade_response.json()
            self.log("✅ Model upgrade successful!", Fore.GREEN)
            self.log("⭐ Upgrade Result ⭐", Fore.CYAN)
            self.log(f"🔹 Current Level: {upgrade_data.get('level', 'N/A')}", Fore.CYAN)
            self.log(f"🔹 Model ID     : {upgrade_data.get('model', 'N/A')}", Fore.CYAN)
        else:
            self.log("❌ Level up requirements not met.", Fore.YELLOW)

        # Optional: Collect coins request
        total_coins = home_data.get("total_coins", [])
        if total_coins:
            coin_info = total_coins[0]
            coin_type = coin_info.get("type", "Telegram")
            coin_count = coin_info.get("count", 0)
            self.log(
                f"🔹 Retrieved coin info: {coin_type} with count: {coin_count}",
                Fore.CYAN,
            )

            collect_url = f"{self.BASE_URL}home/collect"
            payload = [{"type": coin_type, "count": coin_count}]
            self.log(f"📡 Sending collect request with payload: {payload}", Fore.CYAN)
            try:
                collect_response = requests.post(
                    collect_url, headers=headers, json=payload
                )
                collect_response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.log(f"❌ Failed to send collect request: {e}", Fore.RED)
                try:
                    self.log(f"📄 Response: {collect_response.text}", Fore.RED)
                except Exception:
                    pass
                return

            collect_data = collect_response.json()
            self.log("✅ Farming collect successful!", Fore.GREEN)
            self.log("⭐ Farming Result ⭐", Fore.CYAN)
            self.log(
                f"🔹 Pin Points : {collect_data.get('pin_points', 'N/A')}", Fore.CYAN
            )
            self.log(
                f"🔹 Data Power : {collect_data.get('data_power', 'N/A')}", Fore.CYAN
            )

            coins_after = collect_data.get("coins", [])
            if coins_after:
                coin_after_info = coins_after[0]
                self.log(
                    f"🔹 Remaining {coin_after_info.get('type', 'Telegram')} coins: {coin_after_info.get('count', 'N/A')}",
                    Fore.CYAN,
                )

    def daily(self) -> None:
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # Langkah 1: Cek status daily checkin dari API home
        home_url = f"{self.BASE_URL}home"
        self.log("📡 Fetching home data for daily checkin...", Fore.CYAN)
        try:
            home_response = requests.get(home_url, headers=headers)
            home_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch home data: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {home_response.text}", Fore.RED)
            except Exception:
                pass
            return

        home_data = home_response.json()
        is_today_checkin = home_data.get("is_today_checkin", False)
        if is_today_checkin:
            self.log("✅ Daily checkin already claimed.", Fore.GREEN)
            return
        else:
            self.log("⏳ Daily checkin not yet claimed. Proceeding...", Fore.CYAN)

        # Langkah 2: Complete task dengan ID 1001
        complete_url = f"{self.BASE_URL}task/1001/v1/complete"
        self.log("📡 Sending complete task request...", Fore.CYAN)
        try:
            complete_response = requests.post(complete_url, headers=headers, json={})
            complete_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to complete task 1001: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {complete_response.text}", Fore.RED)
            except Exception:
                pass
            return

        complete_result = complete_response.json()
        if complete_result.get("status") != "success":
            self.log("❌ Task completion unsuccessful.", Fore.RED)
            return
        self.log("✅ Task 1001 completed successfully.", Fore.GREEN)

        # Langkah 3: Claim daily checkin dengan request ke checkin_data
        checkin_url = f"{self.BASE_URL}task/checkin_data"
        self.log("📡 Claiming daily checkin...", Fore.CYAN)
        try:
            checkin_response = requests.get(checkin_url, headers=headers)
            checkin_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to claim daily checkin: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {checkin_response.text}", Fore.RED)
            except Exception:
                pass
            return

        checkin_data = checkin_response.json()
        self.log("✅ Daily checkin claimed!", Fore.GREEN)
        self.log(f"🔹 Pin Points: {checkin_data.get('pin_points', 'N/A')}", Fore.CYAN)

        tasks = checkin_data.get("tasks", [])
        if tasks:
            task = tasks[0]  # Asumsikan task pertama adalah daily checkin
            self.log("📝 Daily Checkin Task:", Fore.CYAN)
            self.log(
                f"    • Task Name      : {task.get('task_name', 'N/A')}", Fore.CYAN
            )
            self.log(
                f"    • Reward Points  : {task.get('reward_points', 'N/A')}", Fore.CYAN
            )
            checkin_detail = task.get("checkin_detail", {})
            consecutive_days = checkin_detail.get("consecutive_days", "N/A")
            self.log(f"    • Consecutive Days: {consecutive_days}", Fore.CYAN)
        else:
            self.log("❌ No daily task info found.", Fore.RED)

    def task(self) -> None:
        headers = {**self.HEADERS, "authorization": f"Bearer {self.token}"}

        # Ambil daftar task
        task_list_url = f"{self.BASE_URL}task/v4/list"
        self.log("📡 Fetching task list...", Fore.CYAN)
        try:
            tasks_response = requests.get(task_list_url, headers=headers)
            tasks_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Failed to fetch tasks: {e}", Fore.RED)
            try:
                self.log(f"📄 Response: {tasks_response.text}", Fore.RED)
            except Exception:
                pass
            return

        tasks_data = tasks_response.json()
        tasks = tasks_data.get("tasks", [])
        if not tasks:
            self.log("❌ No tasks found.", Fore.RED)
            return

        # Iterasi setiap task dan cek statusnya
        for task in tasks:
            task_id = task.get("task_id")
            task_name = task.get("task_name", "N/A")
            is_complete = task.get("is_complete", False)
            need_claim = task.get("need_claim", False)
            can_claim = task.get("can_claim", False)

            self.log(f"📝 Task: {task_name} (ID: {task_id})", Fore.CYAN)
            self.log(
                f"    - is_complete: {is_complete}, need_claim: {need_claim}, can_claim: {can_claim}",
                Fore.CYAN,
            )

            # Jika task perlu di-claim (need_claim True) dan masih bisa di-claim (can_claim masih False)
            if need_claim and not can_claim:
                complete_url = f"{self.BASE_URL}task/{task_id}/v1/complete"
                self.log(f"📡 Attempting to complete task {task_id}...", Fore.CYAN)
                try:
                    complete_response = requests.post(
                        complete_url, headers=headers, json={}
                    )
                    complete_response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    self.log(f"❌ Failed to complete task {task_id}: {e}", Fore.RED)
                    try:
                        self.log(f"📄 Response: {complete_response.text}", Fore.RED)
                    except Exception:
                        pass
                    continue

                result = complete_response.json()
                if result.get("status") == "success":
                    self.log(
                        f"✅ Task {task_id} ({task_name}) completed successfully.",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"❌ Task {task_id} ({task_name}) completion failed.", Fore.RED
                    )
            else:
                self.log(
                    f"ℹ️ Task {task_id} ({task_name}) already complete or not eligible for claiming.",
                    Fore.YELLOW,
                )

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        import random

        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


async def process_account(account, original_index, account_label, hip, config):
    # Set a random fake User-Agent for this account
    ua = UserAgent()
    hip.HEADERS["User-Agent"] = ua.random

    display_account = account[:10] + "..." if len(account) > 10 else account
    hip.log(f"👤 Processing {account_label}: {display_account}", Fore.YELLOW)

    # Override proxy if enabled
    if config.get("proxy", False):
        hip.override_requests()
    else:
        hip.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

    # Login (blocking call executed in a thread) using the account's index
    await asyncio.to_thread(hip.login, original_index)

    hip.log("🛠️ Starting task execution...", Fore.CYAN)
    tasks_config = {
        "daily": "Daily Reward Check & Claim 🎁",
        "task": "Automatically solving tasks 🤖",
        "farming": "Automatic farming for abundant harvest 🌾",
    }

    for task_key, task_name in tasks_config.items():
        task_status = config.get(task_key, False)
        color = Fore.YELLOW if task_status else Fore.RED
        hip.log(
            f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
            color,
        )
        if task_status:
            hip.log(f"🔄 Executing {task_name}...", Fore.CYAN)
            await asyncio.to_thread(getattr(hip, task_key))

    delay_switch = config.get("delay_account_switch", 10)
    hip.log(
        f"➡️ Finished processing {account_label}. Waiting {Fore.WHITE}{delay_switch}{Fore.CYAN} seconds before next account.",
        Fore.CYAN,
    )
    await asyncio.sleep(delay_switch)


async def worker(worker_id, hip, config, queue):
    """
    Each worker takes one account from the queue and processes it sequentially.
    A worker will not take a new account until the current one is finished.
    """
    while True:
        try:
            original_index, account = queue.get_nowait()
        except asyncio.QueueEmpty:
            break
        account_label = f"Worker-{worker_id} Account-{original_index+1}"
        await process_account(account, original_index, account_label, hip, config)
        queue.task_done()
    hip.log(f"Worker-{worker_id} finished processing all assigned accounts.", Fore.CYAN)


async def main():
    hip = hipin()
    config = hip.load_config()
    all_accounts = hip.query_list
    num_workers = config.get("thread", 1)  # Number of concurrent workers (threads)

    hip.log(
        "🎉 [LIVEXORDS] === Welcome to Hipin Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    hip.log(f"📂 Loaded {len(all_accounts)} accounts from query list.", Fore.YELLOW)

    if config.get("proxy", False):
        proxies = hip.load_proxies()

    while True:
        # Create a new asyncio Queue and add all accounts (with their original index)
        queue = asyncio.Queue()
        for idx, account in enumerate(all_accounts):
            queue.put_nowait((idx, account))

        # Create worker tasks according to the number of threads specified
        workers = [
            asyncio.create_task(worker(i + 1, hip, config, queue))
            for i in range(num_workers)
        ]

        # Wait until all accounts in the queue are processed
        await queue.join()

        # Cancel workers to avoid overlapping in the next loop
        for w in workers:
            w.cancel()

        hip.log("🔁 All accounts processed. Restarting loop.", Fore.CYAN)
        delay_loop = config.get("delay_loop", 30)
        hip.log(
            f"⏳ Sleeping for {Fore.WHITE}{delay_loop}{Fore.CYAN} seconds before restarting.",
            Fore.CYAN,
        )
        await asyncio.sleep(delay_loop)


if __name__ == "__main__":
    asyncio.run(main())
