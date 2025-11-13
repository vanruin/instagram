import uuid
import json
import hmac
import hashlib
import urllib.parse
import random
import time
import re
import requests
import httpx
import sys
import os
from rich.tree import Tree
from rich import print as sprint
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt, IntPrompt
import threading
from concurrent.futures import ThreadPoolExecutor

# Global variables
hitung = 0
success = 0
checkpoint = 0
login = {'Lib': 'req'}  # Default to requests
console = Console()

# Enhanced color codes for output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ORANGE = '\033[38;5;214m'
    PINK = '\033[38;5;205m'
    PURPLE = '\033[38;5;141m'

def print_logo():
    """Print enhanced Instagram logo with colors"""
    logo = f"""
{Colors.PINK}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║  ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗  ║
║  ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║  ║
║  ██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗██████╔╝███████║██╔████╔██║  ║
║  ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║  ║
║  ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║  ║
║  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ║
║                                                                ║
║                🚀 [bold cyan]INSTAGRAM TOOL SUITE[/bold cyan] 🚀                 ║
║              [bold yellow]Account Extractor + Auto Liker[/bold yellow]            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
{Colors.RESET}
    """
    console.print(Panel(logo, style="bold magenta", padding=1))

def print_separator():
    """Print a decorative separator line"""
    console.print(f"[cyan]{'═' * 80}[/cyan]")

def print_header(text):
    """Print a formatted header"""
    print_separator()
    console.print(f"\n[bold magenta]✨ {text} ✨[/bold magenta]\n")
    print_separator()

def print_success(text):
    """Print success message"""
    console.print(f"[bold green]✅ {text}[/bold green]")

def print_error(text):
    """Print error message"""
    console.print(f"[bold red]❌ {text}[/bold red]")

def print_warning(text):
    """Print warning message"""
    console.print(f"[bold yellow]⚠️ {text}[/bold yellow]")

def print_info(text):
    """Print info message"""
    console.print(f"[bold blue]📢 {text}[/bold blue]")

def print_processing(text):
    """Print processing message"""
    console.print(f"[bold cyan]🔄 {text}[/bold cyan]")

def get_android_user_agent():
    android_versions = [
        "10.0.0.11.119", "10.3.2.11.119", "10.8.1.11.119", "10.12.1.11.119",
        "10.16.0.11.119", "10.18.0.11.119", "10.20.0.11.119", "10.21.1.11.119"
    ]
    devices = ["SM-G973F", "SM-G975F", "SM-G970F", "SM-A505F", "Pixel 6", "Pixel 7"]
    return f"Instagram {random.choice(android_versions)} Android ({random.choice(['10','11','12'])}/{random.choice(['10','11','12'])}.0; 480dpi; 1080x2280; samsung; {random.choice(devices)}; en_US)"

def convert_cookie(item):
    try:
        sesid = 'sessionid=' + re.findall('sessionid=([^;]+)', str(item))[0]
        ds_id = 'ds_user_id=' + re.findall('ds_user_id=([^;]+)', str(item))[0]
        csrft = 'csrftoken=' + re.findall('csrftoken=([^;]+)', str(item))[0]
        return f'{csrft}; {ds_id}; {sesid}; ig_nrcb=1; dpr=2;'
    except Exception as e:
        print_error(f"Cookie conversion failed: {e}")
        return 'cookies tidak di temukan, error saat convert'

def info(username):
    return "N/A", "N/A"

def www_insta(username=None, password=None, method="android"):
    global hitung, success, checkpoint, login
    if username is None or password is None:
        username = Prompt.ask("📧 Enter username", default="")
        password = Prompt.ask("🔑 Enter password", password=True)
        if not username or not password:
            return False, None, None

    user_agent = get_android_user_agent()

    print_processing("Using ANDROID method...")

    try:
        ses = requests.Session()
        curl = ses.get('https://www.instagram.com/api/v1/si/fetch_headers/?challenge_type=signup&guid=' + str(uuid.uuid4()))
        payload = json.dumps({
            'phone_id': str(uuid.uuid4()),
            '_csrftoken': curl.cookies.get('csrftoken', 'TeWMHnpFe4nja'),
            'username': username,
            'guid': str(uuid.uuid4()),
            'device_id': 'android-' + str(uuid.uuid4()),
            'password': password,
            'login_attempt_count': '0',
        })
        param = hmac.new(
            '46024e8f31e295869a0e861eaed42cb1dd8454b55232d85f6c6764365079374b'.encode(),
            payload.encode(),
            hashlib.sha224
        ).hexdigest() + '.' + urllib.parse.quote(payload)
        encod = f'ig_sig_key_version=4&signed_body={param}'
        header = {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': user_agent,
            'X-IG-App-ID': '936619743392459',
        }
        response = ses.post('https://www.instagram.com/api/v1/accounts/login/', data=encod, headers=header)

        if 'logged_in_user' in response.text:
            success += 1
            kuki = convert_cookie(response.headers.get('Set-Cookie'))
            auth = f"{response.headers.get('ig-set-authorization')};{kuki}"
            followers, following = info(username)
            
            cetak = Tree(f'[bold green]🎉 LOGIN SUCCESS[/bold green]')
            cetak.add(f'👤 Username: {username}')
            cetak.add(f'📱 Method: ANDROID')
            cetak.add(f'🔐 Cookies: Extracted successfully')
            console.print(cetak)
            
            # Save to Android storage
            save_account_to_file(username, password)
            return True, kuki, auth
        else:
            print_error(f"Login failed for: {username}")
            return False, None, None
    except Exception as e:
        print_error(f"{e}")
        return False, None, None

