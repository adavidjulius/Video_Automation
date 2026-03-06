import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def upload_video(video_path, title):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Go to YouTube Studio
        driver.get("https://studio.youtube.com")
        time.sleep(5)

        # Login (requires secrets)
        email = os.environ.get("YOUTUBE_EMAIL")
        password = os.environ.get("YOUTUBE_PASS")
        if not email or not password:
            print("❌ YouTube credentials not set")
            return

        # Email
        email_input = driver.find_element(By.NAME, "identifier")
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        # Click upload
        upload_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='create-icon']")
        upload_btn.click()
        time.sleep(2)

        # Select "Upload video"
        upload_video_btn = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-item[test-id='upload-beta']")
        upload_video_btn.click()
        time.sleep(3)

        # File input
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(os.path.abspath(video_path))
        time.sleep(10)  # Wait for upload

        # Title
        title_input = driver.find_element(By.CSS_SELECTOR, "ytcp-social-suggestions-textbox[id='title-textarea']")
        title_input.clear()
        title_input.send_keys(title)

        # Description
        desc_input = driver.find_element(By.CSS_SELECTOR, "ytcp-social-suggestions-textbox[id='description-textarea']")
        desc_input.send_keys(f"Auto-generated video about {title} #shorts #ai")

        # Set to Unlisted
        unlisted = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='UNLISTED']")
        unlisted.click()

        # Next -> Next -> Publish
        next_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='next-button']")
        next_btn.click()  # Details
        time.sleep(2)
        next_btn.click()  # Elements
        time.sleep(2)
        next_btn.click()  # Visibility
        time.sleep(2)

        publish_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='done-button']")
        publish_btn.click()

        print(f"✅ Uploaded: {title}")

    except Exception as e:
        print(f"❌ Upload failed: {e}")
        driver.save_screenshot("upload_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    video_files = [f for f in os.listdir(".") if f.endswith(".mp4")]
    if not video_files:
        print("No video found")
        sys.exit(1)
    latest = max(video_files, key=os.path.getctime)
    topic = sys.argv[1] if len(sys.argv) > 1 else "Untitled"
    upload_video(latest, topic)
