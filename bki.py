from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
from functools import wraps
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyDul5bK14kfgvEVZXi64vgTtzTQzWloU5o")

NEWS_API_KEY = "d0ab919abf90e8f69d8f15455c3207dd"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 20,
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

chat_session = model.start_chat()
MEDICAL_PROMPT = "You are an AI expert in the medical field in India. Answer queries strictly within the context of medicine, healthcare, diseases, treatments, and related medical topics of India."

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    return decorated_function

@app.route('/api/chat', methods=['POST'])
@handle_errors
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No message provided'
        }), 400

    query = data['message'].strip().lower()

    if query == "emergency contact":
        return jsonify({
            'status': 'success',
            'response': {
                'police': '100',
                'ambulance': '102',
                'fire': '101'
            }
        })

    full_query = f"{MEDICAL_PROMPT} {query}"
    response = chat_session.send_message(full_query)

    return jsonify({
        'status': 'success',
        'response': response.text
    })

@app.route('/api/news', methods=['GET'])
@handle_errors
def get_medical_news():
    params = {
        'apiKey': NEWS_API_KEY,
        'category': 'health',
        'language': 'en',
        'country': 'in',
    }

    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    news_data = response.json()

    headlines = [article['title'] for article in news_data.get('articles', [])]

    return jsonify({
        'status': 'success',
        'headlines': headlines
    })

@app.route('/api/emotional-assessment', methods=['POST'])
@handle_errors
def assess_emotion():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({
            'status': 'error',
            'message': 'No message provided'
        }), 400

    query = data['message'].lower()

    if any(word in query for word in ["overwhelmed", "stress", "work", "anxiety"]):
        response_type = "stress"
        response = {
            "message": "It seems like you're feeling overwhelmed.",
            "techniques": [
                "Deep breathing exercises",
                "Time management techniques",
                "Mindfulness meditation",
                "Regular breaks during work",
                "Talking to a counselor"
            ],
            "resources": ["https://www.thelivelovelaughfoundation.org/"]
        }
    elif "depressed" in query or "sad" in query:
        response_type = "depression"
        response = {
            "message": "I'm sorry you're feeling this way.",
            "resources": [
                {"name": "iCall Helpline", "url": "https://www.icallhelpline.org/"},
                {"name": "LiveLoveLaugh Foundation", "url": "https://www.thelivelovelaughfoundation.org/"}
            ]
        }
    else:
        response_type = "general"
        response = {
            "message": "I'm here to listen and provide support. Could you tell me more about what you're feeling?"
        }

    return jsonify({
        'status': 'success',
        'type': response_type,
        'response': response
    })

@app.route('/api/counselors', methods=['GET'])
@handle_errors
def get_counselors():
    counselors = [
        {
            "name": "Sahai - Mental Health Support",
            "services": ["Counseling", "therapy for mental health issues", "stress", "anxiety", "depression"],
            "location": "Delhi NCR",
            "online_available": True,
            "contact": "+91 98103 93607"
        },
        {
            "name": "The Mind Research Foundation",
            "services": ["Psychological counseling", "therapy", "mental health assessments"],
            "location": "Multiple locations in Delhi",
            "contact": "+91 98998 70879"
        },
        {
            "name": "Fortis Healthcare - Mental Health Services",
            "services": ["Clinical psychologists", "therapists", "psychiatrists", "anxiety", "depression", "stress management"],
            "location": "Fortis Escorts Heart Institute, Okhla Road, Delhi",
            "contact": "+91 11 4711 2222"
        }
    ]

    return jsonify({
        'status': 'success',
        'counselors': counselors
    })

@app.route('/api/resources', methods=['GET'])
@handle_errors
def get_mental_health_resources():
    resources = [
        {
            "name": "iCall - Online Counseling Service",
            "services": ["free counseling", "confidential counseling"],
            "hours": "9 AM - 9 PM every day",
            "website": "https://www.icallhelpline.org/",
            "contact": "+91 91529 8484"
        },
        {
            "name": "The Live Love Laugh Foundation",
            "services": ["online counseling", "mental health resources"],
            "website": "https://www.thelivelovelaughfoundation.org/",
            "contact": "+91 80109 80109",
            "available": "24/7"
        },
        {
            "name": "Snehi - Suicide Prevention Helpline",
            "services": ["suicide prevention", "crisis support"],
            "website": "http://www.snehi.org/",
            "contact": ["91-22-2772 6771", "91-22-2772 6773"],
            "hours": "9 AM - 9 PM"
        }
    ]

    return jsonify({
        'status': 'success',
        'resources': resources
    })

@app.route('/api/cbt-exercises', methods=['GET'])
@handle_errors
def get_cbt_exercises():
    exercises = [
        {
            "name": "Thought records",
            "description": "Document and analyze thoughts, emotions, and behaviors",
            "recommended_duration": "15-20 minutes daily"
        },
        {
            "name": "Behavioral activation",
            "description": "Schedule and engage in activities that bring joy or accomplishment",
            "recommended_duration": "30 minutes daily"
        },
        {
            "name": "Cognitive restructuring",
            "description": "Identify and challenge negative thought patterns",
            "recommended_duration": "20-30 minutes per session"
        },
        {
            "name": "Mindfulness",
            "description": "Practice present-moment awareness without judgment",
            "recommended_duration": "10-15 minutes daily"
        },
        {
            "name": "Journaling",
            "description": "Write down thoughts and feelings to identify patterns",
            "recommended_duration": "15-20 minutes daily"
        }
    ]

    return jsonify({
        'status': 'success',
        'exercises': exercises
    })

if __name__ == '__main__':
    print('Hello, I’m Mr. Medical. I can provide information on medical topics. How can I help you?')

    while True:
        print("Waiting for your input...")
        query = input("mr. medical: ").strip().lower()

        if query:
            if query in ["quit", "exit"]:
                print("Ending chat. Goodbye!")
                break
            elif query == "emergency contact":
                print("\u2022 Police: 100 \u2022 Ambulance: 102 \u2022 Fire: 101")
            elif query == "counselors":
                counselors = requests.get('http://127.0.0.1:5000/api/counselors').json()
                print(json.dumps(counselors, indent=2))
            elif query == "news":
                news = requests.get('http://127.0.0.1:5000/api/news').json()
                print("Latest Health News:", json.dumps(news.get('headlines', []), indent=2))
            elif query == "suggest some cbt based exercise":
                cbt_exercises = requests.get('http://127.0.0.1:5000/api/cbt-exercises').json()
                for exercise in cbt_exercises.get('exercises', []):
                    print(f"- {exercise['name']}: {exercise['description']} ({exercise['recommended_duration']})")
            elif query == "online mental health resources":
                resources = requests.get('http://127.0.0.1:5000/api/resources').json()
                print("Online Mental Health Resources:", json.dumps(resources, indent=2))
            else:
                full_query = f"{MEDICAL_PROMPT} {query}"
                try:
                    response = chat_session.send_message(full_query)
                    print("mr. medical:", response.text)
                except Exception as e:
                    print("An error occurred:", e)

    app.run(debug=True)
