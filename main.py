import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import re

GOOGLE_FORMS_URL = "https://forms.gle/q7VEDtJoWVvMpa6RA"
ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(url=ZILLOW_CLONE_URL)

zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")

# getting house addresses
all_house_addresses = soup.find_all(name="address", attrs={'data-test': 'property-card-addr'})
house_address = [address.getText() for address in all_house_addresses]
cleaned_addresses = [clean_addresses.strip() for clean_addresses in house_address]
# print(cleaned_addresses)

# getting house links
all_house_links_tag = soup.find_all(name="a", attrs={'data-test': 'property-card-link'})
all_house_links = [tag['href'] for tag in all_house_links_tag]
cleaned_house_links = [cleaned_link.strip() for cleaned_link in all_house_links]
# print(cleaned_house_links)

# Getting house prices
all_house_prices = soup.find_all(name="span", attrs={"data-test": "property-card-price"})
all_house_prices_text = [price_text.getText() for price_text in all_house_prices]


# Clean the house prices
def clean_price(price):
    # Remove '/mo' and '+' characters
    cleaned_price = price.replace('/mo', '').replace('+', '').strip()
    # Remove 'bd' patterns and extra whitespace
    cleaned_price = re.sub(r'\s*\d*bd', '', cleaned_price).strip()
    return cleaned_price


all_house_prices_text_cleaned = [clean_price(text) for text in all_house_prices_text]

# Print cleaned house prices
# print(all_house_prices_text_cleaned)

# Part 2 Filling the Google forms with Selenium

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(cleaned_house_links)):
    driver.get(GOOGLE_FORMS_URL)
    time.sleep(2)

    address_line = driver.find_element(By.XPATH,
                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                             '1]/div/div[1]/input')
    price_line = driver.find_element(By.XPATH,
                                     value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                           '1]/div/div[1]/input')
    link_line = driver.find_element(By.XPATH,
                                    value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                          '1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_line.send_keys(cleaned_addresses[n])
    price_line.send_keys(all_house_prices_text_cleaned[n])
    link_line.send_keys(cleaned_house_links[n])
    submit_button.click()
