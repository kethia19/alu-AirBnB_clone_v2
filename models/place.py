#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Table, ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
import models


class Place(BaseModel, Base):

    """ A place to stay """
    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        reviews = relationship('Review', cascade='all, delete,delete-orphan',
                               backref='place')

        place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id',
                ForeignKey('places.id'),
                primary_key=True,
                nullable=False),
            Column(
                'amenity_id',
                ForeignKey('amenities.id'),
                primary_key=True,
                nullable=False))
        amenities = relationship('Amenity', secondary=place_amenity,
                                 viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            '''returns the list of Review instances with place_id
                equals the current Place.id
                FileStorage relationship between Place and Review
            '''
            from models import storage
            related_reviews = []
            reviews = storage.all(Review).items()
            for review in reviews.values():
                if review.place_id == self.id:
                    related_reviews.append(review)
            return related_reviews

        @property
        def amenities(self):
            '''returns the list of Review instances with place_id
                equals the current Place.id
                FileStorage relationship between Place and Review
            '''
            from models import storage
            related_amenities = []

            amenities = storage.all(Amenity).items()
            for amenity in amenities.values():
                if amenity.place_id == self.id:
                    related_amenities.append(amenity)
            return related_amenities

        @amenities.setter
        def amenities(self, obj):
            if obj is None:
                pass
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity.id:
                    self.amenity_ids.append(obj.id)
