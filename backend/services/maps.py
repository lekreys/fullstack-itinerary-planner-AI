from fastapi import APIRouter
import requests
import urllib.parse
from schema import nearby_places , all_place , coordinate , detail_place
import os




router = APIRouter()

API_KEY = os.getenv("API_KEY")



@router.post("/google_coordinate")
def google_coordinate(request : coordinate):

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={request.place}&key={API_KEY}"
    response = requests.get(url).json()

    return {
    "place_name" : response["results"][0]["formatted_address"],
    "latitude" : response["results"][0]['geometry']["viewport"]['northeast']['lng'],
    "longitude" : response["results"][0]['geometry']["viewport"]['northeast']['lat'] 
    }



@router.post("/google_nearby_place")
def google_place_nearby(request : nearby_places ) :

    coordinate= f"{request.longitude},{request.latitude}"
    radius = request.radius * 1000

    url= f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinate}&radius={radius}&type={request.type_place}&key={API_KEY}"
    data = requests.get(url).json()

    info_list = {"results" : []}

    for i in range(0,len(data["results"])) :

        result = data["results"][i] 

        photo_url = None

        photos = result.get("photos", [])        
        if photos and "html_attributions" in photos[0]:
            photo_url = photos[0]["html_attributions"][0].split('"')[1]


        dictionary_pllace = {

            "name" : result.get("name" , None),
            "photo_url" : photo_url,
            "place_id" : result.get("place_id" , None),
            "ratings" : result.get("rating" , None),
            "global_code" :result.get("plus_code" , {}).get("global_code" , None),
            "user_rating_total" : result.get('user_ratings_total' , None),
            "vicinity" : result.get('vicinity'),
            "latitude": result.get("geometry", {}).get("viewport", {}).get("northeast", {}).get("lng"),
            "longitude": result.get("geometry", {}).get("viewport", {}).get("northeast", {}).get("lat")


        }

        print( dictionary_pllace)

        info_list["results"].append(dictionary_pllace)


    return info_list


@router.post("/google_place")
def google_place(request : all_place) :

    next_token = ""

    encoded_query = urllib.parse.quote_plus(request.query)

    url= f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={request.token}&query={encoded_query}&key={API_KEY}"
    data = requests.get(url).json()        


    info_list = {"results" : [] , "token" : ""}

    if 'next_page_token' in data:
        info_list["token"] = data['next_page_token']


    for i in range(0,len(data["results"])) :

        result = data["results"][i] 

        photo_url = None

        photos = result.get("photos", [])        
        if photos and "html_attributions" in photos[0]:
            photo_url = photos[0]["html_attributions"][0].split('"')[1]


        dictionary_pllace = {
            "name" : result.get("name" , None),
            "photo_url" : photo_url,
            "place_id" : result.get("place_id" , None),
            "ratings" : result.get("rating" , None),
            "global_code" :result.get("plus_code" , {}).get("global_code" , None),
            "user_rating_total" : result.get('user_ratings_total' , None),
            "vicinity" : result.get('vicinity'),
            "types" :  result.get('types'),
            "latitude": result.get("geometry", {}).get("viewport", {}).get("northeast", {}).get("lng"),
            "longitude": result.get("geometry", {}).get("viewport", {}).get("northeast", {}).get("lat")
        }

        print( dictionary_pllace)

        info_list["results"].append(dictionary_pllace)


    return info_list




@router.post("/detail_place")
def detail_place(request : detail_place):

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={request.place}&fields=name,rating,formatted_address,geometry,photo,opening_hours,reviews&key=AIzaSyBHWaZzVoN9YgdzEAQ4fnHCDJbaenn0dj4"

    response = requests.get(url)
    data = response.json()

    result_data = data.get("result", {})

    result = {
        "name": result_data.get("name", None),
        "location": result_data.get("geometry", {}).get("location", None),
        "opening_hours": result_data.get("opening_hours", {}).get("periods", None),
        "rating": result_data.get("rating", None),
        "reviews": result_data.get("reviews", None)
    }

    return result

