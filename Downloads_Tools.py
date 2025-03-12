import os
import time
import yt_dlp
import requests
import qrcode
import colorama
import platform
import re
from urllib.parse import urlparse
from colorama import Fore
from tqdm import tqdm

# Initialize colorama
colorama.init(autoreset=True)

# Create necessary folders
os.makedirs("Downloads/Videos", exist_ok=True)
os.makedirs("Downloads/Photos", exist_ok=True)
os.makedirs("Downloads/QR", exist_ok=True)

# Detect OS for the clear command
def clear_screen():
    """Clear screen for better UI"""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def banner():
    clear_screen()
    print(Fore.CYAN + r"""
     ██████╗ ██████╗  ██████╗ ███╗   ██╗██████╗ ████████╗
    ██╔════╝ ██╔══██╗██╔═══██╗████╗  ██║██╔══██╗╚══██╔══╝
    ██║  ███╗██████╔╝██║   ██║██╔██╗ ██║██║  ██║   ██║   
    ██║   ██║██╔═══╝ ██║   ██║██║╚██╗██║██║  ██║   ██║   
    ╚██████╔╝██║     ╚██████╔╝██║ ╚████║██████╔╝   ██║   
     ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═══╝╚═════╝    ╚═╝   
    """)
    print(Fore.YELLOW + "🔥 Download Videos, Photos & Generate QR Codes 🔥")
    print(Fore.GREEN + "GitHub: https://github.com/KevinKhemra007")
    print(Fore.RED + "Telegram: https://t.me/hackisreal007")
    print(Fore.YELLOW + "TikTok: https://www.tiktok.com/@raatechofficial" )
    print(Fore.YELLOW + "=" * 50)

def loading_animation():
    """Loading animation with ASCII art"""
    animation = ["[▓▓░░░░░░░░░]", "[▓▓▓▓░░░░░░░░]", "[▓▓▓▓▓▓░░░░░░]", "[▓▓▓▓▓▓▓▓░░░░]", "[▓▓▓▓▓▓▓▓▓▓░░]", "[▓▓▓▓▓▓▓▓▓▓▓▓]"]
    for i in animation:
        print(Fore.MAGENTA + f"\r[⚡] Loading {i}", end="", flush=True)
        time.sleep(0.3)
    print("\n")

def sanitize_filename(filename):
    """Remove invalid characters from filenames"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def get_file_extension(url):
    """Extract the file extension safely from the URL"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    extension = filename.split('.')[-1] if '.' in filename else 'jpg'
    return extension

def download_video(url):
    """Download video from any social media platform"""
    loading_animation()
    ydl_opts = {
        'outtmpl': 'Downloads/Videos/%(title)s.%(ext)s',
        'format': 'best',
        'quiet': False,
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(Fore.GREEN + "[✅] Video saved in Downloads/Videos/")
    except Exception as e:
        print(Fore.RED + f"[❌] Error: {e}")

def download_photo(url, filename):
    """Download any image format from a URL"""
    loading_animation()
    filename = sanitize_filename(filename)
    extension = get_file_extension(url)
    filepath = f"Downloads/Photos/{filename}.{extension}"
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(filepath, 'wb') as file, tqdm(
        desc=f"[⬇] Downloading {filename}.{extension}",
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            bar.update(len(chunk))
    print(Fore.GREEN + f"[✅] Photo saved in {filepath}")

def generate_qr(link):
    """Convert link to QR code"""
    loading_animation()
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    qr_img.save("Downloads/QR/qrcode.png")
    print(Fore.GREEN + "[✅] QR Code saved in Downloads/QR/")

def open_downloads_folder():
    """Open the Downloads folder automatically"""
    if platform.system() == "Windows":
        os.system("explorer Downloads")
    elif platform.system() == "Linux":
        os.system("xdg-open Downloads")
    elif platform.system() == "Darwin":
        os.system("open Downloads")

def main():
    """Main Menu"""
    while True:
        banner()
        print("[1] Download Video (All Social Media)")
        print("[2] Download Photo (Any Format)")
        print("[3] Generate QR Code")
        print("[4] Open Downloads Folder")
        print("[5] Exit")
        choice = input("[📌] Enter your choice: ")

        if choice == "1":
            url = input("[🎥] Enter video URL from Facebook, YouTube, TikTok, Instagram, Twitter, etc.: ")
            download_video(url)
        elif choice == "2":
            url = input("[📸] Enter photo URL: ")
            filename = input("[💾] Enter filename (without extension): ")
            download_photo(url, filename)
        elif choice == "3":
            link = input("[🔗] Enter link for QR Code: ")
            generate_qr(link)
        elif choice == "4":
            open_downloads_folder()
        elif choice == "5":
            print("[🛑] Exiting...")
            break
        else:
            print("[❌] Invalid choice! Try again.")

if __name__ == "__main__":
    main()
