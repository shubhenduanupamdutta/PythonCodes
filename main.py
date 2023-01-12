import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

URL = "https://www.amazon.in/LG-139-7-Inches-Ultra-OLED55G1PTZ/dp/B09FLYBVWG/?_encoding=UTF8&ref_=pd_gw_ci_mcx_mr_hp_atf_m"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
ACCEPT_LANGUAGE = "en-US,en;q=0.9,hi;q=0.8"
PRICE_LIMIT = 145000.0
MY_EMAIL = "shubhenduanupam@outlook.com"
PASSWORD = "Coronaisthenew$upervirus2020"


def get_price() -> (float, str):
    """Gets price in Rupees(float) of the product in the URL from amazon.in"""
    response = requests.get(url=URL, headers={"User-Agent": USER_AGENT, "Accept-Language": ACCEPT_LANGUAGE})
    amazon_product_page = response.text
    soup = BeautifulSoup(amazon_product_page, "lxml")
    # print(soup.prettify())
    price_rupees = float(soup.find(name="span", class_="a-price-whole").getText().replace(",",""))
    product_title = soup.find(name="span", id="productTitle").getText()
    return price_rupees, product_title


def send_mail(price_product, title_product):
    """Send mail to inform about price drop to the user."""
    with smtplib.SMTP("smtp.office365.com", port=587) as connection:
        # Securing our connection, TLS  = Transport Layer Security
        connection.starttls()
        # Login into email
        connection.login(user=MY_EMAIL, password=PASSWORD)
        # Sending the mail
        subject = f"Price Drop in {title_product}"
        message = f"Subject:{subject}\n\nPrice of {title_product} has gone down to Rs.{price_product}.\n" \
                  f"Here is the link : {URL}"
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="gappudutta@gmail.com",
            msg=message
        )


price, title = get_price()

if price < PRICE_LIMIT:
    send_mail(price, title)