import os

class Config:
    #debug = True
    SECRET_KEY = 'gaidi'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:Access@localhost/pitch'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    