def save_account_to_file(username, password):
    """Save account to /sdcard/Instagram/Accounts.txt without overwriting"""
    try:
        # Create directory if it doesn't exist
        directory = "/sdcard/Instagram"
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_success(f"Created directory: {directory}")
        
        file_path = os.path.join(directory, "Accounts.txt")
        
        # Check if account already exists
        existing_accounts = set()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '|' in line:
                        existing_username = line.split('|')[0]
                        existing_accounts.add(existing_username)
        
        # Only add if account doesn't exist
        if username not in existing_accounts:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"{username}|{password}\n")
            print_success(f"Account saved to: {file_path}")
        else:
            print_warning("Account already exists in file")
            
    except Exception as e:
        print_error(f"Failed to save account: {e}")

def extract_post_id_from_response(response_data):
    try:
        items = response_data.get("data", {}).get("xdt_api__v1__media__shortcode__web_info", {}).get("items", [])
        if items:
            post_id = items[0].get("id")
            return post_id
        return None
    except (AttributeError, KeyError, IndexError) as e:
        print_error(f"Error extracting ID: {e}")
        return None

def FixID(link):
    cookie = ("eyJkc191c2VyX2lkIjoiNjIzNDE1MjIzNTkiLCJzZXNzaW9uaWQiOiI2MjM0MTUyMjM1OSUzQVZxdXljRnNCcnd4R3BMJTNBMTUlM0FBWWhMNzhNZ3pmNXI1RG9SMkxhMHM5amlpQUlSZ2NFRkYxczVUWmJDQkEifQ==;"
              "csrftoken=z93Br6e724GDnrijW7w7WSNczNR4eWIi; ds_user_id=62341522359; "
              "sessionid=62341522359%3AVquycFsBrwxGpL%3A15%3AAYhL78Mgzf5r5DoR2La0s9jiiAIRgcEFF1s5TZbCBA; ig_nrcb=1; dpr=2;")

    csrf_token = re.search(r'csrftoken=([^;]+)', cookie).group(1)
    link = link.strip()

    shortcode_match = re.search(r'/p/([^/?]+)', link)
    if not shortcode_match:
        print_error("Invalid Instagram link format.")
        return None
    shortcode = shortcode_match.group(1)

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.instagram.com",
        "referer": f"https://www.instagram.com/p/{shortcode}/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "x-csrftoken": csrf_token,
        "x-fb-friendly-name": "PolarisPostRootQuery",
        "x-fb-lsd": "kMBb-Hg3FQu_G7aGngLE2w",
        "x-ig-app-id": "936619743392459",
        "x-root-field-name": "xdt_api__v1__media__shortcode__web_info",
        "cookie": cookie
    }

    payload = {
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisPostRootQuery",
        "variables": json.dumps({"shortcode": shortcode}),
        "server_timestamps": "true",
        "doc_id": "25540082168932123"
    }

    url = "https://www.instagram.com/graphql/query/"
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    post_id = extract_post_id_from_response(data)
    return post_id

