# AI-Powered Itinerary Planner

An AI-driven full-stack itinerary planner that uses Google Maps API to fetch location data and LLM (Large Language Model) to generate optimized travel itineraries based on user preferences.



## Preview
https://github.com/user-attachments/assets/f6c149b4-4aca-45d3-b4fd-5ee3c26e19cc

## Features
- Fetches places data from Google Maps API
- Uses LLM to generate customized travel itineraries
- Full-stack implementation with FastAPI (backend) and Svelte (frontend)
- Interactive and dynamic user experience
- Integrated chatbot for travel consultation using LLM

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/lekreys/fullstack-itinerary-planner-AI.git
cd fullstack-itinerary-planner-AI
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory and add the following:
```sh
API_KEY=your_google_api_key
API_KEY_OPENAI=your_openai_api_key
```

## Backend Setup (FastAPI)

### 1. Install Dependencies
```sh
pip install -r requirements.txt
```

### 2. Run the FastAPI Server
```sh
uvicorn main:app --reload
```

## Frontend Setup (Svelte)

### 1. Install Dependencies
```sh
cd frontend
npm install
```

### 2. Run the Development Server
```sh
npm run dev
```

## Usage
1. Enter your travel destination and duration.
2. The app will fetch places using Google Maps API.
3. The LLM will generate a detailed itinerary.
4. View, edit, or refine the itinerary as needed.
