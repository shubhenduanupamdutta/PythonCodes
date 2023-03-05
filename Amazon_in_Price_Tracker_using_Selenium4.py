from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

URL_PRODUCT = "https://www.amazon.in/LG-139-7-Inches-Ultra-OLED55G1PTZ/dp/B09FLYBVWG/?_encoding=UTF8&pd_rd_w=4JsrN"
                "&content-id=amzn1.sym.a591f53f-b25f-40ba-9fb6-d144bc8febfb&pf_rd_p=a591f53f-b25f-40ba-9fb6-d144bc8febfb&pf_rd_r=KXQ9XMQGMZ0E89TD8N8B&pd_rd_wg=Ilb27&pd_rd_r=529266f8-0acb-4f84-a92e-42e371e2f141&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(url=URL_PRODUCT)
price = driver.find_elements(By.CSS_SELECTOR, "span .a-price-whole")
print(type(price), len(price), price[-1].text, type(price[0]))
for prices in price:
    print(prices.text)

# Finding using XPath the price of the product
price = driver.find_element(By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[2]/span[2]')
print(price.text)

driver.quit()
