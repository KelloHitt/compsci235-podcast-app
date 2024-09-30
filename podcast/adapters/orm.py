from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from podcast.domainmodel import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()


# TODO: create tables

# TODO: mapping the domain model to the tables
def map_model_to_tables():
    pass
