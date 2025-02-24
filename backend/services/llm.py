import os
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage , SystemMessage , AIMessage
from schema import function_calling_place , generate_itinerary , chatbot 
from fastapi import APIRouter, HTTPException
from langchain.prompts import PromptTemplate



API_KEY = os.getenv("API_KEY_OPENAI")
router = APIRouter()

@router.post("/function_calling_Place")
def function_calling_place(request: function_calling_place):
    tools = [{
        "name": "get_itinerary_details",
        "description": "Extract location, number of days, and start time from user input.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The name of a city or country mentioned in the user's input."
                },
                "days": {
                    "type": "integer",
                    "description": "The number of days for the trip."
                },
                "start_time": {
                    "type": "string",
                    "description": "The starting time of the itinerary in HH:MM format."
                }
            },
            "required": ["location", "days", "start_time"],
        },
    }]

    try:

        llm = ChatOpenAI(model=request.model, api_key=API_KEY)

        get_details = llm.invoke([HumanMessage(content=request.prompt)], functions=tools)

        arguments = get_details.additional_kwargs.get("function_call", {}).get("arguments", "{}")
        parsed_args = json.loads(arguments)

        location = parsed_args.get("location", None)
        days = parsed_args.get("days", None)
        start_time = parsed_args.get("start_time", None)

        if not location or not days or not start_time:
            raise ValueError("Missing required itinerary details.")

        return {"location": location, "days": days, "start_time": start_time}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






template = PromptTemplate.from_template(

    """

        Saya ingin Anda membuat itinerary perjalanan berdasarkan data tempat yang saya berikan.

        Berikut adalah daftar tempat yang tersedia di destinasi ini:
        {json_data_tempat}

        buatkan itinerary untuk {jumlah_hari} hari 

        Tolong buat itinerary harian yang efisien dan menyenangkan, dengan mempertimbangkan waktu perjalanan antar lokasi.
        Pastikan tiap hari memiliki jadwal yang jelas mulai dari pagi hingga malam hingga jamnya , saya mau setiap hari itinerary dibuat mulai dari jam {jam_mulai} hingga jam 9 malam.

        saya ingin itinerary ini dibuat dengan memprioritaskan tempat yang bertipe {place_type}

        Format output yang saya inginkan dalam bentuk JSON seperti ini dan hanya jsonnya:

            {{
            "result": [
                {{
                "day": 1,
                "date": "YYYY-MM-DD",
                "schedule": [
                    {{
                    "time": "08:00",
                    "activity": "Sarapan di tempat terbaik",
                    "location": "Nama restoran",
                    "latitude" :  sesuai di jsonnya yang aku berikan,
                    "longitude" : sesuai di jsonnya yang aku berikan,
                    "description": "Deskripsi aktivitas.",
                    "photo_url" :  sesuai di jsonnya yang aku berikan,
                    "place_id" : sesuai di jsonnya yang aku berikan,
                    "ratings" :  sesuai di jsonnya yang aku berikan,
                    "global_code" : sesuai di jsonnya yang aku berikan,
                    "user_rating_total" :  sesuai di jsonnya yang aku berikan,
                    "vicinity" :  sesuai di jsonnya yang aku berikan,
                    "types" :  sesuai di jsonnya yang aku berikan
                    }},
                    {{
                    "time": "10:00",
                    "activity": "Mengunjungi tempat wisata",
                    "location": "sesuai di jsonnya yang aku berikan",
                    "latitude" :  sesuai di jsonnya yang aku berikan,
                    "longitude" : sesuai di jsonnya yang aku berikan,
                    "description": "Deskripsi aktivitas.",
                    "photo_url" :  sesuai di jsonnya yang aku berikan,
                    "place_id" : sesuai di jsonnya yang aku berikan,
                    "ratings" :  sesuai di jsonnya yang aku berikan,
                    "global_code" : sesuai di jsonnya yang aku berikan,
                    "user_rating_total" :  sesuai di jsonnya yang aku berikan,
                    "vicinity" :  sesuai di jsonnya yang aku berikan,
                    "types" :  sesuai di jsonnya yang aku berikan
                    }}
                ]
                }}
            ]
            }}
    """   
)






system_chat = """
    Kamu adalah AI Trip Planner yang membantu pengguna menemukan rekomendasi tempat wisata, transportasi, akomodasi, dan tips perjalanan. 

    **Cara Memberikan Rekomendasi:**
    - Jika pengguna bertanya tentang tempat wisata, berikan:
    1. Nama tempat
    2. Deskripsi singkat
    3. Aktivitas yang bisa dilakukan
    4. Lokasi & cara menuju ke sana

    - Jika pengguna menanyakan transportasi, jelaskan opsi seperti kereta, bus, pesawat, atau rental mobil tergantung lokasinya.
    - Jika pengguna bertanya tentang akomodasi, berikan beberapa pilihan berdasarkan anggaran: **budget, standar, dan luxury**.

    **Jika pengguna meminta itinerary lengkap**, langsung arahkan ke sistem itinerary generator dengan menjawab:
    _"Untuk membuat itinerary, silakan gunakan fitur itinerary planner kami."_  

    Gunakan bahasa yang ramah, singkat, dan informatif. Jika ada pertanyaan tidak terkait perjalanan, katakan bahwa kamu hanya bisa membantu dalam perencanaan trip.

    ---

    **Contoh Interaksi:**
    **User:** "Aku mau ke Jepang, ada rekomendasi tempat wisata?"  
    **AI:** "Tentu! Berikut beberapa tempat menarik di Jepang:  
    1. **Fushimi Inari Taisha (Kyoto)** – Kuil dengan ribuan gerbang merah ikonik.  
    2. **Shibuya Crossing (Tokyo)** – Penyebrangan jalan tersibuk di dunia.  
    3. **Mount Fuji** – Gunung berapi terkenal yang bisa dinikmati dari Danau Kawaguchi."

    **User:** "Bisa buatkan itinerary 5 hari di Jepang?"  
    **AI:** "Untuk membuat itinerary, silakan gunakan fitur itinerary planner kami."  

    ---

    Siap bantuin trip selanjutnya, bro? 🚀😎

    """

@router.post("/generate_itinerary")
def generate_itinerary(request : generate_itinerary): 
        

    filled_prompt = template.format(
        jumlah_hari=request.jumlah_hari,
        jam_mulai=request.jam_mulai,
        json_data_tempat=request.json_data_tempat,
        place_type=request.place_type
    )

    llm = ChatOpenAI(model=request.model, api_key=API_KEY)
    response = llm.invoke([HumanMessage(content=filled_prompt)])

    ititnerary = response.content

    try:
        clean_json = ititnerary.replace("\\n", "").replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        print("JSON berhasil di-load:", data)
    except json.JSONDecodeError as e:
         print("Error decoding JSON:", e)

    
    return data



@router.post("/chatbot")
async def chat(request: chatbot):

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, openai_api_key=API_KEY)

    messages = [{"role" : "system" , "content" : system_chat }]
    for msg in request.messages:
        if msg['role'] == "system":
            messages.append(SystemMessage(content=msg["content"]))
        elif msg['role'] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg['role'] == "assistant":
            messages.append(AIMessage(content=msg["content"]))  
    
    response = llm.invoke(messages)

    return {"role":"assistant" ,  "content" : response.content}



