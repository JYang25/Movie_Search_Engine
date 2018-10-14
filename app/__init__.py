from flask import Flask
from Process_Metadata import LoadMovie, Movie, Create_Index, ParseWords, Idx
# from Process_Metadata import LoadMovie, Movie

app = Flask(__name__)
app.config.from_object('config')

# load the movies data
Movies = LoadMovie()

# create index from movies
Index = Create_Index(Movies)

from app import views

