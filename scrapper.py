from bs4 import BeautifulSoup
from requests import get
from database import Database

db = Database()


class Scrapper:
    def __init__(self, database=db):
        self.db = database
        self.URL = ''
        self.apply_url = ''

    def get_offers_from_olx(self):
        self.URL = 'https://www.olx.pl/praca/'
        last_page = int(
            BeautifulSoup(get(self.URL).content, features='html.parser').find(attrs={'data-cy': 'page-link-last'})
                .get_text())

        for page in range(1, last_page + 1):
            page_content = get(f'{self.URL}?page={page}')
            bs = BeautifulSoup(page_content.content, features='html.parser')
            for offer in bs.find_all('div', class_='offer-wrapper'):
                offer_url = offer.find('a')['href']
                if self.db.get_offer_id(offer_url=offer_url) == -1:
                    footer = offer.find('td', class_='bottom-cell')
                    name = offer.find("strong").get_text().strip()
                    location = footer.find('small', class_='breadcrumb').get_text().strip()
                    self.db.add_new_offer(name=name,
                                          offer_url=offer_url,
                                          apply_url="",
                                          location=location,
                                          portal="olx.pl")

            print(f"Loading... Done {round(page / last_page * 100, 2)}%")


    def get_offers_from_praca(self):
        self.URL = 'https://www.praca.pl'
        self.apply_url = 'https://www.praca.pl/aplikuj_'
        page = 1
        while True:
            page_content = get(f'{self.URL}/oferty-pracy_{page}')
            bs = BeautifulSoup(page_content.content, features='html.parser')
            for offer in bs.find_all('li', class_='listing__item'):
                if offer.find('a', class_='job-id'):
                    offer_url = offer.find('a', class_='job-id')['href'].split('#')[0]
                    offer_id = offer_url.split('_')[-1]
                    offer_url = f'{self.URL}{offer_url}'
                    if self.db.get_offer_id(offer_url=offer_url) == -1:
                        location = offer.find('div', class_='listing__location').get_text()
                        name = offer.find('a', class_='job-id').get_text().strip()
                        apply_url = f"{self.apply_url}{offer_id}"
                        self.db.add_new_offer(name=name,
                                              offer_url=offer_url,
                                              apply_url=apply_url,
                                              location=location,
                                              portal="praca.pl")
            if bs.find('a', class_='pagination__item--next'):
                page += 1
                print(page)
                continue
            break

    def get_offers_from_pracuj(self):
        self.URL = 'https://www.pracuj.pl/praca/'
        last_page = int(
            BeautifulSoup(get(self.URL).content, features='html.parser')
                          .findAll('li', class_='pagination_element-page')[-1].get_text())

        for page in range(1, last_page + 1):
            page_content = get(f'{self.URL}?pn={page}')
            bs = BeautifulSoup(page_content.content, features='html.parser')
            for offer in bs.find_all('li', class_='results__list-container-item'):
                if offer.find('a', class_='offer-details__title-link'):
                    offer_url = offer.find('a', class_='offer-details__title-link')['href']
                    if self.db.get_offer_id(offer_url=offer_url) == -1:
                        name = offer.find("h3", class_='offer-details__title').get_text().strip()
                        location = offer.find('li', class_='offer-labels__item--location').get_text().strip()
                        self.db.add_new_offer(name=name,
                                              offer_url=offer_url,
                                              location=location,
                                              portal="pracuj.pl")

            print(f"Loading... Done {round(page / last_page * 100, 2)}%")
