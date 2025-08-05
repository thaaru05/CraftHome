from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time


browser = None


LOCAL_URL = "http://127.0.0.1:8000/"

def open_local_app():
    global browser
    if browser is None:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  
        service = Service()  
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.get(LOCAL_URL)
        print(f"Opened {LOCAL_URL}")
    else:
        print("Browser is already open.")

def close_local_app():
    global browser
    if browser:
        browser.quit()
        browser = None
        print("Browser closed.")
    else:
        print("Browser is already closed.")

def manual_test():
    while True:
        cmd = input("Enter command (open / close / exit): ").strip().lower()
        if cmd == "open":
            open_local_app()
        elif cmd == "close":
            close_local_app()
        elif cmd == "exit":
            close_local_app()
            break
        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    manual_test()
