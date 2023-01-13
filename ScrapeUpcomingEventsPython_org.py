from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL = "https://www.python.org/"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url=URL)

# Getting the events
upcoming_events = driver.find_elements(By.CSS_SELECTOR, ".event-widget li")
# getting time and even from upcoming_events
events = {}
for i, event in enumerate(upcoming_events):
    time = (event.find_element(By.TAG_NAME, "time")).text
    event_name = event.find_element(By.TAG_NAME, "a").text
    events[i] = {"time": time, "name": event_name}

print(events)
