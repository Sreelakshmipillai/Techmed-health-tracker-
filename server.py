from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

lemmatizer = WordNetLemmatizer()

# Load resources
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Track pending appointment requests
pending_appointment = {}

# Available appointment slots for each doctor
available_slots = {
    "dr. sanjay roy": ["2025-04-29 10:00 AM", "2025-05-01 11:00 AM", "2025-05-03 2:00 PM"],
    "dr. george bell": ["2025-04-29 10:00 AM", "2025-04-30 2:00 PM", "2025-05-01 3:00 PM"],
    "dr. katherine": ["2025-04-29 9:00 AM", "2025-04-30 1:00 PM"],
    "dr. henry anderson": ["2025-04-29 11:00 AM", "2025-05-01 12:00 PM"]
}

# Doctor and specialization info
doctor_info = {
    "dr. sanjay roy": {
        "specialization": "Cardiologist",
        "doctor": "Dr. Sanjay Roy",
        "remedy": "Consult for heart-related issues."
    },
    "dr. george bell": {
        "specialization": "Dermatologist",
        "doctor": "Dr. George Bell",
        "remedy": "Consult for skin-related issues."
    },
    "dr. katherine": {
        "specialization": "Pediatrician",
        "doctor": "Dr. Katherine",
        "remedy": "Consult for child-related illnesses."
    },
    "dr. henry anderson": {
        "specialization": "Neurosurgeon",
        "doctor": "Dr. Henry Anderson",
        "remedy": "Consult for brain and nervous system issues."
    }
}

specialization_keywords = {
    "cardiologist": "dr. sanjay roy",
    "dermatologist": "dr. george bell",
    "pediatrician": "dr. katherine",
    "neurosurgeon": "dr. henry anderson"
}


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "I'm sorry, I didn't understand that."
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I'm not sure I understand. Can you rephrase?"

# Expanded Doctor suggestion function
def suggest_doctor(user_message):
    user_message = user_message.lower()

    # Check if doctor name is mentioned
    for doc_name, info in doctor_info.items():
        if doc_name in user_message:
            slots = available_slots.get(doc_name, [])
            if slots:
                pending_appointment['info'] = info
                pending_appointment['symptom'] = f"Appointment with {info['doctor']}"
                pending_appointment['slots'] = slots
                slots_list = "\n".join(slots)
                return (f"You asked for an appointment with {info['doctor']}. Available slots:\n{slots_list}\n\nPlease type your preferred date and time exactly as shown to book it.")
            else:
                return (f"Sorry, no available slots for {info['doctor']} at the moment.")

    # Check if specialization is mentioned
    for spec, doc_name in specialization_keywords.items():
        if spec in user_message:
            info = doctor_info[doc_name]
            slots = available_slots.get(doc_name, [])
            if slots:
                pending_appointment['info'] = info
                pending_appointment['symptom'] = f"Appointment with {info['doctor']} ({info['specialization']})"
                pending_appointment['slots'] = slots
                slots_list = "\n".join(slots)
                return (f"You asked for a {spec}. I recommend {info['doctor']}. Available slots:\n{slots_list}\n\nPlease type your preferred date and time exactly as shown to book it.")
            else:
                return (f"Sorry, no available slots for {info['doctor']} at the moment.")

    return None

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message'].strip().lower()

    # Check if user is responding to a pending appointment
    if 'info' in pending_appointment:
        selected_slot = message.strip()
        info = pending_appointment['info']
        slots = pending_appointment.get('slots', [])
        if selected_slot in slots:
            slots.remove(selected_slot)
            pending_appointment.clear()
            return jsonify({'reply': (f"✅ Successfully booked your appointment with {info['doctor']} at {selected_slot}!")})
        else:
            return jsonify({'reply': "Sorry, that slot is not available. Please select from the available slots listed."})

    # Check for doctor/specialization suggestion
    doctor_suggestion = suggest_doctor(message)
    if doctor_suggestion:
        return jsonify({'reply': doctor_suggestion})

    # Else normal chatbot flow
    intents_list = predict_class(message)
    response = get_response(intents_list, intents)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(port=5000)