def extract_bulk_accounts():
    """Extract accounts from bulk file"""
    print_header("BULK ACCOUNT EXTRACTION")
    
    try:
        file_path = Prompt.ask("📂 Enter file path (email|password format)")
        
        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return
        
        accounts_extracted = 0
        total_accounts = 0
        
        # Count total accounts first
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line.strip():
                    total_accounts += 1
        
        print_info(f"Found {total_accounts} accounts in file")
        print_separator()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Extracting accounts...", total=total_accounts)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            username = parts[0].strip()
                            password = parts[1].strip()
                            
                            if username and password:
                                print_processing(f"Account {line_num}/{total_accounts}: {username}")
                                success, cookie, auth = www_insta(username, password, "android")
                                if success:
                                    accounts_extracted += 1
                                progress.update(task, advance=1)
                            else:
                                print_warning(f"Line {line_num}: Invalid format")
                        else:
                            print_warning(f"Line {line_num}: Invalid format")
                    else:
                        print_warning(f"Line {line_num}: No separator found")
        
        print_header("EXTRACTION SUMMARY")
        print_success(f"Successfully extracted {accounts_extracted}/{total_accounts} accounts")
        print_info(f"Accounts saved to: /sdcard/Instagram/Accounts.txt")
        
    except Exception as e:
        print_error(f"Bulk extraction failed: {e}")

def extract_single_account():
    """Extract single account"""
    print_header("SINGLE ACCOUNT EXTRACTION")
    
    username = Prompt.ask("📧 Enter email/username")
    password = Prompt.ask("🔑 Enter password", password=True)
    
    if not username or not password:
        print_error("Username and password are required")
        return
    
    print_separator()
    print_processing(f"Extracting account: {username}")
    success, cookie, auth = www_insta(username, password, "android")
    
    if success:
        print_success("Account extracted successfully")
    else:
        print_error("Account extraction failed")

