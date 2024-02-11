import requests
from bs4 import BeautifulSoup
import psycopg2
from dotenv import load_dotenv
import os
import datetime
import re

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def scrape_and_save_data(start_url):
    """The main function that the entire script performs."""
    process_page(start_url)

def process_page(url):
    """Searches for all references to cars."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    car_links = soup.find_all('a', class_='m-link-ticket')

    for link in car_links:
        car_url = link['href']
        process_car_page(car_url)
       
    next_page_link = soup.find('a', class_='page-link js-next')
    if next_page_link:
        next_page_url = next_page_link['href']
        if next_page_url != url:
            process_page(next_page_url)
    

def process_car_page(url):
    """The function that is responsible for scraping the car card."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #Car URL
    url = response.url
     
    #Title
    title = soup.find('h1', class_='head').text.strip()
     
    #Price
    info_price = soup.find('strong', class_='').text.strip()
    replace_price = info_price.replace('$', '').replace(' ', '')

    if replace_price.isdigit():
        price = int(replace_price)
    else:
        price = None
        
    #Odometer
    info_odometer = soup.find('div', class_='bold dhide').text.strip()
    if info_odometer:
        info_odometer = info_odometer.split('•')[0].strip()
        new_odometer = info_odometer.replace('пробіг', '').replace(' ', '') 
        odometer_number = int(new_odometer.replace('тис.км', ''))
        odometer = odometer_number * 1000
    
    #Name seller
    seller_info_div = soup.find('div', class_='seller_info_name bold')
    seller_info_h4 = soup.find('h4', class_='seller_info_name')

    if seller_info_div:
        username = seller_info_div.text.strip()
    elif seller_info_h4:
        a_tag = seller_info_h4.find('a')
        if a_tag:
            username = a_tag.text.strip()
        else:
            username = seller_info_h4.text.strip()
    else:
        username = "Ім’я не вказане"
    
    #Phone number 
    phone_number = None
    phone_number_span = soup.find("span", class_="phone bold")
    if phone_number_span:
        number = phone_number_span.text.strip()
        phone_number = number.replace('показати', '').replace(' ', '')

    #Image URL
    image_info= soup.find('img', class_='outline m-auto')
    image_url = image_info.get('src')
    
    #Image count 
    images_count = None
    images_count_tag = soup.find('a', class_='show-all link-dotted')
    if images_count_tag:
        text = images_count_tag.get_text(strip=True)
        match = re.search(r'\d+', text)
        if match:
            images_count = int(match.group())
    
    #Car number 
    state_num_span = soup.find('span', class_='state-num ua')
    car_number = None  

    if state_num_span:
        text_content = state_num_span.text.strip()
        match = re.search(r'[A-Z]{2} \d{4} [A-Z]{2}', text_content)
        
        if match:
            car_number = match.group()
    
    #Car vin
    car_vin = None
    vin_code = soup.find('span', class_='label-vin')

    if vin_code:
        car_vin = vin_code.text.strip()
    
    
    save_car_data(url, title, price, odometer, username, phone_number, image_url, images_count, car_number, car_vin)
   

def save_car_data(url, title, price, odometer, username, phone_number, image_url, images_count, car_number, car_vin):
    """Save data to db."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    sql = """
        INSERT INTO cars (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (url, title, price, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime.datetime.now())

    cur.execute(sql, values)
    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    start_url = "https://auto.ria.com/uk/car/used/"
    scrape_and_save_data(start_url)


