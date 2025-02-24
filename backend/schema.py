import pydantic
from pydantic import BaseModel 



class function_calling_place(BaseModel):

    prompt : str
    model : str



class nearby_places(BaseModel) : 
    longitude : str
    latitude : str
    type_place : str
    radius : int

class all_place(BaseModel) :
    query : str
    token : str


class coordinate(BaseModel):
    place : str


class detail_place(BaseModel):
    place : str


class generate_itinerary(BaseModel) : 
    jumlah_hari : str
    jam_mulai : str
    json_data_tempat : str
    place_type : str
    model : str


class chatbot(BaseModel):
    messages : list