class InstagramLiker:
    def __init__(self, accounts_path="/sdcard/Instagram/Accounts.txt"):
        self.accounts_path = accounts_path
        self.stats = {
            'success': 0,
            'failed': 0,
            'total': 0
        }

    def extract_csrftoken(self, cookie):
        for part in cookie.split(';'):
            if 'csrftoken=' in part:
                return part.split('=')[1].strip()
        return None

    def extract_shortcode(self, link):
        match = re.search(r"/p/([^/]+)/", link)
        if not match:
            match = re.search(r"/reel/([^/]+)/", link)
        return match.group(1) if match else None

    def get_media_id(self, shortcode, cookie):
        url = "https://www.instagram.com/graphql/query/"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "x-ig-app-id": "936619743392459",
            "cookie": cookie
        }
        payload = {
            "variables": {"shortcode": shortcode},
            "doc_id": "8845758582119845"
        }

        r = requests.post(url, json=payload, headers=headers)
        try:
            data = r.json()
            return data["data"]["xdt_api__v1__media__shortcode__web_info"]["items"][0]["id"]
        except Exception:
            print_error("Failed to get media ID")
            return None

    def like_post(self, cookie, media_id, account_num):
        try:
            csrftoken = self.extract_csrftoken(cookie)
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "x-ig-app-id": "936619743392459",
                "content-type": "application/json",
                "x-fb-friendly-name": "usePolarisLikeMediaLikeMutation",
                "cookie": cookie
            }
            if csrftoken:
                headers["x-csrftoken"] = csrftoken

            payload = {
                "variables": {"media_id": media_id},
                "doc_id": "8244673538908708"
            }

            r = requests.post("https://www.instagram.com/graphql/query/", json=payload, headers=headers, timeout=10)
            success = r.status_code == 200
            
            if success:
                self.stats['success'] += 1
                console.print(f"[green]✅ Account {account_num}: Liked successfully[/green]")
            else:
                self.stats['failed'] += 1
                console.print(f"[red]❌ Account {account_num}: Failed to like[/red]")
                
            return success
        except Exception as e:
            self.stats['failed'] += 1
            console.print(f"[red]❌ Account {account_num}: Error - {str(e)}[/red]")
            return False

    def like_instagram_post(self):
        print_header("AUTO LIKER")
        
        # Load accounts
        if not os.path.exists(self.accounts_path):
            print_error(f"Accounts file not found: {self.accounts_path}")
            return

        with open(self.accounts_path, "r") as f:
            accounts = [x.strip() for x in f if x.strip()]

        if not accounts:
            print_error("No accounts found in the file!")
            return

        # User input
        link = Prompt.ask("🔗 Enter Instagram post/reel link")
        total_likes = IntPrompt.ask("❤️ How many likes do you want", default=len(accounts))
        
        # Get media ID
        print_processing("Getting media ID...")
        media_id = FixID(link)
        
        if not media_id:
            print_error("Failed to get media ID from the link")
            return

        print_success(f"Media ID: {media_id}")
        print_info(f"Total accounts available: {len(accounts)}")
        print_info(f"Target likes: {total_likes}")

        self.stats = {'success': 0, 'failed': 0, 'total': total_likes}

        # Start liking process
        print_separator()
        print_processing("Starting auto-like process...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task("Sending likes...", total=total_likes)
            
            # Use threading for faster execution
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for i in range(total_likes):
                    if i < len(accounts):
                        cookie = accounts[i].split("|")[-1] if "|" in accounts[i] else accounts[i]
                        future = executor.submit(self.like_post, cookie, media_id, i+1)
                        futures.append(future)
                        progress.update(task, advance=1)
                        time.sleep(0.5)  # Rate limiting
                
                # Wait for all tasks to complete
                for future in futures:
                    future.result()

        # Display final results
        print_separator()
        print_header("LIKING COMPLETED")
        
        results_table = Table(show_header=True, header_style="bold magenta")
        results_table.add_column("Metric", style="cyan")
        results_table.add_column("Count", style="white")
        
        results_table.add_row("Total Attempted", str(total_likes))
        results_table.add_row("Successful Likes", f"[green]{self.stats['success']}[/green]")
        results_table.add_row("Failed Likes", f"[red]{self.stats['failed']}[/red]")
        results_table.add_row("Success Rate", f"{ (self.stats['success']/total_likes)*100 if total_likes > 0 else 0:.1f}%")
        
        console.print(results_table)

def auto_liker_menu():
    """Auto liker menu"""
    liker = InstagramLiker()
    liker.like_instagram_post()
import requests
import json
import re

def extract_profile_user_id(profile_url):
    """
    Extract the user ID of the target Instagram profile
    """
    cookie_string = "csrftoken=z93Br6e724GDnrijW7w7WSNczNR4eWIi; ds_user_id=62341522359; sessionid=62341522359%3AVquycFsBrwxGpL%3A15%3AAYhL78Mgzf5r5DoR2La0s9jiiAIRgcEFF1s5TZbCBA; ig_nrcb=1; dpr=2;"
    cookies = {}
    for cookie in cookie_string.split(';'):
        cookie = cookie.strip()
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key] = value
    
    # Extract username from URL
    username = profile_url.rstrip('/').split('/')[-1]
    
    # Set up headers
    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'referer': profile_url,
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'x-csrftoken': cookies.get('csrftoken', ''),
        'x-ig-app-id': '1217981644879628'
    }
    
    try:
        # Method 1: Try to fetch the profile page and extract from JSON data
        print(f"Fetching profile data for: {username}")
        
        response = requests.get(profile_url, cookies=cookies, headers=headers)
        
        if response.status_code == 200:
            # Look for user ID in the response HTML
            html_content = response.text
            
            # Pattern 1: Look for "profilePage_"
            profile_id_match = re.search(r'"profilePage_([0-9]+)"', html_content)
            if profile_id_match:
                return profile_id_match.group(1)
            
            # Pattern 2: Look for "userId":"123456789"
            user_id_match = re.search(r'"user_id":"([0-9]+)"', html_content)
            if user_id_match:
                return user_id_match.group(1)
            
            # Pattern 3: Look for graphql data
            graphql_match = re.search(r'"id":"([0-9]+)"', html_content)
            if graphql_match:
                return graphql_match.group(1)
            
            print("Could not find user ID in HTML response. Trying API method...")
            
        # Method 2: Try GraphQL API approach
        api_url = "https://www.instagram.com/api/v1/users/web_profile_info/"
        params = {
            'username': username
        }
        
        api_headers = headers.copy()
        api_headers['x-requested-with'] = 'XMLHttpRequest'
        
        api_response = requests.get(api_url, params=params, cookies=cookies, headers=api_headers)
        
        if api_response.status_code == 200:
            data = api_response.json()
            if 'data' in data and 'user' in data['data']:
                return data['data']['user']['id']
        
        return None
        
    except Exception as e:
        print(f"Error extracting user ID: {e}")
        return None
import requests
import json
import re
import os

