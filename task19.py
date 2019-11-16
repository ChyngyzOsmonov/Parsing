import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url) 
    return r.text


def get_tolal_pages(html):
    soup = BeautifulSoup(html, features='lxml')
    
    pages = soup.find('ul', class_='pagn').find('li', class_='pagn-last').find_all('a')[-1].get('href')
    total_pages = pages.split('&')[1].split('=')[1]
    
    return int(total_pages)


def write_csv(data):
    with open('lalafo.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['desc'],
                          data['price'],
                          data['url']) )


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='content-size-wrapper main-section bg-white d-flex ').find_all('article', class_='listing-item')
    for ad in ads:
        try:
            title = ad.find('div', class_='listing-item-main').find('a').text.strip()
        except:
            title = ''
        
        try:
            url ='https://lalafo.kg' + ad.find('div', class_='listing-item-main').find('a').get('href')
        except:
            url = ''

        try:
            price = ad.find('p', class_='listing-item-title').text.strip()
        except:
            price = ''

        try:
            desc = ad.find('p', class_='listing-item-description').text.strip()
        except:
            desc = ''
        
        
        data = {'title': title,
                'desc': desc,
                'price': price,
                'url': url}
        
        write_csv(data)


def main():
    url = 'https://lalafo.kg/bishkek/q-samsung?currency=KGS'
    base_url = 'https://lalafo.kg/bishkek/'
    page_part = '&page='
    query_part = 'q-samsung?currency=KGS'

    total_pages =get_tolal_pages(get_html(url))
    
    for i in range(1, total_pages):
        url_gen = base_url + query_part + page_part + str(i)
        #print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()