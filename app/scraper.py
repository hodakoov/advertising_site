from datetime import datetime, timedelta, timezone
from time import sleep
from urllib.parse import parse_qs, urlencode, urlparse
import logging
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from app import create_app
from app.extensions import db
from app.models.post import Post


logging.basicConfig(
    format='%(levelname)s - %(message)s',
    level=logging.INFO
)

months_map = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}


def get_ad_creation_timestamp(raw_creation_time):
    now = datetime.now()
    if raw_creation_time.startswith('сегодня'):
        raw_creation_time = raw_creation_time.replace(
            'сегодня в', now.strftime('%d.%m.%Y')
        )
    elif raw_creation_time.startswith('вчера'):
        raw_creation_time = raw_creation_time.replace(
            'вчера в', (now - timedelta(days=1)).strftime('%d.%m.%Y')
        )
    else:
        date, time = raw_creation_time.split(' в ')
        day, month = date.split()
        month = months_map[month]
        year = now.year
        raw_creation_time = f'{day}.{month}.{year} {time}'
    added = datetime.strptime(raw_creation_time, '%d.%m.%Y %H:%M')
    if added > now:
        return added.replace(year=year - 1).replace(tzinfo=timezone.utc)
    else:
        return added.replace(tzinfo=timezone.utc)


def wait_for_unban(driver, url, delay_limit):
    retries_count = 0
    while driver.title.startswith('Доступ ограничен'):
        sleep(delay_limit * (2 ** (retries_count - 1)))
        retries_count += 1
        driver.delete_all_cookies()
        driver.get(url)


def scrap_ad(driver, ad_url, delay_limit):
    driver.get(ad_url)
    if driver.title.startswith('Доступ ограничен'):
        wait_for_unban(driver, ad_url, delay_limit)

    try:
        driver.switch_to.active_element
        ad_id = driver.find_element(
            By.XPATH, "//div[@data-item-id]"
        ).get_attribute('data-item-id')
        title = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
        price = driver.find_element(
            By.XPATH, "//span[@itemProp='price']"
        ).get_attribute('content')
        address = driver.find_element(
            By.XPATH, "//div[@itemProp='address']"
        ).text.split('\n')[0]
        desc = driver.find_element(By.XPATH, "//div[@itemProp='description']").text
        raw_creation_time = driver.find_element(
            By.XPATH, "//span[@data-marker='item-view/item-date']"
        ).text.replace('· ', '')
        added = get_ad_creation_timestamp(raw_creation_time)

        image_preview_elements = driver.find_elements(
            By.XPATH, "//li[@data-type='image']"
        )
        image_urls = []
        first_image_url = driver.find_element(
            By.XPATH, "//div[starts-with(@class, 'image-frame-wrapper')]"
        ).get_attribute('data-url')
        image_urls.append(first_image_url)
        if image_preview_elements:
            for element in image_preview_elements[1:]:
                element.click()
                sleep(1)
                image_url = driver.find_element(
                    By.XPATH, "//div[starts-with(@class, 'image-frame-wrapper')]"
                ).get_attribute('data-url')
                image_urls.append(image_url)
    except NoSuchElementException as error:
        logging.error(f'{error}, ad url: {ad_url}')
    else:
        return {
            'id': ad_id,
            'title': title,
            'price': None if price == '0' else int(price),
            'address': address,
            'desc': desc,
            'added': added,
            'image_urls': ' '.join(image_urls)
        }


def write_ads_to_db(ads):
    for ad in ads:
        post = Post(
            title=ad['title'],
            ad_id=ad['id'],
            ad_datetime=ad['added'],
            image_url=ad['image_urls'],
            address=ad['address'],
            price=ad['price'],
            description=ad['desc'],
            author_id=1
        )
        ad_exists = db.session.query(Post).filter(Post.ad_id == ad['id']).count()
        if not ad_exists:
            db.session.add(post)
    db.session.commit()


def scrap_ads(initial_url, page_limit, delay_limit):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--headless=new")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.implicitly_wait(2)

    driver.get(initial_url)

    logging.info('Collecting ad page urls...')
    ad_elements = driver.find_elements(
        By.XPATH, "//div[starts-with(@class, 'iva-item-slider')]/a"
    )
    ad_urls = []
    ad_urls.extend([element.get_attribute('href') for element in ad_elements])

    ads_count = int(driver.find_element(
        By.XPATH, "//span[starts-with(@class, 'page-title-count')]"
    ).text.replace(' ', ''))

    sleep(random.uniform(5, delay_limit))

    if ads_count > len(ad_urls) and (page_limit is None or page_limit > 1):
        last_page_url = driver.find_elements(
            By.XPATH, "//a[@class='pagination-page']"
        )[-1].get_attribute('href')
        url_parts = urlparse(last_page_url)
        query = parse_qs(url_parts.query)
        last_page_num = int(query['p'][0])
        ads_list_pages_to_scrap = min(page_limit, last_page_num)

        for ads_list_page_num in range(2, ads_list_pages_to_scrap + 1):
            query['p'] = ads_list_page_num
            ads_list_page_url = url_parts._replace(
                query=urlencode(query, doseq=True)
            ).geturl()
            driver.get(ads_list_page_url)
            if driver.title.startswith('Доступ ограничен'):
                wait_for_unban(driver, ads_list_page_url, delay_limit)

            ad_elements = driver.find_elements(
                By.XPATH, "//div[starts-with(@class, 'iva-item-slider')]/a"
            )
            ad_urls.extend([element.get_attribute('href') for element in ad_elements])

            sleep(random.uniform(5, delay_limit))

    if len(ad_urls) > ads_count:
        ad_urls = ad_urls[:ads_count]

    ad_urls_count = len(ad_urls)
    ads = []
    for count, ad_url in enumerate(ad_urls, start=1):
        logging.info(f'Scraping {count} of {ad_urls_count} ads.')
        ad = scrap_ad(driver, ad_url, delay_limit)
        if ad:
            ads.append(ad)
        sleep(random.uniform(5, delay_limit))

    driver.quit()
    logging.info('Scraper session finished.')

    return ads


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        initial_url = app.config['SCRAPER_INITIAL_URL']
        page_limit = app.config['SCRAPER_PAGE_LIMIT']
        delay_limit = app.config['SCRAPER_DELAY_LIMIT']

        ads = scrap_ads(initial_url, page_limit, delay_limit)
        write_ads_to_db(ads)
