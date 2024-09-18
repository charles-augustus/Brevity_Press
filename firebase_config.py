# firebase_config.py
import pyrebase

# Firebase configuration
firebase_config = {
    'apiKey': "AIzaSyCKAvAzbq3vjtGGv-7tSu0ZWPuFq5La3qI",
    'authDomain': "newspaper-d8e6e.firebaseapp.com",
    'databaseURL': "https://newspaper-d8e6e-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'projectId': "newspaper-d8e6e",
    'storageBucket': "newspaper-d8e6e.appspot.com",
    'messagingSenderId': "139831674443",
    'appId': "1:139831674443:web:0833a9ed489d8c6cdcefce",
    'measurementId': "YOUR_MEASUREMENT_ID"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
