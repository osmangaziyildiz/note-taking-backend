import firebase_admin
from firebase_admin import credentials, firestore, auth
from src.core.config import settings

# Initialize Firebase Admin SDK
cred = credentials.Certificate(settings.firebase_credentials_path)
firebase_admin.initialize_app(cred)

# Easy access to Firestore and Auth services
db = firestore.client()
firebase_auth = auth