from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

load_dotenv()
Base = declarative_base()


class WorkOffers(Base):
    __tablename__ = 'work_offers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191))
    location = Column(String(191))
    offer_url = Column(String(191), unique=True)
    apply_url = Column(String(191))
    portal_id = Column(Integer, ForeignKey('portals.id'), nullable=False)
    added = Column(DateTime)

    portals = relationship('Portals', back_populates='work_offers')


class Portals(Base):
    __tablename__ = 'portals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(191), unique=True)

    work_offers = relationship('WorkOffers', back_populates='portals')


class Database:
    def __init__(self,
                 db_host=getenv('DB_HOST'),
                 db_port=getenv('PORT'),
                 db_user=getenv('DB_USER'),
                 db_password=getenv('DB_PASSWORD'),
                 database=getenv('DATABASE'),
                 test=True):
        if test:
            self.engine = create_engine('sqlite:///database.db')
            self.create_database()
        else:
            self.engine = create_engine(f'mysql://{db_user}:{db_password}@{db_host}:{db_port}/{database}')
        self.Session = sessionmaker(bind=self.engine)
        self.sess = self.Session()

    def create_database(self):
        Base.metadata.create_all(self.engine)

    def get_offer_id(self, offer_url: str) -> int:
        if offer_id := self.sess.query(WorkOffers).filter_by(offer_url=offer_url).first():
            return offer_id.id
        return -1

    def get_portal_id(self, portal: str) -> int:
        if brand_id := self.sess.query(Portals).filter_by(name=portal).first():
            return brand_id.id
        else:
            self.sess.add(Portals(name=portal))
            self.sess.commit()
        return self.sess.query(Portals).filter_by(name=portal).first().id

    def add_new_offer(self,
                      name: str,
                      offer_url: str,
                      location: str,
                      portal: str,
                      apply_url: str = "",
                      added=datetime.now()):

        print(f"adding {name}: {offer_url}")

        self.sess.add(WorkOffers(name=name,
                                 location=location,
                                 offer_url=offer_url,
                                 apply_url=apply_url,
                                 portal_id=self.get_portal_id(portal=portal),
                                 added=added))
        self.sess.commit()
