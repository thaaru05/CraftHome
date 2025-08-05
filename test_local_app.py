from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def test_local_app():
    LOCAL_URL = "http://localhost:8000"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")

    service = Service()
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        browser.get(LOCAL_URL)
        print("Local app opened successfully.")
        assert "CraftHome" in browser.title or "React App" in browser.title
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        browser.quit()
        print("Browser closed.")

if __name__ == "__main__":
    test_local_app()


#python manage.py runserver