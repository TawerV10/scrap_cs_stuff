from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time

def get_html(url, ua, path):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-agent={ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

    service = Service(path)
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.maximize_window()
        driver.get(url)
        time.sleep(30)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

def get_data():
    data = []
    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')

    all_knives = soup.find_all(class_='c-asset c-asset--steam ng-star-inserted')
    for item in all_knives:
        title = item.find('price', class_='ng-star-inserted').text.strip()
        try:
            sale = item.find('div', class_='o-assetBadge o-assetBadge--discount ng-star-inserted').text.strip()
        except Exception:
            sale = None
        float = item.find(class_='o-qualityChart__info ng-star-inserted').find('span').text.strip()
        href = item.find('div', class_='u-game u-game--csGo').find('img').get('src').strip()

        data.append({
            'title': title,
            'sale': sale,
            'href': href,
            'float': float
        })

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    ua = UserAgent().random
    url = 'https://dmarket.com/ua/ingame-items/item-list/csgo-skins/knife?utm_source=google&utm_medium=cpc&utm_campaign=dm_new_brand-ua_s&gclid=Cj0KCQjwlK-WBhDjARIsAO2sErTTm_bYzJnbNjXoBuQNow9ovulB80nNG2iI_AV9OQ_qC7VKqazufkoaAhj2EALw_wcB&price-to=1000&price-from=800'
    path = r'C:\Users\name\Documents\GitHub\scrap_cs_stuff\chromedriver.exe'

    get_html(url, ua, path)
    get_data()

if __name__ == '__main__':
    main()