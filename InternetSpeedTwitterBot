# Keep in mind this code is to be used with GoogleChrome and you may need to put in a code during login into twitter.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Constansts, EMAIL, PASSWORD and URLS
Twitter_ID = YOUR_TWITTER_ID
Twitter_password = YOUR_TWTITER_PASSWORD
URL_SpeedTest = "https://www.speedtest.net/"
URL_Twitter = "https://twitter.com/home"
ISP_Twitter_Handle = "@ACTFibernet"

# Speed Constants
PROMISED_DOWN = 75
PROMISED_UP = 75

service = Service(ChromeDriverManager().install())

class InternetSpeedTwitterBot:
    """Gets internet speed from speedtest.net."""
    def __init__(self):
        self.driver = webdriver.Chrome(service=service)
        self.down = None
        self.up = None

    def get_internet_speed(self):
        driver1 = self.driver
        driver1.get(url=URL_SpeedTest)
        time.sleep(3)
        start_test = driver1.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        start_test.click()
        while True:
            try:
                download_speed = driver1.find_element(By.CSS_SELECTOR, "div.result-data span.download-speed")
                self.down = float(download_speed.text)
                upload_speed = driver1.find_element(By.CSS_SELECTOR, "div.result-data span.upload-speed")
                self.up = float(upload_speed.text)
            except ValueError:
                time.sleep(3)
            else:
                break
        time.sleep(3)

    def tweet_at_provider(self):
        driver2 = self.driver
        driver2.get(url=URL_Twitter)
        time.sleep(7)
        self.send_email(driver2)
        time.sleep(3)
        # input()
        self.send_password(driver2)
        time.sleep(3)
        self.get_and_send_verification_code(driver2)
        time.sleep(14)
        if ((PROMISED_UP - self.up) < 10 or (self.up > PROMISED_UP)) and \
            ((PROMISED_DOWN - self.down) < 10 or (self.down > PROMISED_DOWN)):
            self.tweet_good(driver2)
        else:
            self.tweet_complaint(driver2)
        time.sleep(7)
        driver2.quit()

    def send_email(self, driver):
        """Sends Email to twitter account."""
        email_input = driver.find_element(By.TAG_NAME, "input")
        email_input.send_keys(Twitter_ID)
        email_input.send_keys(Keys.ENTER)

    def send_password(self, driver):
        """Sends password to twitter account."""
        def password():
            time.sleep(3)
            password = driver.find_element(By.NAME, "password")
            password.send_keys(Twitter_password)
            password.send_keys(Keys.ENTER)

        try:
            password()
        except NoSuchElementException:
            send_phone = driver.find_element(By.TAG_NAME, "input")
            send_phone.send_keys("9749935538")
            send_phone.send_keys(Keys.ENTER)
            password()

    def get_and_send_verification_code(self, driver):
        verification_code = input("Enter the verification code: ")
        verify = driver.find_element(By.TAG_NAME, "input")
        verify.send_keys(verification_code)
        verify.send_keys(Keys.ENTER)

    def tweet_good(self, driver):
        good_tweet = f"Wow! I am getting downloads of {self.down} Mbps and uploads of {self.up} Mbps on a 75 Mbps " \
                     f"plan. Great service {ISP_Twitter_Handle}!!   "
        self.tweet(good_tweet, driver)

    def tweet_complaint(self, driver):
        complaint = f"Hey {ISP_Twitter_Handle}, What is the problem? I am getting only {self.down} Mbps downloads and " \
                    f"{self.up} Mbps uplaods when my plan is of 75 Mbps.   "
        self.tweet(complaint, driver)

    def tweet(self, text, driver):
        # input()
        tweet_box = driver.find_element(By.CSS_SELECTOR, "[aria-label= 'Tweet text']")
        tweet_box.send_keys(text)
        tweet_button = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        tweet_button.click()

NetSpeedTwitterBot = InternetSpeedTwitterBot()
NetSpeedTwitterBot.get_internet_speed()
# print(NetSpeedTwitterBot.up, NetSpeedTwitterBot.down)
NetSpeedTwitterBot.tweet_at_provider()
