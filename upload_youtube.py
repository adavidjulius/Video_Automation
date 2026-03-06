# upload_youtube.py - Uses free browser automation
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def upload_to_youtube(video_path, title, description):
    """Upload video using free browser automation"""
    
    # Setup headless Chrome (runs on GitHub)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Go to YouTube Studio
        driver.get("https://studio.youtube.com")
        time.sleep(5)
        
        # Login (using secrets)
        email_input = driver.find_element(By.NAME, "identifier")
        email_input.send_keys(os.environ["YOUTUBE_EMAIL"])
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(os.environ["YOUTUBE_PASS"])
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Click upload button
        upload_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='create-icon']")
        upload_btn.click()
        time.sleep(2)
        
        # Select upload video
        upload_video_btn = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-item[test-id='upload-beta']")
        upload_video_btn.click()
        time.sleep(3)
        
        # Upload file
        file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(os.path.abspath(video_path))
        time.sleep(10)  # Wait for upload
        
        # Fill details
        title_input = driver.find_element(By.CSS_SELECTOR, "ytcp-social-suggestions-textbox[id='title-textarea']")
        title_input.clear()
        title_input.send_keys(title)
        
        desc_input = driver.find_element(By.CSS_SELECTOR, "ytcp-social-suggestions-textbox[id='description-textarea']")
        desc_input.send_keys(description)
        
        # Set to unlisted (safer)
        visibility_radio = driver.find_element(By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='UNLISTED']")
        visibility_radio.click()
        
        # Publish
        next_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='next-button']")
        next_btn.click()  # Details
        time.sleep(2)
        next_btn.click()  # Elements
        time.sleep(2)
        next_btn.click()  # Visibility
        time.sleep(2)
        
        publish_btn = driver.find_element(By.CSS_SELECTOR, "ytcp-button[id='done-button']")
        publish_btn.click()
        
        print(f"✅ Video uploaded: {title}")
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        driver.save_screenshot("upload_error.png")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    video_files = [f for f in os.listdir(".") if f.endswith(".mp4")]
    if video_files:
        latest_video = max(video_files, key=os.path.getctime)
        topic = sys.argv[1] if len(sys.argv) > 1 else "Awesome Video"
        upload_to_youtube(
            latest_video, 
            f"{topic} - Daily AI Video", 
            f"Auto-generated video about {topic} #shorts #ai #coding"
        )
