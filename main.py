import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plyer import notification
from datetime import datetime
import keyboard

def setup_browser():
    options = webdriver.ChromeOptions()
    # Suppress unwanted logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    return webdriver.Chrome(options=options)

def login(browser, url):
    try:
        print("Opening login page...")
        browser.get(url)
        print("Please log in through the browser window.")
        print("The program will continue once you're logged in.")
        print("Press Enter after you have logged in...")
        input()
        
        # After login, enable headless mode for background operation
        browser.quit()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # Add the same log suppression to headless browser
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        return browser
        
    except Exception as e:
        print(f"Error during login: {e}")
        browser.quit()
        exit(1)

def check_website(browser):
    try:
        browser.refresh()
        page_text = browser.page_source.lower()
        return "studass" not in page_text  # If hjelp is not in text, we're logged in and can check for queue
    except Exception as e:
        print(f"Error checking website: {e}")
        return False

def send_notification():
    notification.notify(
        title='Student Assistant Queue',
        message='Someone needs help!',
        timeout=10
    )

def toggle_pause(paused):
    paused['value'] = not paused['value']
    status = "PAUSED" if paused['value'] else "RESUMED"
    print(f"\nQueue helper {status}")

def exit_program(running, browser):
    running['value'] = False
    print("\nQueue helper stopped.")
    browser.quit()
    keyboard.unhook_all()

def main():
    url = 'https://tdt4102.idi.ntnu.no/studass'
    check_count = 0
    paused = {'value': False}
    running = {'value': True}
    
    browser = setup_browser()
    browser = login(browser, url)
    
    print("Queue helper started. Press Ctrl+X to exit, Ctrl+P to pause/resume.")
    keyboard.add_hotkey('ctrl+p', toggle_pause, args=(paused,))
    keyboard.add_hotkey('ctrl+x', exit_program, args=(running, browser,))
    
    while running['value']:
        if not paused['value']:
            current_time = datetime.now()
            check_count += 1
            print(f"Check #{check_count} at {current_time.strftime('%H:%M:%S')}")
            
            if check_website(browser):
                send_notification()
                print("Notification sent!")
        
        time.sleep(5)

if __name__ == "__main__":
    main()