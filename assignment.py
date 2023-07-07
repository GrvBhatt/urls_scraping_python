import csv
import requests
from bs4 import BeautifulSoup

def scrape_product_listing(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_url = product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()
        rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        num_reviews = product.find('span', {'class': 'a-size-base'}).text.strip().replace(',', '')

        data.append([product_url, product_name, product_price, rating, num_reviews])

    return data



def scrape_multiple_pages(num_pages):
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    
    all_data = []
    for page in range(1, num_pages + 1):
        url = base_url + str(page)
        data = scrape_product_listing(url)
        all_data.extend(data)

    # Save the data to a CSV file
    with open('product_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
        writer.writerows(all_data)

    print('Scraping complete. Data saved to product_list.csv.')


scrape_multiple_pages(20)

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_info = soup.find('div', {'id': 'prodDetails'})

    description = soup.find('div', {'id': 'productDescription'}).text.strip()
    asin = product_info.find('th', text='ASIN').find_next('td').text.strip()
    product_description = product_info.find('th', text='Product Description').find_next('td').text.strip()
    manufacturer = product_info.find('th', text='Manufacturer').find_next('td').text.strip()

    return description, asin, product_description, manufacturer



def scrape_product_details(urls):
    all_data = []
    for url in urls:
        data = scrape_product_page(url)
        all_data.append(data)

    # Save the data to a CSV file
    with open('product_details.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Description', 'ASIN', 'Product Description', 'Manufacturer'])
        writer.writerows(all_data)

    print('Scraping complete. Data saved to product_details.csv.')


import pandas as pd

df = pd.read_csv('product_list.csv')
urls = df['Product URL'].tolist()

scrape_product_details(urls[:200])  # Scrape the first 200 URLs

