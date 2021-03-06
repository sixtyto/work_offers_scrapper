from scrapper import Scrapper

sc = Scrapper()

print('Getting offers from olx.pl')
sc.get_offers_from_olx()

print('Getting values from praca.pl')
sc.get_offers_from_praca()

print('Getting offers from pracuj.pl')
sc.get_offers_from_pracuj()
