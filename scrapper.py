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
