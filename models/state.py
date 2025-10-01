#!/usr/bin/python3
""" State Module for HBNB project """

from models.base_model import BaseModel
from models.city import City
from models.base_model import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade="all, delete,delete-orphan")

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            '''returns the list of City instances with state_id
                equals the current State.id
                FileStorage relationship between State and City
            '''
            from models import storage
            related_cities = []

            # gets the entire storage- a dictionary
            cities = storage.all(City)
            # cities.value returns list of the city objects
            for city in cities.values():
                # if the object.state_id == self.id
                if city.state_id == self.id:
                    # append to the cities list
                    related_cities.append(city)
            return related_cities
