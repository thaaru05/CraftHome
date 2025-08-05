from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

# ---- CONFIG ----
URL = "http://localhost:8000"
USERNAME = "thaaru@gmail.com"
PASSWORD = "thaaru"

# ---- START DRIVER ----
options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)

def test_open_app():
    try:
        driver.get(URL)
        print("✅ App opened.")
    except Exception as e:
        print("❌ Failed to open app:", e)

def test_delete_cookies():
    try:
        driver.delete_all_cookies()
        print("✅ Cookies deleted.")
    except Exception as e:
        print("❌ Failed to delete cookies:", e)

def test_session_storage():
    try:
        driver.get(URL)
        time.sleep(2)
        session_data = driver.execute_script("return window.sessionStorage;")
        print("📦 Session Storage:", session_data)
    except Exception as e:
        print("❌ Failed to read session storage:", e)

def test_window_size():
    try:
        driver.set_window_rect(width=1024, height=768)
        print("✅ Window resized to 1024x768.")
    except Exception as e:
        print("❌ Failed to resize window:", e)

def test_registration(role="user"):
    try:
        driver.get(URL + "/register")
        time.sleep(2)
        driver.find_element(By.ID, "name").send_keys(f"{role}_user")
        driver.find_element(By.ID, "email").send_keys(f"{role}@email.com")
        driver.find_element(By.ID, "password").send_keys("test123")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]").click()
        print(f"✅ {role.capitalize()} registered.")
    except Exception as e:
        print(f"❌ Registration failed for {role}:", e)

def test_invalid_login():
    try:
        driver.get(URL + "/login")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys("wronguser")
        driver.find_element(By.ID, "password").send_keys("wrongpass")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(1)
        error_text = driver.find_element(By.CLASS_NAME, "text-red-500").text
        print("🔒 Error Message:", error_text)
        assert "invalid" in error_text.lower()
    except Exception as e:
        print("❌ Invalid login test failed:", e)

def test_valid_login_and_purchase():
    try:
        driver.get(URL + "/login")
        time.sleep(2)
        driver.find_element(By.ID, "email").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        time.sleep(2)
        print(f"✅ Logged in as {USERNAME} with password: {PASSWORD}")

        # Simulate purchasing an item
        driver.find_element(By.XPATH, "//button[contains(text(), 'Add to Cart')]").click()
        driver.find_element(By.XPATH, "//a[contains(text(), 'Cart')]").click()
        driver.find_element(By.XPATH, "//button[contains(text(), 'Checkout')]").click()
        print("🛒 Item purchased.")
    except Exception as e:
        print("❌ Valid login or purchase failed:", e)

def test_invoice_print():
    try:
        driver.get(URL + "/invoice")
        time.sleep(1)
        invoice_text = driver.find_element(By.TAG_NAME, "body").text
        print("🧾 Invoice:\n", invoice_text)
    except Exception as e:
        print("❌ Invoice test failed:", e)

def test_logo_visibility():
    try:
        driver.get(URL)
        logo = driver.find_element(By.TAG_NAME, "img")
        assert logo.is_displayed()
        print("✅ Logo is visible.")
    except Exception as e:
        print("❌ Logo visibility test failed:", e)

def test_auto_suggestions():
    try:
        search = driver.find_element(By.NAME, "search")
        search.send_keys("sh")
        time.sleep(1)
        suggestions = driver.find_elements(By.CLASS_NAME, "suggestion")
        print("🔍 Auto-suggestions:", [s.text for s in suggestions])
        assert len(suggestions) > 0
    except Exception as e:
        print("❌ Auto-suggestions test failed:", e)

def test_dropdowns():
    try:
        driver.get(URL)
        single_dropdown = Select(driver.find_element(By.ID, "category-select"))
        single_dropdown.select_by_visible_text("Books")
        print("📘 Single dropdown works.")

        multi_dropdown = Select(driver.find_element(By.ID, "multi-select"))
        multi_dropdown.select_by_index(0)
        multi_dropdown.select_by_index(1)
        print("📦 Multi dropdown works.")
    except Exception as e:
        print("❌ Dropdown test failed:", e)

# ---- RUN TEST CASES ----
try:
    test_open_app()
    test_delete_cookies()
    test_session_storage()
    test_window_size()
    test_registration("user")
    test_registration("admin")
    test_registration("guest")
    test_invalid_login()
    test_valid_login_and_purchase()
    test_invoice_print()
    test_logo_visibility()
    test_auto_suggestions()
    test_dropdowns()
finally:
    driver.quit()
    print("🚪 Browser closed.")
