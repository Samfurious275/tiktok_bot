# uploader.py

from selenium.webdriver.chrome.service import Service
import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
def upload_to_tiktok(video_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(executable_path=config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Anti-detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

    print("[🌐] Opening TikTok...")
    driver.get("https://www.tiktok.com/")
    time.sleep(5)

    # 🔐 Load cookies
    if os.path.exists(config.COOKIE_FILE):
        try:
            with open(config.COOKIE_FILE, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    cookie['domain'] = '.tiktok.com'
                    driver.add_cookie(cookie)
            print("[🍪] Loaded cookies")
            driver.refresh()
            time.sleep(5)
        except Exception as e:
            print(f"[⚠️] Failed to load cookies: {e}")

    # 🧑‍💻 Check login
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "user-avatar")] | //span[text()="Profile"]'))
        )
        print("[✅] Already logged in!")
    except:
        print("[🔐] Not logged in. Starting login...")
        do_login(driver)

    # 📤 Go to upload page
    print("[📤] Opening upload page...")
    driver.get("https://www.tiktok.com/upload")
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
    except:
        print("[❌] Upload page failed to load")
        driver.quit()
        return

    # 📎 Attach video
    try:
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(os.path.abspath(video_path))
        print(f"[📎] Attached: {os.path.basename(video_path)}")
    except Exception as e:
        print(f"[❌] Failed to attach: {e}")
        driver.quit()
        return

    # ⏳ Wait for upload processing
    print("[⏳] Waiting for upload processing...")
    try:
        WebDriverWait(driver, 40).until(
            EC.invisibility_of_element_located((By.XPATH, '//circle[@stroke-dasharray="49 50"]'))
        )
        print("[✅] Upload processing complete.")
    except Exception as e:
        print(f"[⚠️] Upload may still be processing: {e}")

    # 🖊️ Add caption
    print("[📝] Adding caption...")
    try:
        caption_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-e2e="caption"]'))
        )
        caption_box.click()
        time.sleep(1)
        caption_box.send_keys("#fyp #viral #trending")
        print("[✅] Caption added.")
    except Exception as e:
        print(f"[⚠️] Failed to add caption: {e}")

    # 📣 Click final "Post" button
    print("[🖱️] Clicking final Post button...")
    try:
        post_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="post_video_button"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_button)
        time.sleep(1)

        try:
            post_button.click()
            print("[✅] Post button clicked!")
        except:
            print("[🖱️] Normal click failed. Using JS click.")
            driver.execute_script("arguments[0].click();", post_button)
            print("[✅] JS click successful!")

    except Exception as e:
        print(f"[❌] Failed to click Post button: {e}")
        driver.quit()
        return

    # 🚨 Handle "Continue to post?" modal
    print("[🔍] Checking for 'Continue to post?' modal...")
    try:
        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Post now"]]'))
        )
        print("[🖱️] 'Post now' modal detected. Clicking...")
        driver.execute_script("arguments[0].click();", continue_button)
        time.sleep(3)
        print("[✅] Modal accepted.")
    except Exception as e:
        print("[🟢] No modal appeared.")

    # ✅ Final wait
    time.sleep(15)

    # 💾 Save cookies
    try:
        cookies = driver.get_cookies()
        with open(config.COOKIE_FILE, 'wb') as f:
            pickle.dump(cookies, f)
        print("[🍪] Session saved.")
    except Exception as e:
        print(f"[⚠️] Failed to save cookies: {e}")

    driver.quit()
def do_login(driver):
    """Perform login if not already logged in"""
    print("[🔐] Navigating to login page...")
    driver.get("https://www.tiktok.com/login")
    time.sleep(5)

    try:
        print("[📧] Entering login credentials...")
        email_input = driver.find_element(By.XPATH, '//input[@type="text"]')
        password_input = driver.find_element(By.XPATH, '//input[@type="password"]')

        email_input.send_keys(config.TIKTOK_USERNAME)
        password_input.send_keys(config.TIKTOK_PASSWORD)

        login_button = driver.find_element(
            By.XPATH,
            '//button[span[text()="Log in"]] | //button[contains(text(), "Log in")]'
        )
        login_button.click()

        print("[⏳] Login submitted. Please solve CAPTCHA if prompted...")
        time.sleep(15)  # Give user time to solve CAPTCHA manually
    except Exception as e:
        print(f"[⚠️] Login failed: {e}")
