import json, os
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from firebase_admin import credentials, auth, initialize_app


load_dotenv()
firebase_credentials = {
  "type": "service_account",
  "project_id": "balance-scale-app",
  "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
  "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.getenv("FIREBASE_CLIENT_ID"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.getenv("FIREBASE_CERT_URL"),
  "universe_domain": "googleapis.com"
}

cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)

async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]  # Assumes format: "Bearer <token>" 
        decoded_token = auth.verify_id_token(token, check_revoked=True, clock_skew_seconds=10)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")