class InstagramFollower:
    def __init__(self, accounts_path="/sdcard/Instagram/Accounts.txt"):
        self.accounts_path = accounts_path

    def extract_csrftoken(self, cookie):
        for part in cookie.split(';'):
            if 'csrftoken=' in part:
                return part.split('=')[1].strip()
        return None

    def get_user_id(self, username, cookie):
        """
        Converts a username to a numeric user_id.
        """
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/128.0.0.0 Safari/537.36",
            "cookie": cookie
        }
        try:
            r = requests.get(url, headers=headers)
            data = r.json()
            return str(data["graphql"]["user"]["id"])
        except Exception:
            print("❌ Failed to fetch user ID for:", username)
            print("Response:", r.text)
            return None

    def follow_user(self, cookie, target_user_id):
        csrftoken = self.extract_csrftoken(cookie)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/128.0.0.0 Safari/537.36",
            "x-ig-app-id": "936619743392459",
            "content-type": "application/json",
            "fb_api_req_friendly_name": "usePolarisFollowMutation",
            "server_timestamps": "true",
            "cookie": cookie
        }
        if csrftoken:
            headers["x-csrftoken"] = csrftoken

        url = "https://www.instagram.com/graphql/query/"
        variables = {
            "target_user_id": target_user_id,
            "container_module": "profile",
            "nav_chain": "PolarisProfilePostsTabRoot:profilePage:1:via_cold_start"
        }
        payload = {
            "doc_id": "9740159112729312",
            "variables": json.dumps(variables)
        }

        r = requests.post(url, json=payload, headers=headers)
        return r.status_code == 200

    def follow_target(self):
        # Load accounts
        if not os.path.exists(self.accounts_path):
            print("❌ File not found:", self.accounts_path)
            return

        with open(self.accounts_path, "r") as f:
            accounts = [x.strip() for x in f if x.strip()]

        target = input("👤 Enter target username or user ID: ").strip()
        total_follows = int(input("🤝 How many follows do you want?: "))

        targetoprofile = extract_profile_user_id(target)

        success = 0
        count = 0

        for i in range(total_follows):
            cookie = accounts[i % len(accounts)].split("|")[-1]
            result = self.follow_user(cookie, targetoprofile)
            count += 1
            if result:
                success += 1
                print(f"✅ Successfully Followed {success}/{total_follows}")
            else:
                print(f"❌ Failed {count}/{total_follows}")

        print(f"\n🎯 Done! {success} out of {total_follows} follows sent successfully.")


# Example usage
def insta():
    follower = InstagramFollower()
    follower.follow_target()

def main_menu():
    """Main menu for the application"""
    print_logo()
    print_header("INSTAGRAM TOOL SUITE")
    
    while True:
        console.print("\n[bold cyan]🎯 MAIN MENU[/bold cyan]")
        console.print("[cyan]┌────────────────────────────────────────┐[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]1.[/yellow] 📦 Bulk Account Extraction           [cyan]│[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]2.[/yellow] 👤 Single Account Extraction         [cyan]│[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]3.[/yellow] ❤️  Auto Liker                        [cyan]│[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]4.[/yellow] ❤️  Auto Follow                        [cyan]│[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]4.[/yellow] 📊 View Statistics                   [cyan]│[/cyan]")
        console.print("[cyan]│[/cyan] [yellow]5.[/yellow] 🚪 Exit                              [cyan]│[/cyan]")
        console.print("[cyan]└────────────────────────────────────────┘[/cyan]")
        
        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5"], default="1")
        
        if choice == '1':
            extract_bulk_accounts()
        elif choice == '2':
            extract_single_account()
        elif choice == '3':
            auto_liker_menu()
        elif choice == '4':
            insta()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            console.print("[bold green]👋 Thank you for using Instagram Tool Suite![/bold green]")
            sys.exit(0)
        
        
        if Prompt.ask("\nReturn to main menu", choices=["y", "n"], default="y") == "n":
            break

def show_statistics():
    """Show statistics"""
    print_header("STATISTICS")
    
    stats_table = Table(show_header=True, header_style="bold magenta")
    stats_table.add_column("Metric", style="cyan")
    stats_table.add_column("Value", style="white")
    
    stats_table.add_row("Total Login Attempts", str(hitung))
    stats_table.add_row("Successful Logins", f"[green]{success}[/green]")
    stats_table.add_row("Checkpoint Accounts", f"[yellow]{checkpoint}[/yellow]")
    stats_table.add_row("Success Rate", f"{ (success/hitung)*100 if hitung > 0 else 0:.1f}%")
    
    console.print(stats_table)

def print_welcome_message():
    """Print welcome message"""
    print_header("WELCOME TO INSTAGRAM TOOL SUITE")
    
    features = Table(show_header=False, box=None)
    features.add_column("", style="cyan")
    features.add_column("", style="white")
    
    features.add_row("🎯", "Android-only login method")
    features.add_row("📦", "Bulk account extraction from files")
    features.add_row("👤", "Single account extraction")
    features.add_row("❤️", "Advanced auto-liker with threading")
    features.add_row("💾", "Non-overwriting account storage")
    features.add_row("🔐", "Secure cookie extraction")
    features.add_row("📊", "Real-time progress tracking")
    features.add_row("🎨", "Beautiful colored interface")
    
    console.print(features)
    print_separator()

if __name__ == "__main__":
    try:
        print_welcome_message()
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]👋 Program interrupted by user. Goodbye![/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]💥 Unexpected error: {e}[/bold red]")